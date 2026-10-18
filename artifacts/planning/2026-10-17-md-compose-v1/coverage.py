"""Map the design's normative clauses to the acceptance criteria claiming them.

Usage:
  python3 coverage.py [--write]

Reads design.md and every initiative and epic body in this directory, and
writes coverage.md: each design clause with the criteria that plausibly claim
it, uncovered clauses first.

The match is lexical. Two texts are related when they share distinctive terms,
meaning terms that occur in few clauses. That finds a clause no criterion
discusses; it does not prove that a criterion a clause matches actually
verifies it. The uncovered list is the result to act on; the matches are a
reading aid.
"""
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
ATX = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
LABEL = re.compile(r"^- \*\*(.+?)[:.]?\*\*\s*(.*)$")
STEP = re.compile(r"^(\d+)\.\s+(.+)$")
ROW = re.compile(r"^\|\s*`?((?:[^|`\\]|\\.)+?)`?\s*\|\s*(.+?)\s*\|\s*$")
CRITERION = re.compile(r"^- \[[ x]\] \*\*(AC\d+)\.\*\*\s*(.*)$")

# sections that state no obligation on the build: the fixture inventory the
# conformance epic owns, and the deferred upstream note no work is authorized on
EXCLUDED = {"Adversarial acceptance fixtures", "Upstream follow-up reference"}

STOP = set("""a an the and or but if then than that this these those of in on at to for from by with
as is are was were be been being it its it's into over under not no nor so such only also both each
every any some all one two three more most other another same which who whom whose what when where
how why can may must shall should would could do does did done has have had having will
rather while within without before after between through during against per via upon
its their there here them they we you your our us i he she his her
text content document documents section sections run runs
""".split())


def clauses(path):
    """Every labelled bullet, numbered step and table row in a Markdown file."""
    lines = path.read_text(encoding="utf-8").split("\n")
    inside, marker, stack, out = False, "", [], []
    for n, line in enumerate(lines, 1):
        m = FENCE.match(line)
        if m and not inside:
            inside, marker = True, m.group(1)[0] * 3
            continue
        if m and inside and m.group(1)[0] * 3 == marker:
            inside = False
            continue
        if inside:
            continue
        h = ATX.match(line)
        if h:
            lvl = len(h.group(1))
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, h.group(2)))
            continue
        section = stack[-1][1] if stack else "(opening)"
        if any(name in EXCLUDED for _, name in stack):
            continue
        for pattern, kind in ((LABEL, "clause"), (STEP, "step"), (ROW, "row")):
            m = pattern.match(line)
            if not m:
                continue
            label, body = m.group(1).strip(), m.group(2).strip()
            if kind == "row" and (set(label) <= set("- ") or label in ("Option", "Term",
                                                                      "Measure", "Exit",
                                                                      "Reference", "Part",
                                                                      "Task", "Epic", "Avoided")):
                break
            if kind == "step":
                label, body = "step %s" % label, body
            out.append({"section": section, "label": label, "body": body,
                        "line": n, "kind": kind})
            break
    return out


def criteria():
    found = []
    for path in sorted(HERE.glob("i0*.md")):
        name = path.stem.upper().replace("-", ":").replace("INITIATIVE", "")
        for line in path.read_text(encoding="utf-8").split("\n"):
            m = CRITERION.match(line)
            if m:
                found.append(("%s%s" % (name, m.group(1)), m.group(2)))
    return found


def terms(text):
    text = re.sub(r"`[^`]*`", " ", text)
    words = re.findall(r"[a-z][a-z-]{2,}", text.lower())
    return {w for w in words if w not in STOP}


def main():
    design = clauses(HERE / "design.md")
    crits = criteria()
    for c in design:
        c["terms"] = terms(c["label"] + " " + c["body"])
    crit_terms = [(name, terms(body), body) for name, body in crits]

    # a term occurring in many clauses distinguishes nothing
    spread = Counter(t for c in design for t in c["terms"])
    common = {t for t, n in spread.items() if n > len(design) // 8}

    rows = []
    for c in design:
        want = c["terms"] - common
        scored = []
        for name, ct, _ in crit_terms:
            shared = want & ct
            if len(shared) >= 2:
                scored.append((len(shared), name, sorted(shared)))
        scored.sort(reverse=True)
        rows.append((c, scored[:3]))

    uncovered = [r for r in rows if not r[1]]
    covered = [r for r in rows if r[1]]

    out = []
    out.append("# Clause Coverage\n")
    out.append("Generated by `coverage.py`. Do not edit by hand.\n")
    out.append("Every normative clause of [the design](design.md) against the acceptance "
               "criteria of the plan. The match is lexical: a criterion is listed when it "
               "shares at least two distinctive terms with the clause. That is enough to find "
               "a clause no criterion discusses, which is what the first table is for. It is "
               "not evidence that a listed criterion verifies the clause, which is what "
               "I00:E07's clause-to-fixture report establishes against the corpus.\n")
    out.append("| Measure | Value |")
    out.append("| --- | --- |")
    out.append("| Design clauses | %d |" % len(design))
    out.append("| Acceptance criteria | %d |" % len(crits))
    out.append("| Clauses no criterion matches | %d |" % len(uncovered))
    out.append("")
    out.append("## Clauses no criterion matches\n")
    out.append("| Design section | Clause | Line |")
    out.append("| --- | --- | --- |")
    for c, _ in uncovered:
        out.append("| %s | %s | [%d](design.md#L%d) |"
                   % (c["section"], c["label"], c["line"], c["line"]))
    out.append("")
    out.append("## Clauses with a matching criterion\n")
    out.append("| Design section | Clause | Criteria |")
    out.append("| --- | --- | --- |")
    for c, scored in covered:
        out.append("| %s | %s | %s |"
                   % (c["section"], c["label"],
                      ", ".join("%s" % name for _, name, _ in scored)))
    out.append("")
    report = "\n".join(out)

    if "--write" in sys.argv:
        (HERE / "coverage.md").write_text(report, encoding="utf-8")
        print("coverage.md written")
    print("clauses: %d  criteria: %d  unmatched: %d"
          % (len(design), len(crits), len(uncovered)))
    for c, _ in uncovered:
        print("  %-42s %s" % (c["section"][:42], c["label"][:60]))


main()
