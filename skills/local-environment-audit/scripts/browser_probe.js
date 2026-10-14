/* Local environment probe v1.0.0.
 * Inspect this source, then evaluate it only in an authorized browser context.
 * Set the three operator labels below. Labels do not verify profile identity.
 * No deliberate network calls, storage/credential reads, permission requests,
 * DOM insertion, persistent settings writes, or console logging.
 * graphics=true temporarily creates a WebGL context; default is false.
 * Returns an object. Transfer only the inspected, redacted result.
 */
(() => {
  "use strict";
  const OPTIONS = {
    targetAlias: "UNSET",
    contextLabel: "UNSET",
    launchId: "UNSET",
    graphics: false
  };

  const read = (fn) => {
    try {
      const value = fn();
      return value === undefined
        ? { state: "unavailable", value: null }
        : { state: "observed", value };
    } catch (error) {
      const knownNames = ["SecurityError", "TypeError", "ReferenceError", "NotAllowedError", "NotSupportedError"];
      const name = knownNames.includes(error?.name) ? error.name : "Error";
      return { state: "blocked-or-error", value: null, error_type: name };
    }
  };

  const now = new Date();
  const year = now.getUTCFullYear();
  const nav = globalThis.navigator;
  const scr = globalThis.screen;
  const result = {
    _meta: {
      schema: "local-environment-browser-snapshot/1.0",
      probe_version: "1.0.0",
      captured_at: now.toISOString(),
      target_alias: OPTIONS.targetAlias,
      context_label: OPTIONS.contextLabel,
      launch_id: OPTIONS.launchId,
      target_binding_independently_verified_by_script: false,
      graphics_requested: OPTIONS.graphics,
      intentional_network_calls: false,
      persistent_configuration_changes: false
    },
    time: {
      utc_iso: now.toISOString(),
      epoch_ms: now.getTime(),
      utc_offset_minutes_east: read(() => -now.getTimezoneOffset()),
      intl: read(() => Intl.DateTimeFormat().resolvedOptions()),
      january_reference: `${year}-01-15T12:00:00.000Z`,
      january_offset_minutes_east: read(() => -new Date(Date.UTC(year, 0, 15, 12)).getTimezoneOffset()),
      july_reference: `${year}-07-15T12:00:00.000Z`,
      july_offset_minutes_east: read(() => -new Date(Date.UTC(year, 6, 15, 12)).getTimezoneOffset())
    },
    identity: {
      user_agent: read(() => nav.userAgent),
      platform: read(() => nav.platform),
      language: read(() => nav.language),
      languages: read(() => Array.from(nav.languages)),
      hardware_concurrency: read(() => nav.hardwareConcurrency),
      approximate_device_memory_gib: read(() => nav.deviceMemory),
      max_touch_points: read(() => nav.maxTouchPoints),
      webdriver: read(() => nav.webdriver),
      low_entropy_client_hints: read(() => nav.userAgentData?.toJSON())
    },
    display: {
      screen_width_css_px: read(() => scr.width),
      screen_height_css_px: read(() => scr.height),
      available_width_css_px: read(() => scr.availWidth),
      available_height_css_px: read(() => scr.availHeight),
      color_depth: read(() => scr.colorDepth),
      pixel_depth: read(() => scr.pixelDepth),
      viewport_width_css_px: read(() => globalThis.innerWidth),
      viewport_height_css_px: read(() => globalThis.innerHeight),
      device_pixel_ratio: read(() => globalThis.devicePixelRatio),
      visual_viewport_scale: read(() => globalThis.visualViewport?.scale)
    },
    capabilities: {
      secure_context: read(() => globalThis.isSecureContext),
      top_level_context: read(() => globalThis.top === globalThis.self),
      cookie_enabled_flag_only: read(() => nav.cookieEnabled),
      webrtc_api_present_only: read(() => typeof globalThis.RTCPeerConnection !== "undefined"),
      webgpu_api_present_only: read(() => typeof nav.gpu !== "undefined"),
      audio_context_api_present_only: read(() => typeof globalThis.AudioContext !== "undefined")
    },
    webgl: { state: "NOT_TESTED", reason: "Optional graphics probe is off." }
  };

  if (OPTIONS.graphics) {
    result.webgl = read(() => {
      const canvas = document.createElement("canvas");
      let gl = null;
      try {
        gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");
        if (!gl) return { available: false };
        const extension = gl.getExtension("WEBGL_debug_renderer_info");
        return {
          available: true,
          vendor: gl.getParameter(gl.VENDOR),
          renderer: gl.getParameter(gl.RENDERER),
          version: gl.getParameter(gl.VERSION),
          unmasked_metadata_available: Boolean(extension),
          unmasked_vendor: extension ? gl.getParameter(extension.UNMASKED_VENDOR_WEBGL) : null,
          unmasked_renderer: extension ? gl.getParameter(extension.UNMASKED_RENDERER_WEBGL) : null
        };
      } finally {
        // Release only the temporary context created by this probe.
        try { gl?.getExtension("WEBGL_lose_context")?.loseContext(); } catch (_) { /* no output */ }
      }
    });
  }
  return result;
})()
