"""The installed prose API exposes complete inputs and directed reading paths."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'scripts'))
import check_skill_files as checker


class DocumentInterfaces(unittest.TestCase):
    def test_prerequisites_match_direct_required_reads(self):
        for folder in ('modes', 'artifacts', 'protocols'):
            for path in sorted((ROOT / folder).glob('*.md')):
                with self.subTest(file=path.name):
                    lines, fenced, headings = checker.scan(path)
                    section = None
                    declared, used = set(), set()
                    by_line = {i: title for i, level, title in headings if level == 2}
                    sections = {}
                    for i in range(len(lines)):
                        section = by_line.get(i, section)
                        sections[i] = section
                    for i, target in checker.targets(path, lines, fenced):
                        name = target.partition('#')[0]
                        if not name:
                            continue
                        destination = (path.parent / name).resolve()
                        if destination == path:
                            continue
                        if sections[i] == 'Prerequisites':
                            declared.add(destination)
                        elif sections[i] in ('Procedure', 'Operations', 'Fields',
                                             'Outcomes', 'Commands'):
                            used.add(destination)
                        if folder == 'artifacts':
                            self.assertNotIn(destination.parent.name, ('modes', 'protocols'), target)
                    self.assertEqual(declared, used)

    def test_artifact_operations_expose_inputs_and_consecutive_steps(self):
        for path in sorted((ROOT / 'artifacts').glob('*.md')):
            lines, fenced, headings = checker.scan(path)
            section = None
            for position, (start, level, title) in enumerate(headings):
                if level == 2:
                    section = title
                if section != 'Operations' or level != 3:
                    continue
                with self.subTest(file=path.name, operation=title):
                    end = next((i for i, depth, _ in headings[position + 1:] if depth <= 3), len(lines))
                    body = lines[start + 1:end]
                    self.assertGreaterEqual(len(title.split()), 3)
                    self.assertTrue(any(line.startswith('**Inputs:**') for line in body))
                    numbers = [int(m[1]) for line in body if (m := re.match(r'^(\d+)\. ', line))]
                    if numbers:
                        self.assertGreater(len(numbers), 1)
                        self.assertEqual(numbers, list(range(1, len(numbers) + 1)))
                    else:
                        self.assertEqual(len([line for line in body if line.startswith('- ')]), 1)
                    self.assertFalse(any(re.match(r'^(?:\d+\. |\- )\*\*', line) for line in body))
                    self.assertFalse(any(line.startswith(('Result:', '**Result:')) for line in body))

    def test_references_cannot_route_to_modes_or_artifacts(self):
        for path in (ROOT / 'references').glob('*.md'):
            lines, fenced, _ = checker.scan(path)
            for _, target in checker.targets(path, lines, fenced):
                name = target.partition('#')[0]
                self.assertNotIn((path.parent / name).resolve().parent.name,
                                 ('modes', 'artifacts', 'protocols'))

    def test_protocols_are_entered_whole(self):
        """A protocol is one coordinated sequence, so a caller runs the file
        rather than reaching into a step of it."""
        for folder in ('modes', 'protocols'):
            for path in sorted((ROOT / folder).glob('*.md')):
                lines, fenced, _ = checker.scan(path)
                for _, target in checker.targets(path, lines, fenced):
                    name, _, fragment = target.partition('#')
                    if not name:
                        continue
                    destination = (path.parent / name).resolve()
                    if destination.parent.name == 'protocols' and destination != path:
                        with self.subTest(file=path.name, target=target):
                            self.assertEqual(fragment, '')
