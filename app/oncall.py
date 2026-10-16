import json
import urllib.request

RUNBOOK_PLATE = {
    "name": "Payment authorization failed",
    "user_facing_message": "We could not complete your payment.",
    "http_status": 400,
    "log_fields": "amount",
    "retry_allowed": "not_retryable",
}

def active_alert_names(alerts: list[dict]) -> set[str]:
    return {item["name"] for item in alerts if item.get("active")}

def repair(get_json, post_json) -> str:
    names = active_alert_names(get_json("/alerts"))
    if "saved_plate_unavailable" not in names:
        return "clear"
    post_json("/plates", RUNBOOK_PLATE)
    return "restored"

def repair_url(base_url: str) -> str:
    base = base_url.rstrip("/")

    def get_json(path: str):
        with urllib.request.urlopen(base + path) as response:
            return json.loads(response.read().decode())

    def post_json(path: str, body: dict):
        data = json.dumps(body).encode()
        request = urllib.request.Request(
            base + path,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode())

    return repair(get_json, post_json)
