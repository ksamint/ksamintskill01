#!/usr/bin/env python3
"""Minimal offline snapshot of THIS runtime, not proof of the user's device.

Python 3.10+, standard library only. No browser/profile/credential reads, shell
commands, network requests, hostname collection, or environment dumps.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import re
import sys
from typing import Any


def alias(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,79}", value):
        raise argparse.ArgumentTypeError("Use a non-sensitive alias: 1-80 letters, digits, '.', '_', ':', '-'.")
    return value


def snapshot(target_alias: str, target_binding: str) -> dict[str, Any]:
    utc_now = datetime.now(timezone.utc)
    local_now = utc_now.astimezone()
    offset = local_now.utcoffset()
    return {
        "_meta": {
            "schema": "local-environment-host-snapshot/1.0",
            "collector_version": "1.0.0",
            "captured_at": utc_now.isoformat(),
            "target_alias": target_alias,
            "target_binding": target_binding,
            "source": "executing-runtime",
            "target_binding_independently_verified_by_script": False,
            "intentional_network_calls": False,
            "configuration_changes": False,
        },
        "runtime": {
            "os_family": platform.system(),
            "os_release": platform.release(),
            "architecture_reported_to_python": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "logical_cpus_reported_to_python": os.cpu_count(),
        },
        "time": {
            "utc_iso": utc_now.isoformat(),
            "local_iso": local_now.isoformat(),
            "utc_offset_minutes_east": int(offset.total_seconds() / 60) if offset else 0,
            "runtime_timezone_label": local_now.tzname(),
            "iana_timezone": None,
            "clock_sync_status": "NOT_TESTED",
            "clock_accuracy": "NOT_TESTED",
        },
        "limitations": [
            "This measures the executing runtime; a VM, container or remote runner is not automatically the requested physical host.",
            "Target binding is an operator assertion and needs separate evidence.",
            "The timezone label may be an abbreviation, not an IANA zone identifier.",
            "Clock synchronization, browser state, routing, permissions and installed application inventory are not tested.",
            "Logical CPU availability reported to Python is not a verified physical CPU inventory.",
        ],
    }


def write_exclusive(path: Path, text: str) -> None:
    """Create only the explicitly named new artifact; never overwrite."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        handle.write(text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-alias", required=True, type=alias)
    parser.add_argument("--target-binding", choices=["unverified", "operator-confirmed"], default="unverified")
    parser.add_argument("--output", type=Path, help="Explicit new file in an existing approved directory; otherwise prints JSON.")
    args = parser.parse_args()
    try:
        text = json.dumps(snapshot(args.target_alias, args.target_binding), ensure_ascii=False, indent=2) + "\n"
        if args.output is None:
            sys.stdout.write(text)
        else:
            write_exclusive(args.output, text)
    except OSError as error:
        # Avoid echoing private paths or arbitrary exception content.
        sys.stderr.write(f"Collection/output failed ({type(error).__name__}); check the approved destination and access.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
