import html
import os
import sqlite3
import time
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from app.telemetry import decide_alert, log_line, new_trace_id, utc_now

class Plate(BaseModel):
    name: str
    user_facing_message: str
    http_status: int
    log_fields: str
    retry_allowed: Literal["retryable", "not_retryable"]


def db_path() -> Path:
    override = os.environ.get("PLATE_DB")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent / "data" / "plate.sqlite"

def connect():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)

def init_db():
    with connect() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS plate (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL,
                user_facing_message TEXT NOT NULL,
                http_status INTEGER NOT NULL,
                log_fields TEXT NOT NULL,
                retry_allowed TEXT NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS signal (
                id INTEGER PRIMARY KEY,
                trace_id TEXT NOT NULL,
                method TEXT NOT NULL,
                path TEXT NOT NULL,
                status INTEGER NOT NULL,
                duration_ms INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS alert (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                trace_id TEXT NOT NULL,
                active INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )

app = FastAPI(title="Fault Plate API", version="1.0.0")

def record_signal(trace_id: str, method: str, path: str, status: int, duration_ms: int) -> None:
    line = log_line(trace_id, method, path, status, duration_ms)
    print(line, flush=True)
    with connect() as con:
        con.execute(
            """
            INSERT INTO signal (trace_id, method, path, status, duration_ms, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (trace_id, method, path, status, duration_ms, utc_now()),
        )
        alert_name = decide_alert(method, path, status)
        if alert_name:
            con.execute(
                """
                INSERT INTO alert (name, trace_id, active, created_at)
                VALUES (?, ?, 1, ?)
                """,
                (alert_name, trace_id, utc_now()),
            )
        if method == "POST" and path == "/plates" and status == 201:
            con.execute(
                "UPDATE alert SET active = 0 WHERE name = 'saved_plate_unavailable' AND active = 1"
            )

@app.middleware("http")
async def trace_request(request: Request, call_next):
    trace_id = new_trace_id()
    started = time.perf_counter()
    response = await call_next(request)
    duration_ms = int((time.perf_counter() - started) * 1000)
    record_signal(trace_id, request.method, request.url.path, response.status_code, duration_ms)
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.on_event("startup")
def startup():
    init_db()

@app.post("/plates", status_code=201)
def create_plate(plate: Plate) -> Plate:
    with connect() as con:
        con.execute(
            """
            INSERT INTO plate (
                id, name, user_facing_message, http_status, log_fields, retry_allowed
            )
            VALUES (1, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                user_facing_message = excluded.user_facing_message,
                http_status = excluded.http_status,
                log_fields = excluded.log_fields,
                retry_allowed = excluded.retry_allowed
            """,
            (
                plate.name,
                plate.user_facing_message,
                plate.http_status,
                plate.log_fields,
                plate.retry_allowed,
            ),
        )
    return plate

@app.get("/plates")
def read_plate() -> Plate:
    with connect() as con:
        row = con.execute(
            """
            SELECT name, user_facing_message, http_status, log_fields, retry_allowed
            FROM plate
            WHERE id = 1
            """
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="no plate")
    return Plate(
        name=row[0],
        user_facing_message=row[1],
        http_status=row[2],
        log_fields=row[3],
        retry_allowed=row[4],
    )


@app.get("/")
def home():
    return FileResponse(Path(__file__).resolve().parent / "index.html")

@app.get("/alerts")
def read_alerts() -> list[dict]:
    with connect() as con:
        rows = con.execute(
            """
            SELECT name, trace_id, active, created_at
            FROM alert
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
    return [
        {"name": row[0], "trace_id": row[1], "active": bool(row[2]), "created_at": row[3]}
        for row in rows
    ]

@app.get("/metrics", response_class=PlainTextResponse)
def metrics() -> str:
    with connect() as con:
        rows = con.execute(
            "SELECT path, status, COUNT(*) FROM signal GROUP BY path, status"
        ).fetchall()
    lines = ["# fault plate request counts"]
    for path, status, count in rows:
        lines.append(f'fault_plate_requests{{path="{path}",status="{status}"}} {count}')
    return "\n".join(lines) + "\n"

@app.get("/ops", response_class=HTMLResponse)
def ops() -> str:
    with connect() as con:
        signals = con.execute(
            """
            SELECT trace_id, method, path, status, duration_ms, created_at
            FROM signal
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
        alerts = con.execute(
            """
            SELECT name, trace_id, active, created_at
            FROM alert
            ORDER BY id DESC
            LIMIT 20
            """
        ).fetchall()
    def cell(value: object) -> str:
        return html.escape(str(value))

    signal_rows = "".join(
        "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
            *(cell(value) for value in row)
        )
        for row in signals
    )
    alert_rows = "".join(
        "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(
            cell(row[0]), cell(row[1]), "active" if row[2] else "clear", cell(row[3])
        )
        for row in alerts
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Fault Plate ops</title></head>
<body>
<h1>Fault Plate ops</h1>
<p>Paths, status codes, and durations. Card text is not stored here.</p>
<h2>Alerts</h2>
<table>
<tr><th>Name</th><th>Trace</th><th>State</th><th>Time</th></tr>
{alert_rows}
</table>
<h2>Signals</h2>
<table>
<tr><th>Trace</th><th>Method</th><th>Path</th><th>Status</th><th>ms</th><th>Time</th></tr>
{signal_rows}
</table>
</body>
</html>
"""
