# Workflow

One failure, one card, one save.

1. Write the five fields in `docs/product-spec.md` before changing the screen.
2. Keep the screen on `GET /`. Save stays on that screen.
3. `POST /plates` stores one row. `GET /plates` reads it back.
4. Run `pytest` before a pull request. GitHub Actions runs the same command on every pull request and on every push to `main`.
5. Render deploys `main` automatically. That deploy is the development deploy.
6. Production deploy is manual. Run the `production` workflow, then deploy that same commit from the Render dashboard with Manual Deploy.
7. `GET /ops` shows trace id, path, status, and duration. It does not show the card text.
8. When `saved_plate_unavailable` is active, run `python custom-agent/agent.py`.
