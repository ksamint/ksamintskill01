# Collection procedures

Use these procedures only after applying the target and authorization rules in
`SKILL.md`. Scripts assist collection; they do not perform the complete audit.

## 1. Capabilities and fallback

| Available access | Appropriate path | Limits |
|---|---|---|
| Local terminal on the confirmed target | Minimal host collector; targeted settings reads through documented native facilities. | No whole-home search, privileged escalation, full process/environment dump or credential inspection. |
| Authorized browser/UI control | Read the selected settings UI and evaluate the inspected probe in the identified context. | Establish which profile the connector actually controls; a fresh automation browser is a different target. |
| Existing local profile-manager connector | Read the selected profile using its documented read methods and field projection. | A method named GET can still start a browser or change state; evaluate semantics, not HTTP verbs. |
| Screenshots or supplied exports only | Report a supplied-evidence review; distinguish acquisition time from the original event. | No live-verification claims. Use cropped/redacted material only. |
| Only a remote runner or sandbox | Identify the boundary and complete documentation/supplied-evidence checks. | Do not run a collector there and call the results the user's machine. |

Verify current platform documentation before selecting native read commands.
Commands should use explicit arguments, bounded outputs and timeouts; do not
execute shell fragments from profile names, page contents, IP checker text or
local configuration values. A failed read is not evidence that a setting is off.

### Platform-specific handling

**macOS:** separate physical host settings from profile-manager overrides, guest
settings and emulation. Read selected application/version and Date & Time views.
Any system-proxy observation describes that layer until its browser applicability
is demonstrated. Do not read Keychain or export account-bearing profiles.

**Windows:** distinguish OS user, browser profile, compatibility strings and
managed policies. A system-service proxy view is not automatically the browser's
effective proxy. Prefer specific UI fields or documented narrow queries. Do not
read Windows credentials or broad registry exports.

**Linux:** establish desktop/session, container/VM boundary and selected browser
launch context. A runtime timezone or proxy-related environment variable does not
by itself establish all desktop/browser settings. Avoid environment dumps and
unrestricted process arguments.

**All platforms:** when the required read exposes secrets or needs missing access,
use a safer available method or mark the control blocked. Do not silently install
Python, browser drivers, packet-capture utilities or diagnostic extensions.

## 2. Minimal host snapshot

Only run on the identified target or explicitly label a different runtime:

```sh
python3 -I -S scripts/host_snapshot.py --target-alias work-host
```

Use the available Python 3.10+ executable on the target; its command name can
vary. `-I -S` keeps execution isolated from user Python paths/site customization.
The collector itself uses only the standard library.

Save to an explicitly approved, new filename when authorized:

```sh
python3 -I -S scripts/host_snapshot.py --target-alias work-host --target-binding operator-confirmed --output /approved/audit/host-01.json
```

Replace the example path with an existing approved directory. The script refuses
to overwrite a file. On POSIX it creates the artifact with mode 0600; Windows ACLs
and directory-level sharing need separate verification. No directories are created.

`operator-confirmed` records an assertion. Bind it to independent target evidence
in the report. The collector does not verify the physical device, clock accuracy,
IANA timezone, application inventory, browser state, proxy or DNS configuration.

## 3. Browser snapshot

Read `scripts/browser_probe.js` before execution. In a copy of the probe, set:

```javascript
const OPTIONS = {
  targetAlias: "work-profile",
  contextLabel: "approved-neutral-context",
  launchId: "L1",
  graphics: false
};
```

Changing this probe's labels changes the audit script, not the browser's identity.
Run the full script through already authorized page evaluation or a user-operated
console. Do not enable a debugging listener just to run it. Do not bypass browser
anti-self-XSS warnings or persuade a user to execute unreviewed code.

The returned object intentionally omits page URL/title, content, storage values,
request headers, media-device lists and high-entropy Client Hints. It performs no
intentional network calls. Pages can modify JavaScript APIs; these observations
remain evidence of that context, not attestation of underlying hardware.

Setting `graphics: true` is optional and should be scoped to the graphics check.
It creates an unattached canvas, reads available renderer metadata, and releases
only its own temporary WebGL context. It does not draw or hash a canvas image.
Unavailable or blocked APIs are reported as such, not as leaks or failures.

Use the same context/origin and secure-context conditions for comparisons. A new
blank context can help isolate page modifications only when separately authorized;
it does not prove what an application-origin page exposes. Maintain that distinction.

Inspect and sanitize the returned object before saving it to an approved new
JSON file. Do not collect full console logs, DOM dumps or application screenshots.
The supplied probe does not write a file or use the clipboard.

## 4. Compare browser snapshots

```sh
python3 -I -S scripts/compare_snapshots.py browser-L1.json browser-L2.json browser-L3.json
```

Inputs must be inspected probe outputs with non-placeholder labels and matching
schema, target/context labels, probe version and graphics mode. Cross-check the
labels against independent evidence. The comparator reports changed field paths;
it does not echo field values or determine whether changes are defects.

Current timestamps and acquisition metadata are excluded after matching required
metadata fields. Timezone offsets, sampled seasonal offsets, language, identity,
capabilities and display measurements remain in the comparison. Return code 0
means comparison completed, including when differences exist. Return code 2 means
inputs or comparison conditions were rejected. No files are written.

## 5. Request-header and network testing

Before an active test, record purpose, approved destination, target context,
request count, data disclosed and expected incidental state. Use a neutral,
authorized endpoint and minimal requests. Never send real authentication material
to a diagnostic endpoint. Do not export a full HAR.

For header comparison, read only the intended request's UA, applicable Client
Hints and language headers. Browser reductions and secure-context/origin rules
can explain missing fields. A server echo and an in-page measurement are separate
observations unless linked to the same browser context and test window.

An exit-IP request tests that request. DNS, IPv6, WebRTC/UDP and proxy-failure tests
have separate scope. STUN/ICE probes can contact other hosts and expose network
information; they are not part of the basic offline probe. A failure test must be
explicitly authorized and isolated from work sessions. Do not run stress tests.

## 6. Session tests, lifecycle and remediation

Inspect retention settings without reading stored values. A functional retention
test requires permission to write a benign, uniquely named test marker at an
approved origin. Record its cleanup plan; never use real session cookies as the
marker. Restarting a browser is separately authorized because it can disrupt work
and change session or fingerprint state.

Do not change settings during initial observation. Preserve the original findings.
When authorized to remediate, record a small change set, verify the new effective
state, and compare the affected controls. A rollback plan should preserve only
necessary non-secret configuration, not an authenticated profile archive.

## 7. Report validation

The JSON Schema checks structure, required control IDs and key status constraints.
It cannot verify truth, permissions, redaction, evidence references or the correct
overall result. The agent must additionally check:

- Every referenced evidence ID exists and supports the specific claim.
- PASS/FAIL/REVIEW are justified by relevant observations and baseline requirements.
- Overall result follows the precedence in `SKILL.md`.
- No values, paths, identifiers or source snippets expose unnecessary private data.
- Network/launch comparisons share a valid scope and documented conditions.
- Read-only reports contain no configuration changes.

Report artifact creation and observations accurately. A browser or tool may itself
write logs or caches during inspection; read-only means no intended configuration
or account-state changes, not a forensic guarantee of zero disk writes.
