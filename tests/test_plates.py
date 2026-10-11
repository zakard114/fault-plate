import pytest
from fastapi.testclient import TestClient
import app.main as main

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("PLATE_DB", str(tmp_path / "plate.sqlite"))
    with TestClient(main.app) as test_client:
        yield test_client

def test_save_five_fields(client):
    body = {
        "name": "Payment authorization failed",
        "user_facing_message": "We could not complete your payment.",
        "http_status": 400,
        "log_fields": "amount",
        "retry_allowed": "retryable",
    }
    saved = client.post("/plates", json=body)
    assert saved.status_code == 201
    assert saved.json() == body
    read = client.get("/plates")
    assert read.status_code == 200
    assert read.json() == body

def test_reject_bad_retry(client):
    body = {
        "name": "Payment authorization failed",
        "user_facing_message": "We could not complete your payment.",
        "http_status": 400,
        "log_fields": "amount",
        "retry_allowed": "sometimes",
    }
    response = client.post("/plates", json=body)
    assert response.status_code == 422
