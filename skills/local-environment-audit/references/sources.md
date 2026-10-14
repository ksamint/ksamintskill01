# Primary-source register

Reference pages checked on 2026-10-01. Recheck current vendor documentation when a
subsequent audit depends on behavior, compatibility, supported builds, or a UI
label that may have changed. This date is not a claim that a local installation
was inspected or that these pages are immutable.

## S01 — Agent Skills specification

https://agentskills.io/specification

Use: Package format, frontmatter, names and progressive disclosure.

## S02 — AdsPower browser fingerprint settings

https://help.adspower.com/docs/browser_fingerprint

Use: Timezone choices and vendor descriptions of profile settings. Product claims require local verification.

## S03 — AdsPower profile creation

https://help.adspower.com/docs/creating_browser_profiles

Use: Startup-randomization settings and logged configuration changes.

## S04 — MDN: Date.getTimezoneOffset

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset

Use: Offset sign and date-dependent timezone behavior.

## S05 — MaxMind: Geolocation accuracy

https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy

Use: Limits of IP geolocation, including proxy locations.

## S06 — Chrome: User-Agent Client Hints

https://developer.chrome.com/docs/privacy-security/user-agent-client-hints

Use: Browser identity hints and privacy-aware interpretation.

## S07 — MDN: hardwareConcurrency

https://developer.mozilla.org/en-US/docs/Web/API/Navigator/hardwareConcurrency

Use: Available logical processors, not a precise physical inventory.

## S08 — MDN: deviceMemory

https://developer.mozilla.org/en-US/docs/Web/API/Navigator/deviceMemory

Use: Approximate memory and implementation-dependent privacy limits.

## S09 — MDN: Screen.width

https://developer.mozilla.org/en-US/docs/Web/API/Screen/width

Use: Screen width is expressed in CSS pixels.

## S10 — MDN: WEBGL_debug_renderer_info

https://developer.mozilla.org/en-US/docs/Web/API/WEBGL_debug_renderer_info

Use: Renderer metadata availability and privacy restrictions.

## S11 — Chromium: Proxy support in Chrome

https://chromium.googlesource.com/chromium/src/+/HEAD/net/docs/proxy.md

Use: Browser-specific proxy behavior, authentication, bypass rules and transport limits.

## S12 — Chrome: Remote debugging security changes

https://developer.chrome.com/blog/remote-debugging-port

Use: Risks of debugging access and separation from real user profiles.

## S13 — AdsPower: Edit Profile

https://help.adspower.com/docs/editing

Use: Profile editing prerequisites and version/update controls.

## Source handling rules

Use implementation-specific official documentation for version-dependent rules.
Record the document title, URL, access date, and relevant version. A browser fork
can differ from upstream Chromium. Vendor marketing claims about invisibility,
leak prevention or account safety are not substitutes for local measurements.

Technical sources explain interfaces; supplied screenshots and measurements
establish what was observed in a particular context. Keep those evidence roles
separate. No listed source supports a numerical account-reinstatement estimate.
