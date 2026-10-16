import json
from datetime import datetime, timezone

def new_trace_id() -> str:
    from uuid import uuid4
    return uuid4().hex[:16]

def decide_alert(method: str, path: str, status: int) -> str | None:
    if method == "GET" and path == "/plates" and status == 404:
        return "saved_plate_unavailable"
    if method == "POST" and path == "/plates" and status >= 500:
        return "plate_save_failed"
    return None

def log_line(trace_id: str, method: str, path: str, status: int, duration_ms: int) -> str:
    return json.dumps(
        {
            "trace_id": trace_id,
            "method": method,
            "path": path,
            "status": status,
            "duration_ms": duration_ms,
        },
        separators=(",", ":"),
    )

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
