"""Fires-on scoping of the unit set a walk carries."""

import subprocess

from audit_fixtures import AuditFixture


# The ids the demo surface writes: each definition kind on it, fields those files declare, its README.
SURFACE_IDS = ('workflow', 'workflow.graph', 'activity', 'activity.steps', 'activity.steps[].kind',
               'routine', 'routine.steps', 'technique', 'technique.outputs', 'readme')
# What each fixture unit declares, stated here so the expectation is independent of the listing.
DECLARED = {'AP-01. missing-contract': ('technique.outputs',),
            'AP-02. unsafe-binding': ('activity.steps',),
            '1. Define contracts': ('technique', 'routine'),
            'Sibling convention': ('resource',)}


class ScopingTests(AuditFixture):
    def listing(self, construct):
        """The units one construct id lists, through the engine's own reader of the line."""
        run = subprocess.run(['npx', 'tsx', 'guards/list-fires-on.ts', construct,
                              '--root', str(self.root / 'corpus')],
                             cwd=self.engine, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        return {line.split(' ', 1)[1] for line in run.stdout.splitlines() if line}

    def scoped(self, ids):
        units = set()
        for construct in ids:
            units |= self.listing(construct)
        return units

    def test_scope_carries_every_unit_firing_on_a_kind_of_the_surface(self):
        kinds = {construct.split('.')[0] for construct in SURFACE_IDS}
        expected = {unit for unit, ids in DECLARED.items()
                    if any(declared.split('.')[0] in kinds for declared in ids)}
        scoped = self.scoped(SURFACE_IDS)
        self.assertEqual(scoped, expected)
        self.assertLess(len(scoped), len(DECLARED))

    def test_a_unit_reaches_only_the_kinds_its_line_names(self):
        self.assertNotIn('AP-02. unsafe-binding', self.scoped(('technique', 'technique.outputs')))
        self.assertNotIn('AP-01. missing-contract', self.scoped(('activity', 'activity.steps')))

    def test_a_kind_named_alone_leaves_its_field_units_unlisted(self):
        self.assertNotIn('AP-01. missing-contract', self.listing('technique'))
        self.assertIn('AP-01. missing-contract', self.listing('technique.outputs'))
