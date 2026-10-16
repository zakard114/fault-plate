# Task tracker

Public tracker for this repository. One task, one acceptance criterion. The builder marks a task done only after the named test passes.

| ID | Task | Acceptance criterion | Evidence |
|----|------|----------------------|----------|
| FP-1 | Save and read one plate | `POST /plates` with the five fields returns 201, and `GET /plates` returns the same five fields. | `tests/test_plates.py` `test_save_five_fields` |
| FP-2 | Reject an unknown retry value | `retry_allowed` other than `retryable` or `not_retryable` returns 422. | `tests/test_plates.py` `test_reject_bad_retry` |
| FP-3 | Wake on a missing plate | `GET /plates` returning 404 opens `saved_plate_unavailable`. The on-call agent then restores the runbook card, and the next `GET /plates` returns 200. | `tests/test_oncall.py` `test_oncall_wakes_when_the_plate_is_missing` |

The builder agent used FP-1 and FP-2 when the API tests were added, and FP-3 when the on-call wake was added. GitHub Issues, when opened, use these same IDs and acceptance criteria.
