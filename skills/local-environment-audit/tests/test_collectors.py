#!/usr/bin/env python3
"""Offline standard-library tests. Writes only temporary test artifacts."""
from __future__ import annotations
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    assert spec and spec.loader
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


host = module('audit_host', 'host_snapshot.py')
compare = module('audit_compare', 'compare_snapshots.py')


def fixture():
    return {
        '_meta': {'schema': compare.SCHEMA, 'probe_version': '1.0.0',
                  'target_alias': 'fixture-profile', 'context_label': 'fixture-page',
                  'launch_id': 'L1', 'captured_at': '2026-01-01T00:00:00Z',
                  'graphics_requested': False},
        'time': {'utc_iso': '2026-01-01T00:00:00Z', 'epoch_ms': 0,
                 'utc_offset_minutes_east': {'state': 'observed', 'value': 0}},
        'identity': {'platform': {'state': 'observed', 'value': 'fixture-platform'}},
        'display': {}, 'capabilities': {}, 'webgl': {'state': 'NOT_TESTED'}
    }


class CollectorTests(unittest.TestCase):
    def test_host_scope_and_no_network_intent(self):
        result = host.snapshot('fixture-host', 'unverified')
        self.assertEqual(result['_meta']['source'], 'executing-runtime')
        self.assertFalse(result['_meta']['target_binding_independently_verified_by_script'])
        self.assertFalse(result['_meta']['intentional_network_calls'])
        self.assertEqual(result['time']['clock_accuracy'], 'NOT_TESTED')
        self.assertNotIn('hostname', result['runtime'])

    def test_alias_rejects_email(self):
        import argparse
        with self.assertRaises(argparse.ArgumentTypeError):
            host.alias('someone@example.invalid')

    def test_exclusive_output(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'test.json'
            host.write_exclusive(path, '{"first":true}\n')
            with self.assertRaises(FileExistsError):
                host.write_exclusive(path, '{"replacement":true}\n')
            self.assertEqual(json.loads(path.read_text()), {'first': True})

    def test_host_cli_json(self):
        proc = subprocess.run([sys.executable, '-I', '-S', str(ROOT/'scripts/host_snapshot.py'),
                               '--target-alias', 'fixture-host'], capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)['_meta']['target_binding'], 'unverified')

    def test_timestamp_changes_are_excluded(self):
        first = fixture(); second = copy.deepcopy(first)
        second['_meta']['captured_at'] = '2026-01-01T00:01:00Z'
        second['_meta']['launch_id'] = 'L2'
        second['time']['utc_iso'] = '2026-01-01T00:01:00Z'
        second['time']['epoch_ms'] = 60_000
        result = compare.compare_many([first, second])
        self.assertEqual(result['comparisons'][0]['changed_paths'], [])
        self.assertTrue(result['comparison_only'])

    def test_timezone_change_is_retained(self):
        first = fixture(); second = copy.deepcopy(first)
        second['time']['utc_offset_minutes_east']['value'] = 480
        result = compare.compare_many([first, second])
        self.assertEqual(result['comparisons'][0]['changed_paths'], ['time.utc_offset_minutes_east.value'])
        self.assertNotIn('480', json.dumps(result))

    def test_target_mismatch_rejected(self):
        first = fixture(); second = copy.deepcopy(first)
        second['_meta']['target_alias'] = 'other-profile'
        with self.assertRaises(ValueError):
            compare.compare_many([first, second])

    def test_mode_mismatch_rejected(self):
        first = fixture(); second = copy.deepcopy(first)
        second['_meta']['graphics_requested'] = True
        with self.assertRaises(ValueError):
            compare.compare_many([first, second])

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'duplicate.json'
            path.write_text('{"a":1,"a":2}')
            with self.assertRaises(ValueError):
                compare.load_snapshot(path)

    def test_missing_labels_rejected(self):
        data = fixture(); data['_meta']['target_alias'] = 'UNSET'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'unset.json'
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                compare.load_snapshot(path)

    def test_complete_snapshot_loads(self):
        data = fixture()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'valid.json'
            path.write_text(json.dumps(data))
            self.assertEqual(compare.load_snapshot(path), data)

    def test_oversized_input_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'large.json'
            path.write_bytes(b' ' * (compare.MAX_BYTES + 1))
            with self.assertRaises(ValueError):
                compare.load_snapshot(path)

    def test_cli_requires_two_inputs(self):
        proc = subprocess.run([sys.executable, '-I', '-S', str(ROOT/'scripts/compare_snapshots.py'),
                               'one.json'], capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 2)

    def test_comparison_keeps_types(self):
        self.assertEqual(compare.compare_paths({'a': False}, {'a': 0}), ['a'])

    def test_report_template_has_all_controls_and_no_results(self):
        catalog = json.loads((ROOT/'assets/control-catalog.json').read_text())
        report = json.loads((ROOT/'assets/report-template.json').read_text())
        self.assertEqual(set(report['controls']), {control['id'] for control in catalog})
        self.assertEqual(len(catalog), 46)
        self.assertTrue(all(item['outcome'] == 'NOT_TESTED' for item in report['controls'].values()))
        self.assertEqual(report['overall_result'], 'incomplete')
        self.assertEqual(report['configuration_changes'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
