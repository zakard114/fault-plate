# Workflow

One failure, one card, one save.

1. Write the five fields in `docs/product-spec.md` before changing the screen.
2. Keep the screen on `GET /`. Save stays on that screen.
3. `POST /plates` stores one row. `GET /plates` reads it back.
4. Run `pytest` before a pull request. GitHub Actions runs the same command on every pull request and on every push to `main`.
5. After tests pass on `main`, the `deploy-dev` job deploys the dev service. Render auto-deploy of `main` is that dev deploy until a deploy hook is set.
6. Production does not deploy on push. A person runs the `production` workflow, the tests pass, and that run is the only production deploy.
7. `GET /ops` shows trace id, path, status, and duration. It does not show the card text.
8. A 404 from `GET /plates` opens `saved_plate_unavailable`. The on-call agent wakes on that alert and restores the runbook card.
