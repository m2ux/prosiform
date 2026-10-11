"""Adversarial evidence, assignment and completion checks."""

from copy import deepcopy

from audit_fixtures import AuditFixture
from audit_common import AuditError, cell_index, read_json
from audit_dispatch import packet, plan_assignments
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
