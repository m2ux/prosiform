"""Inventory checks against independently specified source facts."""

from audit_fixtures import AuditFixture
from audit_inventory import freshness, inventory


class InventoryTests(AuditFixture):
    def test_all_types_and_supporting_material(self):
        self.assertEqual({row['type'] for row in self.state['rows'].values()},
                         {'workflow', 'activity', 'routine', 'technique'})
        self.assertTrue(any(row['source_kind'] == 'supporting' for row in self.state['rows'].values()))
        self.assertEqual(set(self.state['criteria']),
                         {'ap:missing-contract', 'ap:unsafe-binding', 'dp:1'})
        self.assertTrue(any(row['kind'] == 'relationship' for row in self.state['rows'].values()))
        self.assertIn('corpus/demo/techniques/emit.md#/emit/outputs/report', set(self.state['rows']))
        self.assertIn('corpus/demo/activities/start.yaml#/steps/id=run/routine', self.state['rows'])

    def test_duplicate_ids_keep_occurrences_and_missing_sections(self):
        self.write('corpus/demo/activities/start.yaml',
                   'id: start\nsteps:\n  - id: same\n    kind: action\n'
                   '  - id: same\n    kind: action\n')
        self.write('corpus/demo/techniques/emit.md', '# Emit\nNo capability heading.\n')
        state = inventory(self.root, self.engine, self.spec, 'coordinator')
        self.assertIn('corpus/demo/activities/start.yaml#/steps/id=same', state['rows'])
        self.assertIn('corpus/demo/activities/start.yaml#/steps/id=same~1', state['rows'])
        self.assertIn('corpus/demo/techniques/emit.md#@missing/capability', state['rows'])

    def test_untouched_consumer_joins_surface(self):
        spec = {'paths': ['corpus/demo/techniques/emit.md']}
        state = inventory(self.root, self.engine, spec, 'coordinator')
        origins = {row['source']: row['origin'] for row in state['rows'].values()}
        self.assertEqual(origins['corpus/demo/routines/once.yaml'], 'consumer')
        self.assertEqual(origins['corpus/demo/activities/start.yaml'], 'consumer')

    def test_bytes_and_canon_membership_are_freshness_inputs(self):
        self.assertEqual(freshness(self.state), [])
        self.write('corpus/canon/resources/design-principles.md',
                   '# Principles\n\n## 1. Define contracts\nChanged wording.\n'
                   '\n## 2. New invariant\nA new criterion.\n')
        self.assertTrue(freshness(self.state))
        state = inventory(self.root, self.engine, self.spec, 'coordinator')
        self.assertIn('dp:2', state['criteria'])
        self.assertNotEqual(state['snapshot'], self.state['snapshot'])

    def test_malformed_source_remains_inventoried(self):
        self.write('corpus/demo/activities/start.yaml', 'id: start\nsteps: [\n')
        state = inventory(self.root, self.engine, self.spec, 'coordinator')
        self.assertTrue(state['diagnostics'])
        self.assertIn('corpus/demo/activities/start.yaml#@element', state['rows'])

    def test_explicit_relationship_carries_execution_context(self):
        self.write('corpus/shared/techniques/borrowed.md', '# Borrowed\n## Capability\nAct.\n')
        spec = {'paths': ['corpus/demo'], 'relationships': [{
            'source': 'corpus/demo/activities/start.yaml',
            'target': 'corpus/shared/techniques/borrowed.md',
            'address': 'start/run/call', 'label': 'executing workflow demo; routine once/call',
            'context': ['corpus/demo/workflow.yaml']}]}
        state = inventory(self.root, self.engine, spec, 'coordinator')
        relation = next(row for row in state['rows'].values()
                        if row.get('relationship', {}).get('address') == 'start/run/call')
        self.assertEqual(set(relation['sources']), {'corpus/demo/activities/start.yaml',
                         'corpus/shared/techniques/borrowed.md', 'corpus/demo/workflow.yaml'})
