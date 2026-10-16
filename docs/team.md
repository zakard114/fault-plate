# Agent team

Four roles work on one card. They do not share one chat.

| Role | Reads | Does | Does not |
|------|-------|------|----------|
| Spec author | The five fields | Writes the acceptance criteria for one failure | Read logs for a root cause |
| Builder | `docs/product-spec.md`, `openapi.yaml` | Implements the card, the API, and the tests | Add a second screen |
| Reviewer | `agent-capabilities/subagents/plate-reviewer.md` | Checks the five fields and reports pass or fail | Edit the app or commit |
| On-call | `GET /alerts` | If `saved_plate_unavailable` is active, posts the runbook card | Deploy or delete |

## Process

1. The spec author names the failure and the five fields.
2. The builder implements only that spec and runs `pytest`.
3. The reviewer subagent checks the result without editing files.
4. If the public `GET /plates` is 404, the alert `saved_plate_unavailable` opens.
5. The on-call agent wakes inside the service when `saved_plate_unavailable` is opened and writes the runbook card. `python custom-agent/agent.py` is the same repair if it is run by hand.
6. A person checks the diff before it is pushed.
