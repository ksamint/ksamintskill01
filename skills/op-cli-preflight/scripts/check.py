#!/usr/bin/env python3
"""Verify 1Password CLI access without handling or printing secrets."""

import argparse
import subprocess
import sys


def run(*args: str, timeout: int) -> bool:
    try:
        return subprocess.run(
            ["op", *args],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            check=False,
        ).returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Quick status; no sign-in prompt")
    parser.add_argument("--signin", action="store_true", help="Try the normal desktop sign-in once")
    args = parser.parse_args()
    if args.check == args.signin:
        parser.error("choose exactly one of --check or --signin")

    if run("whoami", timeout=5):
        print("1Password CLI ready")
        return 0
    if args.check:
        print("1Password CLI unavailable; run --signin before reading a secret")
        return 2
    if not run("signin", timeout=20):
        print("1Password CLI sign-in failed or timed out; local app unlock may be needed", file=sys.stderr)
        return 2
    if run("vault", "list", "--format=json", timeout=30):
        print("1Password CLI ready")
        return 0
    print("1Password CLI still awaits local Touch ID or app authorization", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
