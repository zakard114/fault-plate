from fastapi.testclient import TestClient

import app.main as main
from app.oncall import repair

def test_oncall_restores_missing_plate(tmp_path, monkeypatch):
    monkeypatch.setenv("PLATE_DB", str(tmp_path / "plate.sqlite"))
    with TestClient(main.app) as test_client:
        missing = test_client.get("/plates")
        assert missing.status_code == 404
        assert missing.headers["x-trace-id"]
        alerts = test_client.get("/alerts").json()
        assert any(item["name"] == "saved_plate_unavailable" and item["active"] for item in alerts)

        def get_json(path):
            return test_client.get(path).json()

        def post_json(path, body):
            response = test_client.post(path, json=body)
            assert response.status_code == 201
            return response.json()

        assert repair(get_json, post_json) == "restored"
        restored = test_client.get("/plates")
        assert restored.status_code == 200
        assert restored.json()["name"] == "Payment authorization failed"
        ops = test_client.get("/ops")
        assert ops.status_code == 200
        assert "saved_plate_unavailable" in ops.text
        assert "We could not complete your payment." not in ops.text
