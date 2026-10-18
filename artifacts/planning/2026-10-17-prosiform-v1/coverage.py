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

# Clauses a criterion claims as a set rather than by name, and clauses that
# state no obligation of their own. Each entry is a judgement, so it is written
# here and reported rather than dropped: the report lists these separately, and
# an entry naming a criterion that no longer exists is a failure of the run.
COLLECTIVE = [
    ("Markdown and source-heading profile", "Typography", "I00:E02:AC5"),
    ("CLI contract", "--diagnostics", "I00:E06:AC7"),
    ("Section extraction and output hierarchy", "Subsections", "I00:E03:AC1"),
    ("Section extraction and output hierarchy", "Containers", "I00:E03:AC1"),
    ("Compile before publishing", "step", None),
    ("Self-reference and ancestor-reference behavior", "Shared dependency", "I00:E04:AC2"),
    ("Self-reference and ancestor-reference behavior", "Whole-document selection", "I00:E04:AC4"),
    ("Frontmatter policy", "step", "I00:E02:AC2"),
    ("Link classification and resource handling", "Images and non-Markdown resources",
     "I00:E04:AC13"),
    ("Resolution sequence", "step", "I00:E04:AC6"),
    ("Resolution sequence", "", "I00:E04:AC6"),
    ("Resource limits", "--max-", "I00:E04:AC7"),
    ("Validation and failure contract", "Completeness", "I00:E04:AC7"),
    ("Exit status and JSON diagnostics", "", "I00:E02:AC4"),
]

# why a clause carrying no criterion states no obligation of its own
NARRATIVE = {
    "Compile before publishing": "the order the stages run in; each stage's "
                                 "obligation is stated in its own section",
}


def collective_for(clause):
    for section, prefix, criterion in COLLECTIVE:
        if clause["section"] == section and clause["label"].startswith(prefix):
            return criterion, NARRATIVE.get(section)
    return False, None


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
        name = path.stem.replace("-initiative", "").upper().replace("-", ":")
        for line in path.read_text(encoding="utf-8").split("\n"):
            m = CRITERION.match(line)
            if m:
                found.append(("%s:%s" % (name, m.group(1)), m.group(2)))
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

    uncovered, collective, covered = [], [], []
    for clause, scored in rows:
        if scored:
            covered.append((clause, scored))
            continue
        criterion, why = collective_for(clause)
        if criterion is False:
            uncovered.append((clause, scored))
        else:
            collective.append((clause, criterion, why))

    known = {name for name, _, _ in crit_terms}
    stale = sorted({c for _, _, c in COLLECTIVE if c and c not in known})
    if stale:
        raise SystemExit("coverage.py names criteria that no longer exist: "
                         + ", ".join(stale))

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
    out.append("| Clauses claimed as a set | %d |" % len(collective))
    out.append("")
    out.append("## Clauses no criterion matches\n")
    out.append("| Design section | Clause | Line |")
    out.append("| --- | --- | --- |")
    for c, _ in uncovered:
        out.append("| %s | %s | [%d](design.md#L%d) |"
                   % (c["section"], c["label"], c["line"], c["line"]))
    out.append("")
    out.append("## Clauses claimed as a set\n")
    out.append("A criterion binds these together rather than by name, or the clause "
               "states no obligation of its own. Each row is a judgement recorded in "
               "`coverage.py`, and the run fails if one names a criterion that no "
               "longer exists.\n")
    out.append("| Design section | Clause | Claimed by |")
    out.append("| --- | --- | --- |")
    for c, criterion, why in collective:
        out.append("| %s | %s | %s |"
                   % (c["section"], c["label"], criterion or why or "--"))
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
    print("clauses: %d  criteria: %d  claimed as a set: %d  unmatched: %d"
          % (len(design), len(crits), len(collective), len(uncovered)))
    for c, _ in uncovered:
        print("  %-42s %s" % (c["section"][:42], c["label"][:60]))


main()
