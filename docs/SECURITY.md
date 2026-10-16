# Security review

Date: 2026-10-11

## Public files

`git ls-files` at review time:

```text
.dockerignore
.gitignore
Dockerfile
README.md
app/__init__.py
app/index.html
app/main.py
openapi.yaml
pytest.ini
requirements.txt
tests/test_plates.py
```

`docker-compose.yaml` was local then because it contained a machine path. The committed compose file uses `./data` instead.

## Secret scan

The scan searched `*.py`, `*.html`, `*.yaml`, `*.yml`, `*.md`, `*.txt`, and `Dockerfile`, and skipped `venv`, `.venv`, `.git`, and `data`.

The pattern was `api[_-]?key|secret|password|BEGIN PRIVATE|sk-`.

The only hit was the scan command text stored in an untracked local note. That line is not a key or a password. The note is not in `git ls-files`.

## What a person checked

Files read: `app/main.py`, `app/index.html`, `agent-capabilities/permissions.md`, `agent-capabilities/hooks/check_plate.py`, `agent-capabilities/mcp/server.py`, `agent-capabilities/mcp/fetch_plate.py`.

- The code does not contain an API key, a password, or a private key.
- `check_plate.py` looks at the five JSON fields and does not create or edit files.
- `get_plate` and `fetch_plate.py` call `GET /plates` only.
- The public list did not include the local notes.
- `POST /plates` has no login, so one saved card can be replaced. This product records that limit and does not add login.
