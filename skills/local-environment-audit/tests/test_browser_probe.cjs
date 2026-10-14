/* Offline VM fixtures, not live browser certification. */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const code = fs.readFileSync(path.join(__dirname, '../scripts/browser_probe.js'), 'utf8');
let calls = 0;
const forbidden = () => { calls += 1; throw new Error('Forbidden fixture action'); };
function context(extra = {}) {
  const ctx = {
    navigator: { userAgent: 'fixture-UA', platform: 'fixture-platform', language: 'en',
      languages: ['en'], hardwareConcurrency: 4, cookieEnabled: true,
      userAgentData: { toJSON: () => ({ brands: [], platform: 'fixture-platform', mobile: false }) } },
    screen: { width: 1200, height: 800, availWidth: 1200, availHeight: 760, colorDepth: 24, pixelDepth: 24 },
    innerWidth: 1000, innerHeight: 700, devicePixelRatio: 1, isSecureContext: true,
    fetch: forbidden, XMLHttpRequest: forbidden, WebSocket: forbidden,
    RTCPeerConnection: forbidden, AudioContext: forbidden,
    document: { createElement: forbidden }, console: { log: forbidden },
    ...extra
  };
  Object.defineProperty(ctx, 'localStorage', { get: forbidden });
  Object.defineProperty(ctx, 'sessionStorage', { get: forbidden });
  ctx.top = ctx; ctx.self = ctx;
  return vm.createContext(ctx);
}
const normal = vm.runInContext(code, context(), { timeout: 2000 });
assert.equal(normal._meta.schema, 'local-environment-browser-snapshot/1.0');
assert.equal(normal._meta.intentional_network_calls, false);
assert.equal(normal.webgl.state, 'NOT_TESTED');
assert.equal(normal.identity.approximate_device_memory_gib.state, 'unavailable');
assert.equal(normal.capabilities.webrtc_api_present_only.value, true);
assert.equal(calls, 0);
const blockedNav = {};
Object.defineProperty(blockedNav, 'userAgent', { get() { const e = new Error(); e.name = 'SecurityError'; throw e; } });
const blocked = vm.runInContext(code, context({ navigator: blockedNav }), { timeout: 2000 });
assert.equal(blocked.identity.user_agent.state, 'blocked-or-error');
assert.equal(blocked.identity.user_agent.error_type, 'SecurityError');
assert.equal(calls, 0);
let released = false;
const gl = {
  VENDOR: 1, RENDERER: 2, VERSION: 3,
  getParameter(key) { return `fixture-${key}`; },
  getExtension(name) {
    if (name === 'WEBGL_debug_renderer_info') return { UNMASKED_VENDOR_WEBGL: 4, UNMASKED_RENDERER_WEBGL: 5 };
    if (name === 'WEBGL_lose_context') return { loseContext() { released = true; } };
    return null;
  }
};
const graphicsCode = code.replace('graphics: false', 'graphics: true');
const graphics = vm.runInContext(graphicsCode, context({ document: { createElement() { return { getContext() { return gl; } }; } } }), { timeout: 2000 });
assert.equal(graphics.webgl.value.available, true);
assert.equal(graphics.webgl.value.unmasked_renderer, 'fixture-5');
assert.equal(released, true);
assert.equal(calls, 0);
console.log('PASS: default no-I/O fixture, unavailable field, API-presence semantics, blocked getter, optional graphics and context cleanup.');
