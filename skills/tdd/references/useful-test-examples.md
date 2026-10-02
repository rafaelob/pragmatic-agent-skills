# Tests that distinguish right from wrong

Examples are original review guidance, not a claim about tests currently present in a product.

| Situation | Useful check | Avoid by default |
|---|---|---|
| Internal function extracted | Existing public behavior still holds | Freeze the private helper name or number of calls |
| Public field renamed | Real consumer sees compatible schema or deliberate version transition | Assert only the new field literal in the producer source |
| Arithmetic rule changed | Worked independent input/output and meaningful boundaries | Compute expected with the production function |
| Count query fails | Error/unavailable is not displayed as zero | Mock a zero and assert that same zero |
| Retry semantics change | Permanent failure is not retried; ambiguous effect is not duplicated | Increase retry count until the test passes |
| Local UI copy change | Render/reflow or accessible name where affected | Add a full real-backend journey with every role |
| Database constraint changes | Violation rejected by the actual database; permitted case accepted | Mock ORM validation and call that proof of the constraint |
| Generated package | Generator behavior plus the consumed artifact's schema/import when relevant | Only confirm the generator file exists |
| Resource cleanup | Acquired resource released after success and relevant failure | Assert presence of the word `finally` in source |

## Sensitivity without a new mutation platform

For a bug regression, demonstrate the known bad behavior failing where feasible. For an important test whose sensitivity is doubtful, a small intentional fault in a disposable fixture can confirm that it detects the error. A whole-repository mutation campaign is not required by this skill.

An import or exact filename test can be useful when package importability or that filename is a real external contract. A call-count assertion can be useful when duplicate side effects are prohibited. Do not replace judgment with a blanket ban on a test shape.

## Removing or merging tests

Do not delete by age, runtime cost, red status or perceived ugliness alone. Identify the protection, preserve it in an equivalent or better check, or show the behavior is retired. Consolidate meaningful parameter cases without hiding which case failed. Quarantine is an explicit uncovered obligation until another valid check replaces it or the owner changes the requirement.

Unit tests, contracts, integration and E2E can all be useful. Select the layer that owns the failure, then add another only for a distinct boundary or required gate.
