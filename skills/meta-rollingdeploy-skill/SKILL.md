---
name: meta-rollingdeploy-skill
description: Plan, execute, or audit evidence-driven progressive production releases using an existing immutable A/B or rolling substrate, including safe shadow traffic, directed and weighted canaries, single-writer cutover, feature exposure, and fast rollback. Use for large or high-risk releases; do not use for ordinary local development or as a reason to introduce Kubernetes.
---

# Progressive production rollout

Keep the repository's existing release module. Add only the smallest routing and evidence seams needed for progressive delivery; do not build a parallel deploy system.

## Before production mutation

1. Establish the real topology: immutable artifact path, proxy/provider, active and candidate instances, stateful dependencies, write owners, health/governance probes, rollback command, and release lock.
2. Classify every persistence system as single-writer or multi-writer. A single-writer service may receive candidate reads, but every write and side effect stays on the active writer until the commit point.
3. Use `github-fast-deploy` to select the existing GitHub Actions or local/provider route. Pin the remote default branch's exact SHA, reuse exact-tree evidence, and never race two deploy routes.
4. Check artifact-registry capacity and retention before building. Protect images referenced by active, candidate, and rollback receipts; prune only exact unreferenced tags whose source can be rebuilt, or use a reviewed lifecycle policy.
5. Require explicit authorization for the target environment. Authorization for one SHA and environment does not authorize another.

## Progressive sequence

Use repository-native capabilities in this order when supported:

1. Build and verify one immutable artifact.
2. Acquire release-wide exclusivity.
3. Warm the candidate with writes, background jobs, uploads, messaging, and external side effects disabled.
4. Mirror only demonstrably safe reads; discard candidate responses and never mirror request bodies unless the route is proven body-free.
5. Route a trusted operator or synthetic governance project to the candidate. A routing hint is not authorization; the application must still authenticate and authorize normally.
6. Shift safe reads through the repository's configured ladder. Default: directed → 5% → 25% → 100%.
7. At the single-writer commit point, fence and flush the old writer, reconcile state, switch atomically, prove the new instance in read-only mode, then enable it as the sole writer.
8. Activate newly deployed functionality independently through existing project/organization feature controls. Code deployment may finish while a feature remains dark.

Do not mirror uploads, database mutations, jobs, SMS/email, payments, webhooks, or other external side effects. Do not add automatic write failover to a single-writer system.

## Evidence and rollback

Read [references/gates.md](references/gates.md) when defining stage gates, time ceilings, or rollback behaviour.

- Poll evidence every 1–5 seconds and advance immediately when it passes. A timeout is a ceiling, not a mandatory observation period.
- After the artifact exists, default to 60 seconds per stage and five minutes total convergence. Extend only for work still producing evidence, such as a real migration.
- Before the write commit, any breach restores active-only routing and discards the candidate.
- After the write commit, disable the affected feature first when possible; otherwise use the repository's existing single-writer rollback or forward-fix procedure. Never start a competing deploy.
- Finish with exact SHA and artifact identity, stage samples and durations, health/governance results, final writer, feature exposure, and whether rollback occurred.
