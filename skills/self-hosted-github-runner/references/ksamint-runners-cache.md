# ksamint: organization runners and warm builds

## ksamint policy and verified snapshot, 2026-09-20

- The user moved repositories to `https://github.com/ksamint/` and authorized the shared organization pool for all current and future repositories, public and private. Skill source: `ksamint/ksamintskill01`; Promese01: `ksamint/promese01`.
- GitHub API readback: group `Default` (id `1`), `visibility: all`, `allows_public_repositories: true`, `restricted_to_workflows: false`. Both `VM-0-2-debian-ci-ephemeral` and `VM-0-9-debian-ci-ephemeral` were online organization runners.
- Shared labels: `self-hosted`, `Linux`, `X64`, `apuch-ci`, `us`, `ci-ephemeral`, `publish`, `na-siliconvalley`. Re-read current labels and policy before use; this snapshot is not a health guarantee.
- Both hosts are 2 vCPU / 8 GB, but VM-0-2 exposes AMD EPYC 9754 and VM-0-9 Intel Xeon E5 v4. They are not equivalent performance baselines. The cx01 incident showed slower timings on VM-0-9; sampled CPU steal and service quota throttling were zero, not proof of historical absence. Measure the same workload before changing routing or capacity; retain performance gates.
- Both hosts received checksum-verified `gh 2.101.0`; `jq`, `rclone` and `openssl` were verified. Debian's `gh 2.23.0` lacked the publish workflow's `--commit`, `--event` and `--status` flags. Verify required commands as the job user, not only root, and include them in replacement-host provisioning.

Keep controller/admin credentials outside job environments. "Maximum access" here means the authorized repository scheduling scope, not `write-all`, organization-admin tokens, unrestricted sudo or every production secret in every job. Public-repository access requires special care with untrusted PRs, as [GitHub warns](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access). An ephemeral registration plus home/work-directory cleanup is not proof of a disposable isolated machine. Inspect execution isolation before sending untrusted code to this pool.

### Reuse the pool

Read `gh api orgs/ksamint/actions/runner-groups` and `gh api orgs/ksamint/actions/runners` first. Existing group access covers future repositories without per-repo runner registration; workflows still need matching `runs-on` selectors and their own runtime/secrets configuration. Preserve a project's established GitHub-hosted route unless a change is requested.

For workflows already using `PR_RUNNER_LABELS` and `PUBLISH_RUNNER_LABELS`, the cx01 repository values are `["self-hosted","linux","x64","ci-ephemeral","na-siliconvalley"]`. Those variable names are a workflow convention, not automatic GitHub settings or evidence that organization variables exist. Audit repo overrides before introducing org defaults. Do not silently fall back to hosted execution for a self-hosted-only project.

Runner location and object-store location are independent: the US pool uses `na-siliconvalley`; cx01's COS handoff can still use `ap-singapore`. Do not change COS endpoints when fixing runner selectors. Jobs already evaluated with old selectors may keep them; reconcile the exact run and safely replace stale queued work rather than promising a variable edit retargets it.

Inspect the actual owner, controller and builder storage before implementation. Finish or reconcile an active exact-SHA release before infrastructure changes; never bypass a failed gate. Host/controller/tool persistence can coexist with disposable job environments and allowlisted caches; neither cache persistence nor isolation has been proven by this snapshot.

## Organization pool, not one registration per repository

Only if live inspection shows a missing or repo-scoped worker and migration is authorized:

1. Inspect `ksamint` Settings / Actions / Runners and Runner groups, group availability, repository access, current labels and controller credentials. Use an organization pool for eligible repositories rather than duplicating repository registrations.
2. Register replacements against `https://github.com/ksamint`, obtaining registration tokens from `POST /orgs/ksamint/actions/runners/registration-token`. Select an existing authorized group and role/OS/architecture labels; update workflows to target that group and matching labels. A repository transfer does not migrate its runner controller automatically.
3. Preserve ksamint's explicitly authorized all-repository policy. For another organization without that authorization, start with selected repositories. Separate untrusted PR workers from trusted build/release workers; labels and group membership alone do not isolate credentials or a Docker socket.
4. Drain active jobs, migrate one worker, test authorized repositories and verify exclusion of unauthorized ones, then migrate the second. Keep controller rollback available. Ephemeral workers must still deregister, clean the job environment and register replacements.

Check endpoint-specific permissions before requesting credentials. Organization registration supports a GitHub App or fine-grained token with organization `Self-hosted runners: write`; classic/OAuth tokens require `admin:org` and, for private repositories, `repo`. Ordinary repository `GITHUB_TOKEN` is not an organization administration credential. Group management has its own permission requirements. Keep controller credentials out of jobs; request missing authority rather than broadening access silently. [GitHub runner API](https://docs.github.com/en/rest/actions/self-hosted-runners#create-a-registration-token-for-an-organization), [group access](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access).

## Fix cold builds independently

Organization scope does not itself cause or cure cold builds. Inspect the builder driver, daemon lifetime, volume mounts and cleanup commands. An ephemeral runner registration is compatible with persistent cache; a throwaway nested Docker daemon loses its volumes unless its storage is retained deliberately.

- On a persistent host, retain a dedicated BuildKit state volume outside the disposable runner/workspace. With the `docker-container` driver, use a stable builder identity; if recreating that builder, `docker buildx rm --keep-state` preserves its state for recreation under the same name. Confirm the host Docker storage itself survives. [Docker persistence](https://docs.docker.com/build/builders/drivers/docker-container/#cache-persistence).
- Each of the two hosts has its own local volume. When scheduling across hosts causes cache misses, use an authorized private registry cache via `--cache-from type=registry,ref=<cache-ref>` and `--cache-to type=registry,ref=<cache-ref>,mode=max`. Keep the cache reference separate from the output image; confirm driver support and registry permissions. [Registry cache](https://docs.docker.com/build/cache/backends/registry/).
- Namespace builders/cache refs by repository, image target, platform and trust scope. Isolate concurrent writers with separate refs or serialization. Share only explicitly trusted inputs; PR jobs must not overwrite release caches. Never mount one raw BuildKit state directory into two active daemons.
- Keep dependency layers stable: copy lockfiles before changing application source, use locked installs, exclude irrelevant context and use suitable package cache mounts. Keep secret material in BuildKit secret mounts, not copied files or build arguments. [Cache optimization](https://docs.docker.com/build/cache/optimize/).
- Cleanup must remove job files, credentials and disposable execution state, while retaining only the allowlisted cache volumes. Avoid global volume/system pruning. Set cache size/age limits, garbage collection and disk headroom; never retain production secrets or treat caches as rollback artifacts.

## Acceptance before claiming speedup

Record cold and warm phase timings, cache hits, builder identity, storage usage and source SHA with identical pinned inputs. After job cleanup and runner re-registration, rebuild on the same host; test the second host separately and external cache import if configured. Report cache export/import overhead as well as build time. No fixed speedup is promised.

Verify a cold-cache build still works, a changed lockfile invalidates the correct layers, and untrusted jobs cannot read/write protected cache or credentials. Prefer deploying the tested immutable image by digest, not rebuilding it in production. Maintain host-wide CPU/RAM limits in addition to repository-level workflow concurrency.
