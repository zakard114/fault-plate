from app.telemetry import decide_alert, log_line

def test_missing_plate_alert():
    assert decide_alert("GET", "/plates", 404) == "saved_plate_unavailable"

def test_save_does_not_alert():
    assert decide_alert("POST", "/plates", 201) is None

def test_log_line_has_trace_and_no_card_text():
    line = log_line("abc123", "POST", "/plates", 201, 4)
    assert "abc123" in line
    assert "user_facing_message" not in line
    assert "payment" not in line
