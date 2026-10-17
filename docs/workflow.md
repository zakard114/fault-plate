# Workflow

One failure, one card, one save.

1. Write the five fields in `docs/product-spec.md` before changing the screen.
2. Keep the screen on `GET /`. Save stays on that screen.
3. `POST /plates` stores one row. `GET /plates` reads it back. If that read stalls in PowerShell, follow Warnings in the README.
4. Pull requests run `pytest` only.
5. A push to `main` runs `pytest`, then the `deploy-dev` job records a GitHub deployment with environment name `dev`. That record is the dev deploy. Render auto-deploy of `main` remains the dev host https://fault-plate.onrender.com. If `RENDER_DEPLOY_HOOK_URL` is set, the job POSTs the hook. If it is not set, the job still succeeds.
6. Production never runs on push. A person must start `.github/workflows/production.yml` (`workflow_dispatch` only). It runs `pytest`, then records a GitHub deployment with environment name `production`. If `RENDER_PRODUCTION_DEPLOY_HOOK_URL` is set, it POSTs that hook after the tests. If it is not set, the job still succeeds as the manual production deployment record, and the step log says production was recorded and the live Render service is unchanged until a production hook is added. There is no second public URL.
7. `GET /ops` shows trace id, path, status, and duration. It does not show the card text.
8. A 404 from `GET /plates` opens `saved_plate_unavailable`. The on-call agent wakes on that alert and restores the runbook card.
