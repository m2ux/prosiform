"""Check a skill's markdown against the shared skill guidelines.

Resolution and layout are checked together because a reader meets them
together: a link that resolves to nothing and a bullet that swallowed its
code fence both cost the reader the content they were promised.

Fenced blocks and code spans hold specimen text, so a link inside one is a
placeholder rather than a reference, and a heading inside one belongs to the
template it illustrates rather than to the document. A template's `{{...}}`
stands for text the author supplies, so it is measured where it lands rather
than here.

Placement is judged by use. A command specification belongs to the procedure
that runs it, so a specification exactly one other file cites names a caller
it should be sitting in. A mode file's top-level sections are the set the
guidelines name, in the order they name them, so the reader knows what the
file carries before opening it.

A prerequisite citation is recognised by the canonical form the guidelines
state, `Read [Name](target) first.`, which separates it from a selection
link naming the next operation. A selection link points wherever its target
sits; a prerequisite citation names a section the reader must already hold,
so its target belongs in another file.

    python3 skills/scripts/check_skill_files.py skills/workflow-canon
"""

import argparse
import re
import sys
from pathlib import Path

FENCE = re.compile(r'^\s*(```|~~~)')
RULE = re.compile(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$')
HEADING = re.compile(r'^(#{1,6})\s+(.*)$')
LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
CODE_SPAN = re.compile(r'`[^`]*`')
PLACEHOLDER = re.compile(r'\{\{.*\}\}|\{[a-z_]+\}|^[.…\s]*$')
PREREQUISITE = re.compile(r'Read ((?:\[[^\]]+\]\([^)]+\)(?:,\s*)?)+) first\.')
BULLET = re.compile(r'^(\s*)-(\s*)(.*)$')
BOLD_LEAD = re.compile(r'^\s*-\s+\*\*')
BARE_LEAD = re.compile(r'^\s*-\s+\*\*[^*]+\*\*\s*$')
INDENTED = re.compile(r'^\s+\S')
PROSE_LIMIT = 8
LEAD_WIDTH = 100
MODE_SECTIONS = ('Prerequisites', 'Procedure', 'Reference', 'Rules', 'Commands')


def anchor_of(text):
    """GitHub's slug for a heading, which is what a fragment link must match."""
    return re.sub(r'[\s_]+', '-', re.sub(r'[^\w\s-]', '', text.strip().lower()))


def scan(path):
    """Each line with the fence state it sits in, and the file's headings."""
    lines = path.read_text().splitlines()
    fenced = []
    inside = False
    for line in lines:
        if FENCE.match(line):
            fenced.append(True)
            inside = not inside
            continue
        fenced.append(inside)
    headings = [(index, len(match.group(1)), match.group(2))
                for index, line in enumerate(lines)
                if not fenced[index] and (match := HEADING.match(line))]
    return lines, fenced, headings


def frontmatter(lines):
    """Line indices of a leading YAML block, whose delimiters are not rules."""
    if not lines or lines[0].strip() != '---':
        return set()
    for index, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            return set(range(index + 1))
    return set()


def targets(path, lines, fenced):
    """Every link target outside fences and code spans, with its line."""
    for index, line in enumerate(lines):
        if fenced[index]:
            continue
        for target in LINK.findall(CODE_SPAN.sub('', line)):
            if '://' in target or target.startswith('mailto:') or PLACEHOLDER.search(target):
                continue
            yield index, target


def cited(paths):
    """Which files cite each fragment of each file, so use is judged by caller."""
    found = {}
    for path in paths:
        lines, fenced, _ = scan(path)
        for _, target in targets(path, lines, fenced):
            name, _, fragment = target.partition('#')
            if not fragment:
                continue
            destination = (path.parent / name).resolve() if name else path
            found.setdefault(destination, {}).setdefault(anchor_of(fragment), set()).add(path)
    return found


def specifications(headings):
    """Each command specification: a sub-section of a Commands section, or of a
    catalog, whose title makes the whole file one."""
    catalog = any(level == 1 and anchor_of(title) == 'commands' for _, level, title in headings)
    inside = catalog
    for index, level, title in headings:
        if level == 3 and inside:
            yield index, title
        elif level < 3 and not catalog:
            inside = level == 2 and anchor_of(title) == 'commands'


def check(path, root, cache, used):
    lines, fenced, headings = scan(path)
    skip = frontmatter(lines)
    where = path.relative_to(root)
    found = []

    def report(index, kind, detail=''):
        found.append((str(where), index + 1, kind, detail))

    def anchors(target):
        if target not in cache:
            cache[target] = {anchor_of(title) for _, _, title in scan(target)[2]}
        return cache[target]

    callers = used.get(path, {})

    seen = {}
    previous = 0
    for index, level, title in headings:
        slug = anchor_of(title)
        if slug in seen and slug in callers:
            report(index, 'duplicate anchor is cited', f'{slug}, also at line {seen[slug] + 1}')
        seen.setdefault(slug, index)
        if previous and level > previous + 1:
            report(index, 'heading jump', f'h{previous} to h{level}')
        previous = level

    # A specification belongs to the procedure that runs it, so a catalog
    # entry one other file cites is a specification standing away from home.
    for index, title in specifications(headings):
        elsewhere = {caller for caller in callers.get(anchor_of(title), ()) if caller != path}
        if len(elsewhere) == 1:
            caller = elsewhere.pop().relative_to(root)
            report(index, 'command specification with one caller', f'{title}, cited from {caller}')

    # A mode file's top-level sections are a named set in a named order, so
    # the reader knows what the file carries before opening it.
    if path.name.endswith('-mode.md'):
        rank = -1
        for index, level, title in headings:
            if level != 2:
                continue
            if title.strip() not in MODE_SECTIONS:
                report(index, 'section outside the mode set', title.strip())
                continue
            place = MODE_SECTIONS.index(title.strip())
            if place < rank:
                report(index, 'mode sections out of order',
                       f'{MODE_SECTIONS[place]} after {MODE_SECTIONS[rank]}')
            rank = max(rank, place)

    for index, target in targets(path, lines, fenced):
        name, _, fragment = target.partition('#')
        destination = (path.parent / name).resolve() if name else path
        if not destination.is_file():
            report(index, 'unresolved link', target)
        elif fragment and destination.suffix == '.md' and anchor_of(fragment) not in anchors(destination):
            report(index, 'unresolved anchor', target)

    for index, line in enumerate(lines):
        if fenced[index] or index in skip or RULE.match(line):
            continue
        if match := BULLET.match(line):
            gap, rest = match.group(2), match.group(3)
            if not rest.strip():
                report(index, 'empty bullet')
            elif not gap:
                report(index, 'bullet without a space', line.strip()[:60])
            elif FENCE.match(rest):
                report(index, 'bullet holding a code fence', line.strip()[:60])
            elif BULLET.match(rest):
                report(index, 'bullet holding a bullet', line.strip()[:60])
        if (BOLD_LEAD.match(line) and not BARE_LEAD.match(line)
                and '{{' not in line and len(line) > LEAD_WIDTH):
            report(index, 'inline bold lead too wide', f'{len(line)} characters, limit {LEAD_WIDTH}')

        # A prerequisite citation asserts the reader already holds a section.
        # Within one file position carries that, so the citation states an
        # order the reader has passed and the section it names must be elsewhere.
        for sentence in PREREQUISITE.findall(CODE_SPAN.sub('', line)):
            for target in LINK.findall(sentence):
                name, _, fragment = target.partition('#')
                if not fragment or PLACEHOLDER.search(target):
                    continue
                destination = (path.parent / name).resolve() if name else path
                if destination == path:
                    report(index, 'prerequisite citation inside one file', target)

    # Bounded prose: consecutive prose lines, lists and tables excluded
    # because each is one structure and is not split to meet the limit.
    run = 0
    start = 0
    for index, line in enumerate(lines):
        structural = (fenced[index] or index in skip or not line.strip()
                      or line.lstrip().startswith(('-', '|', '>', '#', '*'))
                      or INDENTED.match(line))
        if structural:
            run = 0
            continue
        start = index if run == 0 else start
        run += 1
        if run == PROSE_LIMIT + 1:
            report(start, 'prose over eight lines', 'split into named sub-sections')

    if lines and not lines[-1].strip():
        report(len(lines) - 1, 'trailing blank line')
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('roots', nargs='+', help='skill folders to check')
    parser.add_argument('--quiet', action='store_true', help='print the counts alone')
    options = parser.parse_args(argv)

    files = []
    for name in options.roots:
        root = Path(name).resolve()
        files += [(path, root.parent) for path in sorted(root.rglob('*.md'))]

    used = cited([path for path, _ in files])
    cache = {}
    findings = []
    for path, root in files:
        findings += check(path, root, cache, used)

    if not options.quiet:
        for where, line, kind, detail in findings:
            print(f'{where}:{line}: {kind}' + (f' — {detail}' if detail else ''))
    print(f'{len(files)} files checked, {len(findings)} findings')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
