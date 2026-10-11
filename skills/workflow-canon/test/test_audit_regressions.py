"""Regression cases derived from independent audit gate review."""

import json
import math
from copy import deepcopy

from audit_fixtures import AuditFixture
from audit_common import AuditError, cell_index
from audit_dispatch import packet, plan_assignments
from audit_inventory import inventory
from audit_state import bind, gate, ingest, refresh


class GateRegressionTests(AuditFixture):
    def evaluation_with_high_finding(self):
        self.verified_map()
        planned = plan_assignments(self.state, 'evaluate', self.budgets)
        finding_id = None
        for assignment in planned['assignments']:
            bind(self.state, assignment, 'auditor')
            receipt = self.receipt(assignment, 'pass', 'auditor')
            if finding_id is None:
                receipt['records'][0]['status'] = 'finding'
                receipt['records'][0]['findings'] = [{
                    'band': 'Live', 'severity': 'High', 'origin': 'pre-existing',
                    'summary': 'The fixture output contract needs independent confirmation.',
                    'fix': 'Define and verify its contract.'}]
            self.state = ingest(self.state, receipt)
            finding_id = next(key for key in self.state['obligations']
                              if key.startswith('finding:'))
        return finding_id

    def test_identical_refresh_preserves_required_finding_confirmation(self):
        finding_id = self.evaluation_with_high_finding()
        self.assertIn(finding_id, gate(self.state)['obligations_missing'])
        self.state = refresh(self.state)
        self.assertIn(finding_id, self.state['obligations'])
        self.assertIn(finding_id, gate(self.state)['obligations_missing'])
        self.assertFalse(gate(self.state)['complete'])
        self.assertTrue(any(result.get('findings')
                            for result in self.state['evaluations'].values()))

    def test_canon_preamble_change_invalidates_prior_generation(self):
        self.evaluation_with_high_finding()
        before = self.state['snapshot']
        path = self.root / 'corpus/canon/resources/anti-patterns.md'
        path.write_text(path.read_text().replace(
            '# Anti-patterns\n', '# Anti-patterns: review every source construct\n'))
        self.assertTrue(gate(self.state)['stale'])
        self.state = refresh(self.state)
        self.assertNotEqual(before, self.state['snapshot'])
        self.assertEqual(self.state['mappings'], {})
        self.assertEqual(self.state['verifications'], {})
        self.assertEqual(self.state['evaluations'], {})
        self.assertEqual(self.state['assignments'], {})
        self.assertFalse(gate(self.state)['mapping_ready'])
        self.assertFalse(gate(self.state)['complete'])

    def test_failed_and_invalidated_assignments_reject_late_returns(self):
        assignment = plan_assignments(self.state, 'map', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'mapper')
        receipt = self.receipt(assignment, 'A', 'mapper')
        for status in ('failed', 'invalidated'):
            with self.subTest(status=status):
                candidate = deepcopy(self.state)
                candidate['assignments'][assignment]['status'] = status
                with self.assertRaises(AuditError):
                    ingest(candidate, receipt)
                self.assertEqual(candidate['mappings'], {})

    def test_partial_assignment_rejects_accepted_cell_in_later_attempt(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        first = self.state['assignments'][assignment]['items'][0]
        self.assertGreater(len(self.state['assignments'][assignment]['items']), 1)
        self.state = ingest(self.state, self.receipt(assignment, 'pass', 'auditor', [first]))
        self.assertEqual(self.state['assignments'][assignment]['status'], 'partial')
        before = deepcopy(self.state)
        repeated = self.receipt(assignment, 'blocked', 'auditor', [first], attempt='two')
        with self.assertRaises(AuditError):
            ingest(self.state, repeated)
        self.assertEqual(self.state, before)

    def test_returned_assignment_rejects_new_attempt(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        self.state = ingest(self.state, self.receipt(assignment, 'pass', 'auditor'))
        self.assertEqual(self.state['assignments'][assignment]['status'], 'returned')
        repeated = self.receipt(assignment, 'blocked', 'auditor', attempt='two')
        with self.assertRaises(AuditError):
            ingest(self.state, repeated)

    def test_packet_estimate_bounds_full_mapping_and_verification_payloads(self):
        for phase in ('map', 'verify'):
            with self.subTest(phase=phase):
                planned = plan_assignments(self.state, phase, self.budgets)
                self.assertTrue(planned['assignments'])
                for assignment in planned['assignments']:
                    bind(self.state, assignment, 'mapper' if phase == 'map' else 'map-reviewer')
                    content = packet(self.state, assignment)
                    size = len(json.dumps(content, indent=2, ensure_ascii=False,
                                          sort_keys=True).encode('utf-8'))
                    cost = self.state['assignments'][assignment]['estimate']
                    self.assertGreaterEqual(cost['input_tokens_estimate'],
                                            math.ceil(size / self.budgets['bytes_per_token']))
                    self.assertLessEqual(cost['input_tokens_estimate'] + cost['output_tokens_estimate'],
                                         self.budgets['context_tokens'] - self.budgets['reserve_tokens']
                                         - self.budgets['safety_tokens'])
                    self.assertLessEqual(cost['output_tokens_estimate'], self.budgets['output_tokens'])
                    self.assertLessEqual(cost['work_seconds_estimate'], self.budgets['work_seconds'])
                    if phase == 'verify':
                        self.assertTrue(content['mappings'])
                    else:
                        self.state = ingest(self.state, self.receipt(assignment, 'A', 'mapper'))

    def test_inventory_packets_expose_rows_criteria_and_corpus_manifest(self):
        unselected = 'corpus/outside/README.md'
        self.write(unselected, '# Outside\nThis source has no link to the scoped definitions.\n')
        self.state = inventory(self.root, self.engine, self.spec, 'coordinator')
        self.assertFalse(any(row['source'] == unselected for row in self.state['rows'].values()))
        planned = plan_assignments(self.state, 'inventory', self.budgets)
        all_rows, all_criteria, all_sources = set(), set(), set()
        for assignment in planned['assignments']:
            content = packet(self.state, assignment)
            all_rows.update(content['rows'])
            all_criteria.update(content['criteria'])
            all_sources.update(content.get('corpus_manifest', {}))
        self.assertEqual(all_rows, set(self.state['rows']))
        self.assertEqual(all_criteria, set(self.state['criteria']))
        self.assertTrue(set(self.state['sources']) <= all_sources)
        self.assertIn(unselected, all_sources)

    def test_evaluation_rejects_evidence_outside_row_or_criterion(self):
        self.verified_map()
        assignment = plan_assignments(self.state, 'evaluate', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'auditor')
        index = cell_index(self.state)
        key = next(key for key in self.state['assignments'][assignment]['items']
                   if self.state['rows'][index[key][0]]['start'] > 1
                   and self.state['criteria'][index[key][1]]['start'] > 1)
        row, criterion = index[key]
        targets = {'row': self.state['rows'][row]['source'],
                   'criterion': self.state['criteria'][criterion]['source']}
        for kind, source in targets.items():
            with self.subTest(kind=kind):
                receipt = self.receipt(assignment, 'pass', 'auditor', [key])
                for cite in receipt['records'][0]['evidence']:
                    if cite['source'] == source:
                        cite['start'] = cite['end'] = 1
                with self.assertRaises(AuditError):
                    ingest(self.state, receipt)
                self.assertNotIn(key, self.state['evaluations'])
