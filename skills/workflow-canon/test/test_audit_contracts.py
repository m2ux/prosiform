"""Independent finding, check-evidence and dispatch contract regressions."""

import json
import math
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO

from audit_fixtures import AuditFixture
from audit_common import AuditError, cell_index
from audit_dispatch import packet, plan_assignments
from audit_inventory import inventory
from audit_render import render
from audit_state import bind, gate, ingest
from audit_surface import main, save, status_summary


class AuditContractTests(AuditFixture):
    def finding(self, summary, severity='High', band='Contract'):
        return {'entry': 'AP-01. missing-contract',
                'location': 'corpus/demo/techniques/emit.md#/emit/outputs/report',
                'summary': summary, 'fix': 'Define the missing output constraint.',
                'severity': severity, 'band': band, 'origin': 'pre-existing'}

    def test_one_cell_retains_two_findings_with_separate_independent_confirmations(self):
        self.verified_map()
        index = cell_index(self.state)
        target = next(key for key, (row, criterion) in index.items()
                      if row == 'corpus/demo/techniques/emit.md#@element'
                      and criterion == 'ap:missing-contract')
        planned = plan_assignments(self.state, 'evaluate', self.budgets)
        for assignment in planned['assignments']:
            bind(self.state, assignment, 'auditor')
            receipt = self.receipt(assignment, 'pass', 'auditor')
            for record in receipt['records']:
                if target in record['items']:
                    record['status'] = 'finding'
                    record['findings'] = [self.finding('Report media type is missing.'),
                                          self.finding('Report retention constraint is missing.')]
            self.state = ingest(self.state, receipt)
        self.assertEqual(len(self.state['evaluations'][target]['findings']), 2)
        finding_ids = sorted(key for key in self.state['obligations'] if key.startswith('finding:'))
        self.assertEqual(len(finding_ids), 2)
        self.assertEqual(len(gate(self.state)['findings']), 2)

        planned = plan_assignments(self.state, 'obligations', self.budgets)
        first_owner = next(assignment for assignment in planned['assignments']
                           if finding_ids[0] in self.state['assignments'][assignment]['items'])
        own_confirmation = deepcopy(self.state)
        bind(own_confirmation, first_owner, 'auditor')
        with self.assertRaises(AuditError):
            ingest(own_confirmation, self.receipt(first_owner, '', 'auditor', [finding_ids[0]]))

        held = finding_ids[1]
        for assignment in planned['assignments']:
            bind(self.state, assignment, 'independent-reviewer')
            ready = [key for key in self.state['assignments'][assignment]['items'] if key != held]
            if ready:
                self.state = ingest(self.state, self.receipt(assignment, '', 'independent-reviewer', ready))
        status = gate(self.state)
        self.assertEqual(status['obligations_missing'], [held])
        self.assertFalse(status['complete'])

        final_owner = next(assignment for assignment in planned['assignments']
                           if held in self.state['assignments'][assignment]['items'])
        self.state = ingest(self.state, self.receipt(final_owner, '', 'independent-reviewer',
                                                    [held], attempt='confirm-second'))
        status = gate(self.state)
        self.assertTrue(status['complete'])
        self.assertEqual(len(status['findings']), 2)
        folder = self.root / 'rendered'
        render(self.state, folder)
        report = (folder / 'audit-report.md').read_text()
        for finding in status['findings']:
            self.assertIn(finding['id'], report)
            self.assertIn(finding['summary'], report)

    def test_explicit_finding_identity_deduplicates_across_cells(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        targets = self.state['assignments'][assignment]['items'][:2]
        self.assertEqual(len(targets), 2)
        receipt = self.receipt(assignment, 'finding', 'auditor', targets)
        for record in receipt['records']:
            record['findings'] = [self.finding('Report media type is missing.')]
        self.state = ingest(self.state, receipt)
        ids = [self.state['evaluations'][key]['findings'][0]['id'] for key in targets]
        self.assertEqual(ids[0], ids[1])
        self.assertEqual(len(gate(self.state)['findings']), 1)
        self.assertEqual([key for key in self.state['obligations'] if key.startswith('finding:')],
                         ['finding:' + ids[0]])

    def test_duplicate_finding_cannot_silently_change_classification(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        first, second = self.state['assignments'][assignment]['items'][:2]
        receipt = self.receipt(assignment, 'finding', 'auditor', [first])
        receipt['records'][0]['findings'] = [self.finding('Report media type is missing.', band='Live')]
        self.state = ingest(self.state, receipt)
        for severity, band, origin in (('Low', 'Live', 'pre-existing'),
                                       ('High', 'Hygiene', 'pre-existing'), ('High', 'Live', 'diff')):
            with self.subTest(severity=severity, band=band, origin=origin):
                repeated = self.receipt(assignment, 'finding', 'auditor', [second], attempt='another-cell')
                repeated['records'][0]['findings'] = [self.finding('Report media type is missing.',
                                                                   severity=severity, band=band)]
                repeated['records'][0]['findings'][0]['origin'] = origin
                try:
                    updated = ingest(self.state, repeated)
                except AuditError:
                    continue
                finding = gate(updated)['findings'][0]
                self.assertEqual(finding['severity'], 'High')
                self.assertEqual(finding['band'], 'Live')
                self.assertEqual(finding['origin'], 'pre-existing')

    def test_one_record_cannot_hide_conflicting_duplicates_in_its_findings_array(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        first = self.state['assignments'][assignment]['items'][0]
        receipt = self.receipt(assignment, 'finding', 'auditor', [first])
        receipt['records'][0]['findings'] = [self.finding('Report media type is missing.', band='Live'),
                                          self.finding('Report media type is missing.', severity='Low',
                                                       band='Hygiene')]
        with self.assertRaises(AuditError):
            ingest(self.state, receipt)
        self.assertNotIn(first, self.state['evaluations'])

    def guard_receipt(self):
        self.verified_map()
        planned = plan_assignments(self.state, 'obligations', self.budgets)
        assignment = next(key for key in planned['assignments']
                          if 'check:guards' in self.state['assignments'][key]['items'])
        bind(self.state, assignment, 'check-reviewer')
        return self.receipt(assignment, '', 'check-reviewer', ['check:guards'])

    def test_unmeasured_guard_exit_cannot_be_a_pass(self):
        receipt = self.guard_receipt()
        receipt['records'][0]['check']['exit_code'] = 2
        with self.assertRaises(AuditError):
            ingest(self.state, receipt)
        self.assertNotIn('check:guards', self.state['obligation_results'])

    def test_guard_pass_requires_captured_command_output(self):
        receipt = self.guard_receipt()
        for missing in ('command', 'output', 'output-file'):
            with self.subTest(missing=missing):
                invalid = deepcopy(receipt)
                if missing == 'output-file':
                    invalid['records'][0]['check']['output'] = str(self.root / 'absent-output.txt')
                else:
                    invalid['records'][0]['check'].pop(missing)
                with self.assertRaises(AuditError):
                    ingest(self.state, invalid)
                self.assertNotIn('check:guards', self.state['obligation_results'])

    def test_large_inventory_manifest_partitions_into_bounded_slices(self):
        outside = set()
        for number in range(60):
            source = f'corpus/outside/resource-{number:02}.md'
            outside.add(source)
            self.write(source, '# Independent source\n' + 'Reference-free qualification text. ' * 300 + '\n')
        self.state = inventory(self.root, self.engine, self.spec, 'coordinator')
        limits = deepcopy(self.budgets)
        limits.update(context_tokens=12000, reserve_tokens=1000, safety_tokens=500,
                      output_tokens=800, work_seconds=8)
        planned = plan_assignments(self.state, 'inventory', limits)
        self.assertGreater(planned['assignment_count'], 1)
        required = {key for key, obligation in self.state['obligations'].items()
                    if obligation['kind'] == 'inventory'}
        assigned, represented = [], set()
        for assignment in planned['assignments']:
            content = packet(self.state, assignment)
            job = content['assignment']
            assigned.extend(job['items'])
            represented.update(content['corpus_manifest'])
            cost = job['estimate']
            actual_bytes = len(json.dumps(content, indent=2, ensure_ascii=False,
                                          sort_keys=True).encode('utf-8'))
            self.assertLessEqual(math.ceil(actual_bytes / limits['bytes_per_token']),
                                 cost['input_tokens_estimate'])
            self.assertLessEqual(cost['input_tokens_estimate'] + cost['output_tokens_estimate'],
                                 limits['context_tokens'] - limits['reserve_tokens'] - limits['safety_tokens'])
            self.assertLessEqual(cost['output_tokens_estimate'], limits['output_tokens'])
            self.assertLessEqual(cost['work_seconds_estimate'], limits['work_seconds'])
        self.assertEqual(set(assigned), required)
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertTrue(outside <= represented)

    def test_empty_element_types_render_explicit_empty_surfaces(self):
        source = 'corpus/isolated/techniques/one.md'
        self.write(source, '## Capability\nProduce one artifact.\n\n## Outputs\n### artifact\n')
        self.state = inventory(self.root, self.engine, {'paths': [source], 'checks': ['guards']},
                               'coordinator')
        self.assertEqual({row['type'] for row in self.state['rows'].values()}, {'technique'})
        folder = self.root / 'empty-types'
        render(self.state, folder)
        self.assertEqual(len(list(folder.glob('change-surface-*.md'))), 4)
        for kind in ('workflow', 'routine', 'activity'):
            with self.subTest(kind=kind):
                text = (folder / f'change-surface-{kind}.md').read_text()
                self.assertIn('No scoped elements of this type.', text)
                self.assertIn('[coverage](audit-coverage.md)', text)
                self.assertNotIn('audit-evidence.md#cell-', text)
        self.assertIn('audit-evidence.md#cell-', (folder / 'change-surface-technique.md').read_text())

    def test_large_status_summary_has_counts_and_links_without_residual_item_arrays(self):
        for number in range(200):
            self.write(f'corpus/demo/resources/status-{number:03}.md', '# Resource\nA scoped resource.\n')
        self.state = inventory(self.root, self.engine, self.spec, 'coordinator')
        folder = self.root / 'status-run'
        save(self.state, folder)
        detailed = gate(self.state)
        summary = status_summary(self.state)
        self.assertGreater(summary['unknown'], 1000)
        self.assertFalse(summary['complete'])
        self.assertFalse(summary['mapping_ready'])
        for key in ('inventory_missing', 'obligations_missing', 'findings'):
            self.assertIs(type(summary[key]), int)
            self.assertEqual(summary[key], len(detailed[key]))
        self.assertEqual(summary['snapshot'], self.state['snapshot'])
        self.assertEqual(summary['stale_count'], 0)
        self.assertEqual(summary['stale'], [])
        self.assertEqual(summary['artifacts'], {name: str(folder / name) for name in
                                               ('audit-report.md', 'audit-coverage.md', 'audit-state.json')})
        encoded = json.dumps(summary)
        self.assertLess(len(encoded), 5000)
        self.assertNotIn('inventory:scope:', encoded)
        self.assertNotIn('status-199.md', encoded)
        output = StringIO()
        with redirect_stdout(output):
            exit_code = main(['status', '--run', str(folder), '--require', 'complete'])
        self.assertEqual(exit_code, 2)
        self.assertEqual(json.loads(output.getvalue()), summary)
