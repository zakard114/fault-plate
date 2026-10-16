from fastapi.testclient import TestClient

import app.main as main

def test_oncall_wakes_when_the_plate_is_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("PLATE_DB", str(tmp_path / "plate.sqlite"))
    with TestClient(main.app) as test_client:
        missing = test_client.get("/plates")
        assert missing.status_code == 404
        assert missing.headers["x-trace-id"]
        alerts = test_client.get("/alerts").json()
        assert any(
            item["name"] == "saved_plate_unavailable" and item["active"] is False
            for item in alerts
        )
        restored = test_client.get("/plates")
        assert restored.status_code == 200
        assert restored.json()["name"] == "Payment authorization failed"
        ops = test_client.get("/ops")
        assert ops.status_code == 200
        assert "saved_plate_unavailable" in ops.text
        assert "We could not complete your payment." not in ops.text
