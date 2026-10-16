# Fault Plate

One specification card for one API failure. Five fields. Saving the card finishes that failure.

## Read first

- Product spec: `docs/product-spec.md`
- Task tracker: `docs/tracker.md`
- Workflow: `docs/workflow.md`
- Agent team: `docs/team.md`
- Contract: `openapi.yaml`
- Security: `docs/SECURITY.md`
- Permissions: `agent-capabilities/permissions.md`

## Commands

```powershell
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
pytest
docker compose up --build
python custom-agent/agent.py
```

## Boundaries

- Do not add a second screen, a login, or a log root-cause search.
- Do not copy another course app into this repository.
- Do not put secrets or machine paths in a commit.
- The reviewer skill and subagent are read-only.
- The on-call agent may post the runbook card. It may not deploy.
