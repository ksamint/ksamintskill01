# Local Environment Audit Report

**Audit ID:** [ID]\
**Mode:** [read-only / remediate-authorized]\
**Observation window:** [timestamps and timezone; clock-accuracy status]\
**Overall result:** [action-required / incomplete / review-required / meets-baseline-for-tested-scope]

## Executive assessment

[State the most consequential supported findings, affected functions and necessary
actions. Keep configuration conclusions separate from third-party account issues.]

## Target, baseline and authorization

| Item | Established value | Evidence / limitation |
|---|---|---|
| Executing environment and relationship to requested device | [value] | [E-ID] |
| Selected browser and profile | [value] | [E-ID] |
| Intended purpose and baseline | [value] | [E-ID] |
| Time, network and persistence policies | [value] | [E-ID] |
| Required workflows | [value] | [E-ID] |
| Permitted reads, network tests, lifecycle actions and changes | [value] | [E-ID] |

## Control register

Expand every control from `assets/control-catalog.json` into this table. No control
may disappear because it was blocked, untested or not applicable.

| Control | Expected state | Saved / live observation | Outcome | Severity | Confidence | Evidence | Next action |
|---|---|---|---|---|---|---|---|

## Saved-versus-effective discrepancies

| Setting | Intended | Saved | Effective / live | Responsible layer | Evidence |
|---|---|---|---|---|---|

## Network tests

| Test | Authorized scope | Context / destination / time | Protocol / IP family | Observation | Limits |
|---|---|---|---|---|---|

## Repeatability

| Field | Conditions | First sample | Repeat / relaunch samples | Expected / defect / unresolved | Evidence |
|---|---|---|---|---|---|

## Proposed remediation

| Priority | Target / exact setting | Current → intended | Benefit and prerequisites | Disruption | Approval | Validation | Rollback |
|---|---|---|---|---|---|---|---|

## Actions actually performed

[Distinguish observation, new contexts, requests, artifact writes and authorized
configuration changes. List actual before/after evidence for any verified fix.]

## Limitations and outstanding checks

[State access constraints, uncertain baseline decisions, source dates and tests
not run. Do not characterize missing measurements as passes.]

## Evidence register

| Evidence ID | Source category | Target / context | Acquisition / event time | Method and sanitized value | Limitations |
|---|---|---|---|---|---|

## Sources and information handling

[List relevant official references with access date; document redaction and any
retained non-sensitive artifact locations. Do not attach credential-bearing data.]
