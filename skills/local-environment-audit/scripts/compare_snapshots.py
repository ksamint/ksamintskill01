#!/usr/bin/env python3
"""Compare sanitized browser snapshots. Differences are NOT defect verdicts.

Offline, standard library only. Reports changed field paths, not field values.
Requires matching non-placeholder target/context labels, probe version and mode.
This validates labels, not real-world target identity. No files are written.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

SCHEMA = "local-environment-browser-snapshot/1.0"
MAX_BYTES = 2 * 1024 * 1024
GROUPS = ("time", "identity", "display", "capabilities", "webgl")
TIME_VOLATILE = {"utc_iso", "epoch_ms"}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("Duplicate JSON keys are not accepted.")
        obj[key] = value
    return obj


def load_snapshot(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        raw = handle.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("Snapshot exceeds the 2 MiB size limit.")
    data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    if not isinstance(data, dict) or not isinstance(data.get("_meta"), dict):
        raise ValueError("Expected a browser snapshot object with metadata.")
    if data["_meta"].get("schema") != SCHEMA:
        raise ValueError("Unsupported browser snapshot schema.")
    for group in GROUPS:
        if not isinstance(data.get(group), dict):
            raise ValueError("A required observation group is absent or invalid.")
    for key in ("target_alias", "context_label", "launch_id", "probe_version"):
        value = data["_meta"].get(key)
        if not isinstance(value, str) or not value.strip() or value.upper() == "UNSET":
            raise ValueError("Set non-placeholder target, context, launch and probe-version labels first.")
    if type(data["_meta"].get("graphics_requested")) is not bool:
        raise ValueError("Missing or invalid graphics collection mode.")
    return data


def compare_paths(left: Any, right: Any, path: str = "") -> list[str]:
    if isinstance(left, dict) and isinstance(right, dict):
        output: list[str] = []
        for key in sorted(set(left) | set(right)):
            field = f"{path}.{key}" if path else key
            if key not in left or key not in right:
                output.append(field)
            else:
                output.extend(compare_paths(left[key], right[key], field))
        return output
    # Treat lists as field values; reordering may be meaningful but is not a failure.
    return [] if type(left) is type(right) and left == right else [path]


def observations(snapshot: dict[str, Any]) -> dict[str, Any]:
    result = {key: snapshot[key] for key in GROUPS}
    result["time"] = {key: value for key, value in snapshot["time"].items() if key not in TIME_VOLATILE}
    return result


def compare_many(snapshots: list[dict[str, Any]]) -> dict[str, Any]:
    baseline = snapshots[0]
    constraints = ("schema", "target_alias", "context_label", "probe_version", "graphics_requested")
    comparisons = []
    for index, current in enumerate(snapshots[1:], start=2):
        if any(current["_meta"].get(key) != baseline["_meta"].get(key) for key in constraints):
            raise ValueError("Target/context labels, schema, probe version or collection mode differ; comparison refused.")
        changed = compare_paths(observations(baseline), observations(current))
        comparisons.append({"baseline_input": 1, "candidate_input": index,
                            "changed_field_count": len(changed), "changed_paths": changed})
    return {
        "comparison_only": True,
        "baseline_match_checks": "passed-for-operator-labels-and-probe-mode",
        "independent_target_verification": "required-separately",
        "ignored_fields": ["_meta.*", "time.utc_iso", "time.epoch_ms"],
        "metadata_checked_before_ignoring": list(constraints),
        "comparisons": comparisons,
        "interpretation": "Changes require contextual interpretation. No-change output is not proof of safety, correct routing or an accurate baseline.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshots", type=Path, nargs="+", help="At least two inspected, sanitized browser snapshot JSON files.")
    args = parser.parse_args()
    if len(args.snapshots) < 2:
        parser.error("Supply at least two snapshots.")
    try:
        result = compare_many([load_snapshot(path) for path in args.snapshots])
        sys.stdout.write(json.dumps(result, indent=2) + "\n")
    except (OSError, ValueError, UnicodeError, RecursionError) as error:
        # Do not echo file paths, raw JSON or arbitrary field values.
        sys.stderr.write(f"Comparison refused ({type(error).__name__}). Check snapshot format, labels, collection mode and file access.\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
