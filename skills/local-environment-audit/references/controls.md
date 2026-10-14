# Full control catalog

Version 1.0.0. Use this catalog with `SKILL.md`; no control grants permission to
perform its test. Apply a result to every control. `PASS` requires sufficient
evidence for the stated criterion, `FAIL` requires an established requirement,
and missing access or an unexecuted test must remain visible.

Implementation details and vendor references are in `sources.md`. The procedures
below are this skill's audit design, not a vendor certification standard.


## Target and authority

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `CTX-01` | Bind the executing tool to the requested host, guest, container or remote runtime. | The target relationship is supported by specific evidence; aliases alone are insufficient. | Selected target only. |
| `CTX-02` | Match browser, profile ID and live context. | Saved and live observations refer to the same identified profile. | Do not inspect other profiles. |
| `CTX-03` | Record purpose and intended time, route, persistence and function policies. | Requirements are established; unresolved preferences remain unknown. | Use existing user instructions and managed policy. |
| `CTX-04` | Record available access and action-specific authorization. | Each performed action is within scope; unavailable permissions are explicit. | No authority inferred from a tool being installed. |

## Host and software

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `HST-01` | Read OS family, release and architecture using bounded local inspection. | Readings identify the executing environment without falsely identifying the physical device. | No hardware serials, usernames or hostname required. |
| `HST-02` | Record full browser, profile-manager, kernel and relevant patch builds. | Versions describe the active installation and selected profile, not just the UA string. | Prefer existing About/version UI or selected metadata. |
| `HST-03` | Compare active builds with the applicable current vendor support channel. | Support and update conclusions are supported by current official documentation. | No update installation during a read-only audit. |
| `HST-04` | Review install provenance and managed/security settings relevant to the browser. | The source and applicable controls are known and align with the approved policy. | No whole-system forensic inventory or certificate private-key access. |

## Time

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `TIM-01` | Inspect host time and synchronization configuration; distinguish state from measured accuracy. | The stated clock policy is met; synchronization enabled alone does not prove accuracy. | External time measurement needs approved network scope. |
| `TIM-02` | Compare host timezone, saved profile timezone, launch override and live Intl/Date output. | The responsible layer and returned timezone implement the established time policy. | An IP/device timezone difference alone is not a defect. |
| `TIM-03` | Check timezone name and signed offset for the same instant; account for seasonal rules. | Offsets are explainable under the named zone and timestamp, including fractional-hour zones. | No permanent offset inferred from a single seasonal sample. |

## Profile and launch

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `PRF-01` | Confirm the selected data directory/profile persistence policy. | Work and test state boundaries match the declared purpose. | Do not copy authenticated profiles or credential stores. |
| `PRF-02` | Inspect relevant OS, manager, policy, extension and launch overrides. | Each material override has an identified source; unexplained conflicts are recorded. | Allowlist launch fields before output; do not dump full arguments. |
| `PRF-03` | Compare saved selections with active process and page readings. | Current observations implement the intended saved state or a documented exception. | A fresh launch requires separate lifecycle approval. |

## Network

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `NET-01` | Record proxy type, redacted endpoint, configuration layer and authentication mechanism. | The configured mechanism is supported by the actual browser implementation. | Never read or print the proxy password; record presence/mechanism only. |
| `NET-02` | Observe an approved fresh exit-IP request from the target browser context. | The tested request follows the intended route; destination, time and IP family are recorded. | External request authorization; terminal results are separate evidence. |
| `NET-03` | Inspect relevant VPN/tunnel, PAC, bypass and split-routing configuration. | Effective routing rules match the network policy and explain exceptions. | Do not fetch unknown PAC URLs or expose internal domain lists. |
| `NET-04` | Assess DNS configuration and, when approved, resolution behavior on the tested route. | Observed name resolution follows the policy within the documented test scope. | No DNS-leak verdict from an IP-only check. |
| `NET-05` | Inspect and separately test relevant IPv4 and IPv6 behavior. | Each applicable address family follows the route policy or has an explained unavailable state. | Do not disable IPv6 merely to improve a checker result. |
| `NET-06` | Inspect WebRTC/UDP policy and test required behavior when authorized. | Approved tests support both the stated exposure policy and required real-time functions. | No STUN calls, ICE collection or permission prompts by default. |
| `NET-07` | Test loss of proxy connectivity in an explicitly approved disposable signed-out context. | Failure behavior matches the declared policy, including fail-closed when required. | Never interrupt an active work session for this test without approval. |
| `NET-08` | Inspect HTTPS/certificate-validation settings and relevant connection failures. | Required connections use the approved trust model without unapproved validation bypass. | No private-key reads, certificate installation or packet capture by default. |

