# Progressive rollout gates

Use repository-specific metrics when they already exist. Otherwise keep the gate small and observable.

## Required evidence

- Candidate identity matches the pinned release and expected slot.
- Registry capacity is available before the build starts; active, candidate, and rollback artifacts are protected from retention cleanup.
- Dependency health, database identity, migration compatibility, and governance checks pass.
- Candidate produces no unexpected writes or external side effects while fenced.
- Deterministic synthetic probes have zero failures.
- Candidate 5xx and latency remain within the release's declared threshold relative to active.
- The required candidate sample is reached. Low traffic may be supplemented with safe synthetic requests; do not pass an empty sample by waiting for the clock.

## Default decision table

| Condition | Decision |
| --- | --- |
| Evidence passes before the ceiling | Advance immediately |
| Health, integrity, governance, write-fence, or synthetic probe fails | Roll back immediately |
| Sample cannot be obtained safely | Restore active-only and stop |
| Provider or cancellation state is uncertain | Stop; do not start a second route |
| Failure occurs after the new writer accepts writes | Disable feature or use the existing serialized rollback/forward-fix path |

Record every transition and its evidence in the release receipt. Never store routing tokens, credentials, customer payloads, or other secrets in logs or receipts.
