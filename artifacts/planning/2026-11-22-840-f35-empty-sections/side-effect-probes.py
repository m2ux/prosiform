import hashlib
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

repo = Path('/home/mike1/projects/dev/md-composer/.worktrees/f35-empty-sections')
sys.path.insert(0, str(repo / 'src/tests'))
from test_cli import DECLARED, invoke, written

results = []
for label, link in [
    ('explicit-title-inline', '[Doc](notes.md#notes)'),
    ('explicit-title-reference', '[Doc][target]\n\n[target]: notes.md#notes'),
    ('explicit-title-diagram', '```mermaid\nflowchart TD\nN(Doc)\nclick N href "notes.md#notes"\n```'),
    ('composed-document-reference', '[↳ Section](part.md#section)'),
]:
    with TemporaryDirectory() as folder:
        root = Path(folder)
        written(root, 'guide.md', DECLARED + '# Guide\n\n' + link + '\n')
        written(root, 'notes.md', '---\nprosiform:\n  default:\n    group: {shared: 2}\n---\n# Notes\n\n## Use\n\nContent.\n')
        written(root, 'part.md', DECLARED + '# Part\n\n## Section\n\n[Doc](notes.md)\n')
        original = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.md')}
        run = invoke('-d', 'json', 'guide.md', cwd=root)
        assert run.status == 0, (label, run.stderr)
        assert '### Notes\n' in run.bundle and 'Content.' in run.bundle, label
        assert '#notes' in run.bundle, label
        assert original == {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.md')}
        results.append({'case': label, 'status': 'pass', 'warnings': run.stderr.splitlines()})

def retain(groups, parsed, protected):
    count = sum(len(group.record.headings) for group in groups)
    return list(groups), [], {at: at for at in range(count)}

with TemporaryDirectory() as folder:
    root = Path(folder)
    fixture = repo / 'fixtures/grouping/content-beneath-an-unselected-title-sits-one-level-below-its-subsection/source'
    shutil.copytree(fixture, root, dirs_exist_ok=True)
    guide = root / 'guide.md'
    guide.write_text(guide.read_text() + '\nSee [later](tail.md#beta).\n')
    written(root, 'tail.md', '---\nprosiform:\n  default:\n    group: {tail: 2}\n---\n# Tail\n\n## Beta\n\nRetained tail content.\n')
    with patch('prosiform.cli.prune', retain):
        before = invoke('-d', 'json', 'guide.md', cwd=root)
    after = invoke('-d', 'json', 'guide.md', cwd=root)
    assert before.status == after.status == 0, (before.stderr, after.stderr)
    assert 'Retained tail content.' in before.bundle and 'Retained tail content.' in after.bundle
    before_link = next(line for line in before.bundle.splitlines() if '[later]' in line)
    after_link = next(line for line in after.bundle.splitlines() if '[later]' in line)
    results.append({'case': 'internal-link-preservation-with-pruned-sibling', 'status': 'pass', 'before_link': before_link, 'after_link': after_link, 'warnings': after.stderr.splitlines()})

from prosiform.bundle import Group
from prosiform.provenance import FILENAME_WRAPPER, Generated, Instruction, OVERVIEW_SECTION, Record, VARIANT_HEADING
from prosiform.pruning import prune
from prosiform.source import fragments

wrapper = Generated('Guide', 1, FILENAME_WRAPPER)
empty = Generated('Beta', 2, OVERVIEW_SECTION)
authored = Generated('Beta', 2, VARIANT_HEADING, (('note.md', 'beta'),))
body = Instruction('Content.')
group = Group(('# Guide', '## Beta', '## Beta', body.text), Record('guide.md', None, (wrapper, empty, authored), (empty, authored, body)))
kept, removed, positions = prune([group], {}, set())
before_anchors = fragments([heading.text for heading in group.record.headings])
after_anchors = fragments([heading.text for one in kept for heading in one.record.headings])
assert before_anchors[2] == 'beta-1' and after_anchors[positions[2]] == 'beta'
assert [one.heading for one in removed] == [empty]
results.append({'case': 'duplicate-anchor-reassignment-at-outline-stage', 'status': 'pass', 'before_anchor': before_anchors[2], 'after_anchor': after_anchors[positions[2]], 'retained_position_map': positions})
print(json.dumps(results, indent=2))
