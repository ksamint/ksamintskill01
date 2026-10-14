#!/usr/bin/env python3
"""Read ShopMenu JSON using its macOS Keychain credential."""
import json
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = 'http://129.211.210.83'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError('API redirect rejected to protect the credential')


def endpoint_url(endpoint):
    parts = urllib.parse.urlsplit(endpoint)
    if parts.scheme or parts.netloc or parts.fragment or not parts.path.startswith('/v1/'):
        raise ValueError('Use a relative /v1/ endpoint without a host or fragment')
    return BASE + urllib.parse.quote(endpoint, safe='/%?=&:+,')


def main():
    if len(sys.argv) != 2:
        raise ValueError('Usage: query.py /v1/shops')
    url = endpoint_url(sys.argv[1])
    result = subprocess.run(
        ['/usr/bin/security', 'find-generic-password', '-s', 'com.codex.shopmenu.api-key',
         '-a', 'shopmenu', '-w', '/Users/af/Library/Keychains/login.keychain-db'],
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode or not result.stdout.strip():
        raise ValueError('ShopMenu Keychain credential unavailable; check login Keychain access')
    request = urllib.request.Request(url, headers={'X-API-Key': result.stdout.strip()})
    with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
        data = json.load(response)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        print(f'ShopMenu: {exc}', file=sys.stderr)
        sys.exit(1)
