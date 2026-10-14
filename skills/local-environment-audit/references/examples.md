# Classification examples

These are illustrative decisions, not observations of any user's current device.
Use the exact control criterion and available evidence in each actual audit.

## Unintended timezone override

Supplied material describes a host at UTC+8 and a browser custom setting at
`Etc/GMT+12`, with the live page returning UTC-12. This establishes the reported
override relationship when the observations refer to the same target and window.
With no intended time policy, classify the mismatch as REVIEW. Once the user
establishes that the custom setting is accidental and the profile should follow
the host, the configuration contradicts that requirement: TIM-02 can FAIL.
The source remains user-supplied until independently inspected. It does not
establish an account-restriction cause.

## Intentional proxy and host timezone difference

A host-based time policy is established. The browser returns the host's named
zone and the correct date-specific offset, while an exit-IP lookup suggests a
different zone. The timezone control may PASS for the observed scope. The network
and geolocation observations still require their own assessment. A different
IP-associated zone does not invalidate an intentional host-based policy.

## Custom graphics metadata

A customized desktop profile returns a mobile-associated GPU string. Treat it as
REVIEW until the declared emulation baseline and actual override source explain
it. Do not call the hardware impossible, claim compromise, or manufacture a new
renderer string. If a native-profile baseline prohibits custom renderer metadata,
an observed override can separately fail that configuration requirement.

## Browser resources

A page reports four logical processors, approximate memory of 8 GiB and a
1512-by-982 CSS-pixel screen. These readings alone do not demonstrate a defect.
Interpret the APIs, privacy behavior and display conditions. A claimed inventory
of the physical hardware would need different evidence.

## Startup regeneration

A persistent-work-profile requirement explicitly excludes deliberate identity
regeneration at every launch, and the matching saved profile has that feature
on. PRV-01 can FAIL based on the requirement and settings. The agent may recommend
a change but does not execute it in a read-only audit. Without restart approval,
STB-02 remains BLOCKED even though the saved-setting contradiction is established.

## Browser-probe-only collection

An offline JavaScript snapshot shows `RTCPeerConnection` is present and
`cookieEnabled` is true. This does not test network exposure, complete WebRTC
functionality or session retention. Those controls remain NOT_TESTED, or BLOCKED
when the required action lacks authorization. Do not convert API presence into a
leak verdict or an end-to-end success claim.

## Debugging listener

A narrowly scoped inspection finds an existing debug listener bound to a broad
interface. Record the observed bind, access scope and approved baseline. A bind
alone does not establish external reachability or lack of authentication. A
loopback-only requirement, however, can be contradicted by the configuration
without probing remote systems. Preserve the boundary between observed settings,
reachability, credential exposure and inferred consequences.

## Wrong executing runtime

The agent has a Linux sandbox but the user requested a Mac profile audit. The
sandbox collector describes the sandbox only. Local Mac checks are BLOCKED
unless a target-bound connector or other authorized method is available. Existing
user screenshots may still support a clearly labeled supplied-evidence review.
