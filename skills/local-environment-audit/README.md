# local-environment-audit

A portable, evidence-based skill for auditing host/browser/network configuration.
The package uses the Agent Skills directory format. Its instructions can also be
read by an agent without native skill discovery; actual access depends on that
agent's tools and the user's authorization.

## Use

Place the complete `local-environment-audit` directory in the skill location
supported by your agent. Consult that agent's current documentation for the
installation path; there is no single universal path. Keep the directory name
consistent with the `name` in `SKILL.md`.

For an agent without skill discovery, supply `SKILL.md` and the referenced files
and ask it to follow the skill. The Markdown core can be read on its own, but the
complete package is needed for its control catalog, report schema and collectors.

Suggested invocation:

> Use local-environment-audit to inspect my selected local browser/profile and
> relevant host/network settings. Work read-only. Establish the actual target and
> intended baseline, compare saved settings with live readings, and return the
> complete evidence-backed report. Do not restart profiles, change configuration,
> read credentials or contact external diagnostics without authorization.

## Package

- `SKILL.md`: operating contract, workflow, interpretation and report requirements.
- `references/controls.md`: complete 46-control register.
- `references/collection.md`: capability-aware collection and test procedures.
- `references/sources.md`: primary technical sources and freshness rules.
- `references/examples.md`: worked decisions for common ambiguous readings.
- `scripts/host_snapshot.py`: minimal offline observations of the executing runtime.
- `scripts/browser_probe.js`: allowlisted in-context observations; graphics opt-in.
- `scripts/compare_snapshots.py`: offline changed-field comparison without verdicts.
- `assets/control-catalog.json`: machine-readable control definitions.
- `assets/report-template.md`: human-readable report structure.
- `assets/report-template.json`: full unexecuted control register.
- `assets/report.schema.json`: structural validation contract.
- `tests/test_collectors.py` and `tests/test_browser_probe.cjs`: offline tests.
- `VALIDATION.md`: what was tested in the authoring environment.

## Dependencies and boundaries

The instructions are tool-neutral. Optional Python scripts require Python 3.10+
and use only the standard library. The browser probe uses an authorized existing
browser execution context. The JavaScript tests need Node.js; tests do not imply
Node.js is required on the audited device.

No script installs tools, contacts external services or edits browser settings.
The host collector prints JSON by default; its explicit output option creates a
new artifact without overwriting. The comparator reads supplied snapshots and
prints changed paths. Only the optional graphics probe creates and releases a
temporary WebGL context. Scripts do not prove target binding, physical hardware,
clock accuracy, complete routing, account eligibility or absence of compromise.

Do not run scripts on a remote runner and represent the result as the user's Mac
or PC. Inspect script sources and confirm execution permissions before use. A
user-label such as `operator-confirmed` is an assertion requiring separate evidence.

## Example offline commands

Run from the skill directory, using the actual Python 3.10+ executable available:

```sh
python3 -I -S scripts/host_snapshot.py --target-alias work-host
python3 -I -S scripts/compare_snapshots.py browser-L1.json browser-L2.json
python3 -I -S tests/test_collectors.py
node tests/test_browser_probe.cjs
```

Browser snapshot filenames are inputs produced during an authorized audit; they
are not included sample measurements of your device. Edit only the probe's
operator labels and optional graphics flag in a scratch copy before evaluation.

## Report semantics

Outcomes: PASS, FAIL, REVIEW, BLOCKED, NOT_TESTED, NOT_APPLICABLE. An incomplete
check is never silently counted as a pass. Overall results describe the tested
configuration scope, not a third-party service's trust or account decisions.

A report can be fully documented while access or authorization leaves some tests
incomplete. Proposed fixes remain separate from performed changes.