## Browser identity

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `IDN-01` | Compare UA/platform/Client Hints with selected build and intended environment. | Differences are explained by the baseline and implementation; contradictions remain review items. | Do not fabricate a replacement identity. |
| `IDN-02` | Compare allowlisted request identity headers with page-visible values when authorized. | Differences are evaluated with context, privacy reduction and hint availability accounted for. | No full HAR, Cookie, Authorization, Referer or response-body export. |
| `IDN-03` | Review language order, formatting locale and applicable language headers. | Actual language behavior matches intended preferences and is explained across layers. | Language is not required to match an exit-IP country. |

## Display and graphics

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `DSP-01` | Record screen and viewport CSS dimensions, pixel ratio, color depth, zoom conditions and attached-display context. | Readings are explainable under the display setup and measurement conditions. | Do not set a conventional resolution purely for appearance. |
| `DSP-02` | Inspect available renderer metadata and custom WebGL/WebGPU overrides. | Graphics behavior follows the baseline and required functions operate; unknown metadata stays unknown. | Optional graphics probe only; no synthetic identity editing. |
| `DSP-03` | Interpret logical CPU availability and approximate memory readings. | No failure is inferred merely from disagreement with a physical specification. | Do not run benchmarks or enumerate unrelated hardware. |

## Privacy and location

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `PRV-01` | Review startup regeneration separately from long-lived privacy/noise settings. | Behavior matches the chosen persistence policy; unintended regeneration is identified. | Record a recommendation separately from an executed edit. |
| `PRV-02` | Review intended Canvas, fonts, audio, media, rects, voices and related privacy controls. | Privacy mechanisms and required features are compatible with the stated use. | No raw fingerprint bundle or media-device enumeration by default. |
| `PRV-03` | Inspect location policy and existing grants for the selected sites. | Location access follows the user-approved permission policy. | Do not request actual coordinates or trigger a new permission prompt. |
| `PRV-04` | Check that diagnostic pages and sample origins are approved and consistently identified. | Origin- or context-dependent observations are not generalized beyond the tested context. | No upload of full diagnostic results to third parties. |

## Storage and synchronization

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `DAT-01` | Inspect cookie/site-data retention settings and clear-on-exit policy. | Retention configuration matches the declared session policy. | Do not read stored cookie values, localStorage contents or account databases. |
| `DAT-02` | Review synchronization categories, destinations and access boundaries. | Data synchronization is intentional and appropriate to the profile purpose. | No export of live sessions or wholesale profile backups. |
| `DAT-03` | When authorized, test persistence using a disposable non-sensitive marker in a dedicated test origin. | The benign marker persists or expires as required; test state is tracked and cleaned up as approved. | This writes test state and requires separate permission; a cookie-enabled flag is insufficient. |

## Permissions and exposure

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `SEC-01` | Inventory relevant extensions and their effective site access. | Every extension and broad permission has an approved purpose. | No extension disabling or removal in read-only mode. |
| `SEC-02` | Review required camera, microphone, clipboard, files, local network and device permissions. | Effective grants are no broader than the declared work requirements. | Do not prompt for or exercise powerful permissions by default. |
| `SEC-03` | Inspect relevant existing debugging, automation and local API exposure. | Approved interfaces have appropriate binding/access and are separated from sensitive work sessions. | No enabling debugging, opening ports or scanning networks by default. |
| `SEC-04` | Review relevant browser security controls and any explicit bypasses. | Active settings meet the approved security baseline; deviations have documented authority. | Do not disable sandboxing, safe-browsing, TLS checks or site isolation. |
| `SEC-05` | Check collection and output handling for secrets and unnecessary identifiers. | Reports contain only necessary sanitized facts and evidence references. | Sensitive values must be excluded before tool responses reach the agent. |

## Stability and function

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `STB-01` | Repeat a minimal probe within the same authorized context. | Differences are explained using context, timestamp, display conditions and privacy behavior. | No settings changes or page navigation implied. |
| `STB-02` | Compare an initial launch and two approved relaunches under recorded conditions. | Persistent-profile behavior matches the baseline; changes are classified, not merely counted. | Specific lifecycle approval; otherwise BLOCKED. |
| `STB-03` | Test only required workflows with benign inputs and approved actions. | Required functions operate under the chosen network/privacy configuration. | Uploads, paid calls, messages, account logins and service actions need appropriate authorization. |

## Reporting

| ID | Procedure | Acceptance criterion | Boundary |
|---|---|---|---|
| `RPT-01` | Link every local finding to dated, target-bound evidence. | Documentation supports interpretation and observations support local-state claims. | Preserve source category and original observation window. |
| `RPT-02` | Produce the full register, coverage, limitations, and proposed changes. | Every catalog control has an outcome; untested checks are visible and do not pass. | Do not invent trust scores or service-account predictions. |
| `RPT-03` | Separate observation actions, proposed changes, actual changes and verification. | The report accurately describes all actions and uses before/after evidence for verified remediation. | Saving a setting alone does not establish a verified fix. |
