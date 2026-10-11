# Fault Plate

Fault Plate stores one specification card for one API failure.

When an API fails, the sentence a caller reads and the record the server keeps can drift apart. This app fixes those decisions on one card. Saving the card finishes that failure's specification.

The screen has one card. The fields are name, user-facing message, HTTP status, log fields, and whether a retry is allowed.

## Connection to another project

This app stores the specification. To show that card when a payment fails, the project where the payment happens has to read the saved card. Without that connection, the card stays in this store.

This store keeps one card. A new save replaces the previous card. Choosing among several failure types needs more than one card and a lookup by failure name.

This is not a continuation of a course app. It does not read logs to find a root cause.
