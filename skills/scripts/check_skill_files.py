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
that runs it, so a specification exactly one file cites, that file not the
one holding it, names a caller it should be sitting in. One test decides
every citing file alike, the file holding the specification included: a file
is a caller where a procedure of it carries the citation. A procedure is a
top-level section carrying a numbered step, whatever its heading names it:
the step is the author stating that the reader performs these, in this
order, and is the only place a file records that. Prose runs nothing
whatever its mood, order or count, so a sibling specification, a statement
of what a command does, and a sentence routing three commands in sequence
all name a command without running it. A skill's entry point holds no
command of its own, so a
specification standing there is reported wherever it is cited from. A mode
file's top-level sections are the set the guidelines name, in the order they
name them, Procedure and Rules among them, so the reader knows what the file
carries before opening it.

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
ORDERED = re.compile(r'^\s{0,3}\d+[.)]\s')
BULLET = re.compile(r'^(\s*)-(\s*)(.*)$')
BOLD_LEAD = re.compile(r'^\s*-\s+\*\*')
BARE_LEAD = re.compile(r'^\s*-\s+\*\*[^*]+\*\*\s*$')
INDENTED = re.compile(r'^\s+\S')
PROSE_LIMIT = 8
LEAD_WIDTH = 100
MODE_SECTIONS = ('Prerequisites', 'Procedure', 'Reference', 'Rules', 'Commands')
MODE_REQUIRED = ('Procedure', 'Rules')


def anchor_of(text):
    """GitHub's slug for a heading, which is what a fragment link must match."""
    return re.sub(r'[\s_]+', '-', re.sub(r'[^\w\s-]', '', text.strip().lower()))


def named(path, root):
    """A path as a finding names it: relative to the root given where it lies
    under it, and whole otherwise, since the roots checked together may have
    different parents and a citation may cross between them."""
    return path.relative_to(root) if path.is_relative_to(root) else path


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


def specifications(headings):
    """Each command specification: a sub-section of a Commands section, or of a
    listing of a catalog, whose title makes the whole file one. A catalog's
    Conventions section states how its commands run, so it lists none."""
    catalog = any(level == 1 and anchor_of(title) == 'commands' for _, level, title in headings)
    inside = catalog
    for index, level, title in headings:
        if level == 3 and inside:
            yield index, title
        elif level == 2:
            inside = (anchor_of(title) != 'conventions' if catalog
                      else anchor_of(title) == 'commands')
        elif level == 1 and not catalog:
            inside = False


def specification_spans(headings, total):
    """Line indices held by the file's command specifications. A specification
    states how one command runs, so a citation standing in it names a sibling
    operation rather than running it, and its own numbered detail is part of
    that statement."""
    spans = set()
    for start, _ in specifications(headings):
        end = next((index for index, level, _ in headings
                    if index > start and level <= 3), total)
        spans.update(range(start, end))
    return spans


def procedure_spans(lines, fenced, headings):
    """Line indices held by the file's procedures. A procedure is a top-level
    section carrying a numbered step, whatever its heading names it, and runs
    until the next heading of its own level or above, so the steps under a
    sub-heading belong to it. A command specification is neither, so its lines
    are read out before the steps are counted."""
    specifications_here = specification_spans(headings, len(lines))
    tops = [index for index, level, _ in headings if level <= 2]
    spans = set()
    for position, start in enumerate(tops):
        end = tops[position + 1] if position + 1 < len(tops) else len(lines)
        body = [index for index in range(start, end) if index not in specifications_here]
        if any(ORDERED.match(lines[index]) and not fenced[index] for index in body):
            spans.update(body)
    return spans


def citations(paths):
    """Which files cite each fragment of each file, and which of them run it.
    A file is a caller where a procedure of it carries the citation, and the
    same question is asked of every citing file."""
    cited = {}
    called = {}
    for path in paths:
        lines, fenced, headings = scan(path)
        steps = procedure_spans(lines, fenced, headings)
        for index, target in targets(path, lines, fenced):
            name, _, fragment = target.partition('#')
            if not fragment:
                continue
            destination = (path.parent / name).resolve() if name else path
            anchor = anchor_of(fragment)
            cited.setdefault(destination, {}).setdefault(anchor, set()).add(path)
            if index in steps:
                called.setdefault(destination, {}).setdefault(anchor, set()).add(path)
    return cited, called


def check(path, root, cache, cited, called):
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

    citing_files = cited.get(path, {})
    callers = called.get(path, {})

    seen = {}
    previous = 0
    for index, level, title in headings:
        slug = anchor_of(title)
        if slug in seen and slug in citing_files:
            report(index, 'duplicate anchor is cited', f'{slug}, also at line {seen[slug] + 1}')
        seen.setdefault(slug, index)
        if previous and level > previous + 1:
            report(index, 'heading jump', f'h{previous} to h{level}')
        previous = level

    # A specification belongs to the procedure that runs it, so one exactly
    # one procedure cites, in a file other than its own, stands away from
    # home. The file holding the specification is read by that same test. A
    # skill's entry point holds no command, so a specification there is
    # reported whatever cites it, which is the one placement no caller count
    # can reach.
    for index, title in specifications(headings):
        if path.name == 'SKILL.md':
            report(index, 'command specification in the entry point', title)
            continue
        citing = callers.get(anchor_of(title), ())
        if len(citing) == 1 and path not in citing:
            caller = named(next(iter(citing)), root)
            report(index, 'command specification with one caller', f'{title}, cited from {caller}')

    # A mode file's top-level sections are a named set in a named order, and
    # carry the two the guidelines make mandatory, so the reader knows what
    # the file carries before opening it.
    if path.name.endswith('-mode.md'):
        sections = [(index, title.strip()) for index, level, title in headings if level == 2]
        rank = -1
        for index, title in sections:
            if title not in MODE_SECTIONS:
                report(index, 'section outside the mode set', title)
                continue
            place = MODE_SECTIONS.index(title)
            if place < rank:
                report(index, 'mode sections out of order',
                       f'{MODE_SECTIONS[place]} after {MODE_SECTIONS[rank]}')
            rank = max(rank, place)
        carried = {title for _, title in sections}
        for required in MODE_REQUIRED:
            if required not in carried:
                report(0, 'mode section missing', required)

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

    cited, called = citations([path for path, _ in files])
    cache = {}
    findings = []
    for path, root in files:
        findings += check(path, root, cache, cited, called)

    if not options.quiet:
        for where, line, kind, detail in findings:
            print(f'{where}:{line}: {kind}' + (f' — {detail}' if detail else ''))
    print(f'{len(files)} files checked, {len(findings)} findings')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
