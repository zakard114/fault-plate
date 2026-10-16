# On-call agent

This agent wakes up when the alert `saved_plate_unavailable` is active. That alert means `GET /plates` returned 404, so a caller cannot read the saved card.

The fix posts the runbook card: name `Payment authorization failed`, the payment sentence, HTTP status 400, log field `amount`, retry `not_retryable`.

```powershell
python custom-agent/agent.py
```

`PLATE_URL` defaults to `https://fault-plate.onrender.com`. The agent does not log the card text. It does not deploy.
