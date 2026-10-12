"""Adversarial evidence, assignment and completion checks."""

from copy import deepcopy
from hashlib import sha256

from audit_fixtures import AuditFixture
from audit_common import AuditError, cell_index, read_json
from audit_dispatch import estimate, packet, plan_assignments
from audit_inventory import inventory
from audit_state import bind, gate, ingest, refresh, reset
from audit_surface import main, save


class LifecycleTests(AuditFixture):
    def test_complete_lifecycle_requires_every_phase(self):
        self.assertFalse(gate(self.state)['mapping_ready'])
        self.verified_map()
        self.assertTrue(gate(self.state)['mapping_ready'])
        self.assertFalse(gate(self.state)['complete'])
        self.phase('evaluate', 'pass', 'auditor')
        self.assertFalse(gate(self.state)['complete'])
        self.phase('obligations', 'pass', 'obligation-reviewer')
        self.assertTrue(gate(self.state)['complete'])

    def test_self_verification_and_early_evaluation_refused(self):
        with self.assertRaises(AuditError):
            plan_assignments(self.state, 'evaluate', self.budgets)
        self.phase('map', 'A', 'mapper')
        planned = plan_assignments(self.state, 'verify', self.budgets)
        with self.assertRaises(AuditError):
            bind(self.state, planned['assignments'][0], 'mapper')

    def test_partial_return_extra_item_and_retry(self):
        planned = plan_assignments(self.state, 'map', self.budgets)
        assignment = planned['assignments'][0]
        bind(self.state, assignment, 'mapper')
        first = self.state['assignments'][assignment]['items'][0]
        receipt = self.receipt(assignment, 'A', 'mapper', [first])
        self.state = ingest(self.state, receipt)
        self.assertEqual(self.state['assignments'][assignment]['status'], 'partial')
        self.assertGreater(gate(self.state)['unknown'], 0)
        bad = self.receipt(assignment, 'A', 'mapper', attempt='two')
        bad['records'][0]['items'] = ['unknown-cell']
        with self.assertRaises(AuditError):
            ingest(self.state, bad)
        self.state['assignments'][assignment]['status'] = 'failed'
        retry = plan_assignments(self.state, 'map', self.budgets)
        assigned = [key for job in retry['assignments'] for key in self.state['assignments'][job]['items']]
        self.assertNotIn(first, assigned)
        self.assertEqual(len(assigned), len(set(assigned)))

    def test_exclusions_need_independent_verification(self):
        self.phase('map', 'N', 'mapper')
        self.phase('inventory', 'verified', 'inventory-reviewer')
        self.assertFalse(gate(self.state)['mapping_ready'])
        self.phase('verify', 'verified', 'map-reviewer')
        self.assertTrue(gate(self.state)['mapping_ready'])
        self.assertEqual(gate(self.state)['unevaluated'], 0)

    def test_mapping_edit_invalidates_receipt(self):
        self.verified_map()
        key = next(iter(self.state['mappings']))
        self.state['mappings'][key]['reason'] = 'Changed rationale'
        self.assertFalse(gate(self.state)['mapping_ready'])
        reset(self.state, [key], 'Independent reviewer found a missed constraint')
        self.assertNotIn(key, self.state['verifications'])
        self.assertGreater(gate(self.state)['unknown'], 0)

    def test_source_change_blocks_results_and_refreshes_rows(self):
        self.verified_map()
        self.write('corpus/demo/techniques/emit.md', '# Emit\n## Capability\nNew draft.\n')
        self.assertFalse(gate(self.state)['mapping_ready'])
        self.assertTrue(gate(self.state)['stale'])
        self.state = refresh(self.state)
        self.assertGreater(gate(self.state)['unknown'], 0)
        self.assertTrue(gate(self.state)['inventory_missing'])

    def test_stale_assignment_and_duplicate_attempt_refused(self):
        assignment = plan_assignments(self.state, 'map', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'mapper')
        receipt = self.receipt(assignment, 'A', 'mapper')
        bad = deepcopy(receipt)
        bad['snapshot'] = 'old'
        with self.assertRaises(AuditError):
            ingest(self.state, bad)
        self.state = ingest(self.state, receipt)
        with self.assertRaises(AuditError):
            ingest(self.state, receipt)

    def test_wide_render_empty_type_and_tampered_view(self):
        folder = self.root / 'run'
        save(self.state, folder)
        self.assertEqual(len(list(folder.glob('change-surface-*.md'))), 4)
        self.assertTrue((folder / 'audit-evidence.md').is_file())
        target = folder / 'change-surface-technique.md'
        target.write_text('An incomplete replacement\n')
        self.assertIn('Rendered artifact changed: change-surface-technique.md', gate(self.state)['stale'])
        self.assertEqual(main(['status', '--run', str(folder), '--require', 'complete']), 2)

    def test_budget_partition_and_oversized_context(self):
        self.budgets['work_seconds'] = 10
        planned = plan_assignments(self.state, 'map', self.budgets)
        self.assertGreater(planned['assignment_count'], 1)
        items = [item for key in planned['assignments'] for item in self.state['assignments'][key]['items']]
        self.assertEqual(set(items), set(cell_index(self.state)))
        self.assertEqual(len(items), len(set(items)))
        self.assertTrue(all(len(self.state['assignments'][key]['items']) <= 5 for key in planned['assignments']))
        sample = packet(self.state, planned['assignments'][0])
        self.assertTrue(sample['source_excerpts'])
        small = deepcopy(self.budgets)
        small['context_tokens'] = 2001
        fresh_state = inventory(self.root, self.engine, self.spec, 'coordinator')
        with self.assertRaises(AuditError):
            plan_assignments(fresh_state, 'map', small)

    def test_missing_evidence_is_not_a_disposition(self):
        assignment = plan_assignments(self.state, 'map', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'mapper')
        receipt = self.receipt(assignment, 'N', 'mapper')
        receipt['records'][0]['evidence'] = []
        with self.assertRaises(AuditError):
            ingest(self.state, receipt)


