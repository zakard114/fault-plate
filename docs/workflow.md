# Workflow

One failure, one card, one save.

1. Write the five fields in `docs/product-spec.md` before changing the screen.
2. Keep the screen on `GET /`. Save stays on that screen.
3. `POST /plates` stores one row. `GET /plates` reads it back.
4. Pull requests run `pytest` only.
5. A push to `main` runs `pytest` and then the dev deploy (Render auto-deploy of `main`, or the deploy hook if `RENDER_DEPLOY_HOOK_URL` is set).
6. Production never runs on push. A person must start the production workflow (`.github/workflows/production.yml`), which runs `pytest` again and deploys only when `RENDER_PRODUCTION_DEPLOY_HOOK_URL` is set. Otherwise it stops after tests and tells the person to use Render Manual Deploy.
7. `GET /ops` shows trace id, path, status, and duration. It does not show the card text.
8. A 404 from `GET /plates` opens `saved_plate_unavailable`. The on-call agent wakes on that alert and restores the runbook card.
