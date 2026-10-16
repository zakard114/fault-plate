# Product spec

## Problem

When an API fails, the sentence the caller reads and the record the server keeps can drift apart. Fault Plate stores both decisions on one card.

## Acceptance criteria

- The screen has one card and five fields: name, user-facing message, HTTP status, log fields, retry allowed.
- Save stays on that screen and shows the stored card.
- `POST /plates` returns 201 with the same five fields.
- `retry_allowed` is `retryable` or `not_retryable`. Any other value returns 422.
- `GET /plates` returns the one stored card, or 404 when the store is empty.
- A new save replaces the previous card.
- The app does not read logs to find a root cause, and it does not add a list, a login, or a second product page.

## Tracker

The public task tracker is the GitHub Issues [FP-1](https://github.com/zakard114/fault-plate/issues/1), [FP-2](https://github.com/zakard114/fault-plate/issues/2), and [FP-3](https://github.com/zakard114/fault-plate/issues/3). [`docs/tracker.md`](tracker.md) lists the same acceptance criteria and the tests that satisfy them. The builder used those issues while adding the tests: comments cite `tests/test_plates.py`, `tests/test_oncall.py`, and commit `4402ed8`.