class MappingEvidenceContextTests(AuditFixture):
    def _map_relationship_with_extra_evidence(self, overlapping_fact='Overlapping fact.'):
        source = 'corpus/demo/resources/evidence.md'
        text = ('# Supporting Evidence\nFirst cited fact.\n' + overlapping_fact + '\n'
                'Last overlapping fact.\nAdjacent cited fact.\nUncited gap.\n'
                'Separate cited fact.\nUncited tail.\n')
        self.write(source, text)
        self.state = inventory(self.root, self.engine, self.spec, 'coordinator')
        row = next(value for value in self.state['rows'].values()
                   if value['kind'] == 'relationship'
                   and value['source'] == 'corpus/demo/workflow.yaml'
                   and set(value['sources']) == {'corpus/demo/workflow.yaml',
                                                'corpus/demo/activities/start.yaml'})
        # This cell needs the supporting source only through its mapping evidence.
        self.state['rows'] = {row['id']: row}
        self.state['criteria'] = {'dp:1': self.state['criteria']['dp:1']}
        assignment = plan_assignments(self.state, 'map', self.budgets)['assignments'][0]
        bind(self.state, assignment, 'mapper')
        receipt = self.receipt(assignment, 'A', 'mapper')
        receipt['records'][0]['evidence'].extend(
            {'source': source, 'start': start, 'end': end}
            for start, end in ((2, 3), (3, 4), (5, 5), (7, 7), (2, 3)))
        self.state = ingest(self.state, receipt)
        self.phase('inventory', 'verified', 'inventory-reviewer')
        return deepcopy(self.state), next(iter(cell_index(self.state))), source, text

    def test_mapping_evidence_spans_are_in_verification_and_evaluation_packets(self):
        mapped, key, source, text = self._map_relationship_with_extra_evidence()
        for phase in ('verify', 'evaluate'):
            with self.subTest(phase=phase):
                self.state = deepcopy(mapped)
                if phase == 'evaluate':
                    self.phase('verify', 'verified', 'map-reviewer')
                assignment = plan_assignments(self.state, phase, self.budgets)['assignments'][0]
                bind(self.state, assignment, 'packet-reviewer')
                result = packet(self.state, assignment)
                self.assertEqual(result['assignment']['items'], [key])
                self.assertEqual(result['assignment']['estimate']['context'].get(source),
                                 [[2, 5], [7, 7]])
                excerpts = [item for item in result['source_excerpts'] if item['source'] == source]
                self.assertEqual(excerpts, [
                    {'source': source, 'start': 2, 'end': 5,
                     'hash': sha256(text.encode()).hexdigest(),
                     'text': 'First cited fact.\nOverlapping fact.\nLast overlapping fact.\nAdjacent cited fact.'},
                    {'source': source, 'start': 7, 'end': 7,
                     'hash': sha256(text.encode()).hexdigest(), 'text': 'Separate cited fact.'}])
                for required in ('corpus/demo/workflow.yaml', 'corpus/demo/activities/start.yaml',
                                 'corpus/canon/resources/design-principles.md'):
                    original = (self.root / required).read_text()
                    preserved = [item for item in result['source_excerpts'] if item['source'] == required]
                    self.assertEqual(preserved, [
                        {'source': required, 'start': 1, 'end': len(original.splitlines()),
                         'hash': sha256(original.encode()).hexdigest(), 'text': original.rstrip('\n')}])

    def test_known_mapping_evidence_can_exceed_dispatch_budget(self):
        mapped, key, source, _ = self._map_relationship_with_extra_evidence('x' * 16384)
        for phase in ('verify', 'evaluate'):
            with self.subTest(phase=phase):
                self.state = deepcopy(mapped)
                if phase == 'evaluate':
                    self.phase('verify', 'verified', 'map-reviewer')
                without_dependency = deepcopy(self.state)
                mapping = without_dependency['mappings'][key]
                mapping['evidence'] = [cite for cite in mapping['evidence'] if cite['source'] != source]
                baseline = estimate(without_dependency, phase, [key], self.budgets,
                                    cell_index(without_dependency))
                small = deepcopy(self.budgets)
                small['context_tokens'] = (baseline['input_tokens_estimate']
                                           + baseline['output_tokens_estimate']
                                           + small['reserve_tokens'] + small['safety_tokens'] + 1024)
                with self.assertRaisesRegex(AuditError, 'Indivisible context exceeds declared budgets'):
                    plan_assignments(self.state, phase, small)
