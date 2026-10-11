import os
import sqlite3
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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

app = FastAPI(title="Fault Plate API", version="1.0.0")

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


from fastapi.responses import FileResponse

@app.get("/")
def home():
    return FileResponse(Path(__file__).resolve().parent / "index.html")
