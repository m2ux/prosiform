"""The shared skill-file check, over seeded skills in a temporary tree."""

import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import check_skill_files as checker

FENCE = chr(96) * 3


class SkillFileChecks(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.skill = self.root / 'specimen'
        (self.skill / 'references').mkdir(parents=True)

    def write(self, name, text):
        path = self.skill / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def findings(self):
        files = sorted(self.skill.rglob('*.md'))
        used = checker.cited(files)
        cache = {}
        out = []
        for path in files:
            out += checker.check(path, self.root, cache, used)
        return [(Path(where).name, line, kind) for where, line, kind, _ in out]

    def kinds(self):
        return {kind for _, _, kind in self.findings()}

    def test_a_conforming_skill_reports_nothing(self):
        self.write('SKILL.md', '---\nname: specimen\n---\n\n# Specimen\n\n'
                               'One sentence.\n\n- **Mode.**  See [guide](references/guide.md#terms).\n')
        self.write('references/guide.md', '# Guide\n\n## Terms\n\nA sentence.\n')
        self.assertEqual(self.findings(), [])

    def test_a_link_to_a_missing_file_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\nSee [guide](references/absent.md).\n')
        self.assertIn('unresolved link', self.kinds())

    def test_a_link_to_a_missing_heading_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\nSee [terms](references/guide.md#absent).\n')
        self.write('references/guide.md', '# Guide\n\n## Terms\n\nA sentence.\n')
        self.assertIn('unresolved anchor', self.kinds())

    def test_a_link_inside_a_fence_is_a_specimen(self):
        self.write('SKILL.md', f'# Specimen\n\n{FENCE}markdown\n[absent](references/absent.md)\n{FENCE}\n')
        self.assertEqual(self.findings(), [])

    def test_a_link_inside_a_code_span_is_a_specimen(self):
        self.write('SKILL.md', '# Specimen\n\nWrite `[absent](references/absent.md)` in the body.\n')
        self.assertEqual(self.findings(), [])

    def test_a_template_placeholder_is_not_a_path(self):
        self.write('SKILL.md', '# Specimen\n\n- **R1.** [{{Title}}]({{URL}}) and [more](…).\n')
        self.assertEqual(self.findings(), [])

    def test_a_heading_inside_a_fence_is_not_an_anchor(self):
        self.write('SKILL.md', f'# Specimen\n\n## Layout\n\n{FENCE}markdown\n## Layout\n{FENCE}\n')
        self.assertEqual(self.findings(), [])

    def test_a_repeated_anchor_is_reported_when_it_is_cited(self):
        self.write('SKILL.md', '# Specimen\n\nSee [terms](references/guide.md#terms).\n')
        self.write('references/guide.md', '# Guide\n\n## Terms\n\nOne.\n\n## Terms\n\nTwo.\n')
        self.assertIn('duplicate anchor is cited', self.kinds())

    def test_a_repeated_anchor_nobody_cites_is_left_alone(self):
        self.write('references/guide.md', '# Guide\n\n## Terms\n\nOne.\n\n## Terms\n\nTwo.\n')
        self.assertEqual(self.findings(), [])

    def test_a_skipped_heading_level_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\n### Deep\n\nA sentence.\n')
        self.assertIn('heading jump', self.kinds())

    def test_a_bullet_holding_a_code_fence_is_reported(self):
        self.write('SKILL.md', f'# Specimen\n\n- {FENCE}bash\nls\n{FENCE}\n')
        self.assertIn('bullet holding a code fence', self.kinds())

    def test_a_bullet_holding_a_bullet_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\n- - Read the roster first.\n')
        self.assertIn('bullet holding a bullet', self.kinds())

    def test_an_empty_bullet_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\n- \n\nA sentence.\n')
        self.assertIn('empty bullet', self.kinds())

    def test_frontmatter_and_thematic_breaks_are_not_bullets(self):
        self.write('SKILL.md', '---\nname: specimen\n---\n\n# Specimen\n\nA sentence.\n\n---\n')
        self.assertEqual(self.findings(), [])

    def test_prose_over_eight_lines_is_reported(self):
        body = '\n'.join(f'Sentence {number}.' for number in range(9))
        self.write('SKILL.md', f'# Specimen\n\n{body}\n')
        self.assertIn('prose over eight lines', self.kinds())

    def test_eight_lines_of_prose_is_within_the_limit(self):
        body = '\n'.join(f'Sentence {number}.' for number in range(8))
        self.write('SKILL.md', f'# Specimen\n\n{body}\n')
        self.assertEqual(self.findings(), [])

    def test_a_long_list_is_one_structure(self):
        body = '\n'.join(f'- Item {number}.' for number in range(20))
        self.write('SKILL.md', f'# Specimen\n\n{body}\n')
        self.assertEqual(self.findings(), [])

    def test_a_long_table_is_one_structure(self):
        body = '\n'.join(f'| {number} | value |' for number in range(20))
        self.write('SKILL.md', f'# Specimen\n\n| A | B |\n| --- | --- |\n{body}\n')
        self.assertEqual(self.findings(), [])

    def test_a_wide_inline_bold_lead_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\n- **Label.**  ' + 'word ' * 25 + '\n')
        self.assertIn('inline bold lead too wide', self.kinds())

    def test_a_bold_label_on_its_own_line_has_no_width_limit(self):
        self.write('SKILL.md', '# Specimen\n\n- **Label.**\n  ' + 'word ' * 40 + '\n')
        self.assertEqual(self.findings(), [])

    def test_a_prerequisite_citation_inside_one_file_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\n## Common\n\nOne.\n\n## Spec\n\n'
                               'Read [Common](#common) first. Then run it.\n')
        self.assertIn('prerequisite citation inside one file', self.kinds())

    def test_a_prerequisite_citation_naming_its_own_file_is_reported(self):
        self.write('references/guide.md', '# Guide\n\n## Common\n\nOne.\n\n## Spec\n\n'
                                          'Read [Common](guide.md#common) first.\n')
        self.assertIn('prerequisite citation inside one file', self.kinds())

    def test_a_prerequisite_citation_crossing_a_file_is_allowed(self):
        self.write('SKILL.md', '# Specimen\n\nRead [Terms](references/guide.md#terms) first.\n')
        self.write('references/guide.md', '# Guide\n\n## Terms\n\nA sentence.\n')
        self.assertEqual(self.findings(), [])

    def test_a_selection_link_may_point_anywhere_in_its_file(self):
        self.write('SKILL.md', '# Specimen\n\n## Route\n\nUse [Spec](#spec) for the run.\n\n'
                               '## Spec\n\nA sentence.\n')
        self.assertEqual(self.findings(), [])

    def test_a_prerequisite_example_in_a_code_span_is_a_specimen(self):
        self.write('SKILL.md', '# Specimen\n\n## Common\n\nOne.\n\n'
                               '- **Rule.**  Cite it as `Read [Common](#common) first.` in the body.\n')
        self.assertEqual(self.findings(), [])

    CATALOG = '# Catalog\n\n## Commands\n\n### Fetch issue\n\nFetches one issue.\n'
    LISTING = ('# Commands\n\n## Conventions\n\n### Execution\n\nWhere every command runs.\n'
               '\n## Issues\n\n### Fetch issue\n\nFetches one issue.\n')
    MODE = '# Plan mode\n\nWhat the mode does.\n'
    PROCEDURE = '\n## Procedure\n\n1. **Open.**  The first step.\n'
    RULES = '\n## Rules\n\n- **Scope.**  One sentence.\n'

    def test_a_specification_cited_from_one_other_file_is_reported(self):
        self.write('references/catalog.md', self.CATALOG)
        self.write('references/plan.md', '# Plan\n\nRun [Fetch issue](catalog.md#fetch-issue) first.\n')
        self.assertIn('command specification with one caller', self.kinds())

    def test_a_specification_several_files_cite_stands(self):
        self.write('references/catalog.md', self.CATALOG)
        self.write('references/plan.md', '# Plan\n\nRun [Fetch issue](catalog.md#fetch-issue) first.\n')
        self.write('references/sync.md', '# Sync\n\nRun [Fetch issue](catalog.md#fetch-issue) too.\n')
        self.assertEqual(self.findings(), [])

    def test_a_specification_nobody_cites_stands(self):
        self.write('references/catalog.md', self.CATALOG)
        self.assertEqual(self.findings(), [])

    def test_a_specification_only_its_own_file_cites_stands(self):
        self.write('references/catalog.md',
                   '# Catalog\n\nRun [Fetch issue](#fetch-issue) for it.\n' + self.CATALOG[len('# Catalog\n'):])
        self.assertEqual(self.findings(), [])

    def test_a_specification_its_own_file_and_one_other_cite_stands(self):
        self.write('references/catalog.md',
                   '# Catalog\n\nRun [Fetch issue](#fetch-issue) for it.\n' + self.CATALOG[len('# Catalog\n'):])
        self.write('references/plan.md', '# Plan\n\nRun [Fetch issue](catalog.md#fetch-issue) too.\n')
        self.assertEqual(self.findings(), [])

    def test_a_catalog_entry_cited_from_one_file_is_reported(self):
        self.write('references/commands.md',
                   '# Commands\n\n## Issues\n\n### Fetch issue\n\nFetches one issue.\n')
        self.write('references/plan.md', '# Plan\n\nRun [Fetch issue](commands.md#fetch-issue) first.\n')
        self.assertIn('command specification with one caller', self.kinds())

    def test_a_heading_of_a_catalogs_conventions_is_not_a_specification(self):
        self.write('references/commands.md', self.LISTING)
        self.write('references/plan.md', '# Plan\n\nSee [Execution](commands.md#execution) for it.\n')
        self.assertEqual(self.findings(), [])

    def test_a_heading_of_a_catalogs_listing_is_a_specification(self):
        self.write('references/commands.md', self.LISTING)
        self.write('references/plan.md', '# Plan\n\nRun [Fetch issue](commands.md#fetch-issue) for it.\n')
        self.assertIn('command specification with one caller', self.kinds())

    def test_a_heading_outside_a_commands_section_is_not_a_specification(self):
        self.write('references/catalog.md', '# Catalog\n\n## Reference\n\n### Fetch issue\n\nA sentence.\n')
        self.write('references/plan.md', '# Plan\n\nSee [Fetch issue](catalog.md#fetch-issue) for it.\n')
        self.assertEqual(self.findings(), [])

    def test_a_caller_under_another_root_is_reported(self):
        elsewhere = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, elsewhere)
        catalog = self.write('references/catalog.md', self.CATALOG)
        plan = elsewhere / 'sibling' / 'references' / 'plan.md'
        plan.parent.mkdir(parents=True)
        target = os.path.relpath(catalog, plan.parent)
        plan.write_text(f'# Plan\n\nRun [Fetch issue]({target}#fetch-issue) for it.\n')
        printed = io.StringIO()
        with redirect_stdout(printed):
            status = checker.main([str(self.skill), str(elsewhere / 'sibling')])
        self.assertEqual(status, 1)
        self.assertIn('command specification with one caller', printed.getvalue())

    def test_a_conforming_mode_file_reports_nothing(self):
        self.write('references/plan-mode.md', self.MODE + self.PROCEDURE + self.RULES)
        self.assertEqual(self.findings(), [])

    def test_a_mode_section_outside_the_set_is_reported(self):
        self.write('references/plan-mode.md',
                   self.MODE + self.PROCEDURE + '\n## Findings\n\nOne sentence.\n' + self.RULES)
        self.assertIn('section outside the mode set', self.kinds())

    def test_mode_sections_out_of_order_are_reported(self):
        self.write('references/plan-mode.md', self.MODE + self.RULES + self.PROCEDURE)
        self.assertIn('mode sections out of order', self.kinds())

    def test_a_file_that_is_not_a_mode_carries_any_section(self):
        self.write('references/guide.md', '# Guide\n\n## Findings\n\nOne sentence.\n')
        self.assertEqual(self.findings(), [])

    def test_a_trailing_blank_line_is_reported(self):
        self.write('SKILL.md', '# Specimen\n\nA sentence.\n\n')
        self.assertIn('trailing blank line', self.kinds())

    def run_command(self):
        with redirect_stdout(io.StringIO()):
            return checker.main([str(self.skill), '--quiet'])

    def test_the_command_exits_non_zero_on_a_finding(self):
        self.write('SKILL.md', '# Specimen\n\nSee [guide](references/absent.md).\n')
        self.assertEqual(self.run_command(), 1)

    def test_the_command_exits_zero_when_clean(self):
        self.write('SKILL.md', '# Specimen\n\nA sentence.\n')
        self.assertEqual(self.run_command(), 0)


if __name__ == '__main__':
    unittest.main()
