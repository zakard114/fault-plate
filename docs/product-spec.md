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

GitHub Issues on https://github.com/zakard114/fault-plate/issues are the public task tracker. One issue covers one acceptance criterion above. The builder closes an issue only after `pytest` passes for that criterion.
