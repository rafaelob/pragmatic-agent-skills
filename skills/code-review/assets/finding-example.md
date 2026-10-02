# Optional finding shape

Use only where a substantive finding benefits from structure. No minimum number of findings.

**Location and contract:** The response mapping used by the public count consumer.
**Failure scenario:** A backend timeout is mapped to `count=0` and success.
**Impact:** The consumer mistakes unavailable data for a completed empty query.
**Evidence:** Changed path and the existing failed-lookup test, or explicitly unverified reasoning.
**Small correction / useful check:** Preserve the unavailable state and exercise the consumer with the same empty payload under success and failure.

A suggestion to rename a private helper with no behavioral impact is optional, not a release blocker.
