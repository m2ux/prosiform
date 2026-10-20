# The output budget, measured

`--max-output-bytes` defaults to 262,144. The figure is an engineering default, and
the bundling it has to admit or refuse is the one the proposal used as its evidence:
the closure of Plan Mode in the `work-planner` skill, 39 documents and 318,018 bytes
read whole.

**That bundling is refused by the default.** The complete bundle is **311,022 bytes**,
48,878 over the budget, and the run publishes nothing:

```text
E_RESOURCE_LIMIT: the run reached 311022 bytes of the complete bundle, which crosses the --max-output-bytes budget of 262144
  remedy: restructure the sources, or raise --max-output-bytes
```

The bundle is 97.8% of the bytes its sources hold: one top-level heading per document
and the rewritten destinations cost less than the marks removed from the references.
A closure of this shape therefore bundles to about what it reads, and the default
admits roughly four fifths of it.

## The closure

It is this repository's own history. The `work-planner` skill sits on the `workspace`
branch, and the proposal measured it at
[acac858](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/modes/plan-mode.md),
so the tree is recovered from a clone rather than fetched from elsewhere. The 39
documents are the skill's own 38 plus `skills/guidelines.md`, which one of them cites
from the directory above, which is why the root below is `skills/` and not the skill.

## Marking

The skill declares no dependencies: it carries no `¬` anywhere, because it was written
for an agent that follows links by reading prose rules. Its closure is the Markdown
link graph, and prosiform's closure is the marked references, so measuring one against
the other means marking the tree. Every reference naming a Markdown file the root
carries becomes a dependency; a reference leaving the root, naming an absent file, or
sitting inside a fenced code block stays a citation, since none of those is material
the bundling could reach.

One reference needs a hand. `skills/work-planner/guidelines.md` names
`SKILL.md#command-conventions`, a heading `SKILL.md` does not carry at that commit, so
marked it is refused with `E_TARGET_NOT_FOUND` and the run publishes nothing. Pointing
it at the document is what carries `SKILL.md`, and the three documents reachable only
through it, into the closure the proposal counted. Left as a citation instead, the
closure is 35 documents and **292,514 bytes**, still 30,370 over the budget.

The root is `skills/` rather than the skill for the same reason the closure is 39 and
not 38: `guidelines.md` cites `../guidelines.md`, and a marked reference the root
cannot contain is refused with `E_SOURCE_OUTSIDE_ROOT`.

## Re-taking it

From a clone of this repository, with `<build>` the command line of the build under
test:

```bash
mkdir -p /tmp/closure
git archive acac858 skills/work-planner skills/guidelines.md | tar -x -C /tmp/closure
python3 mark.py /tmp/closure/skills
sed -i 's|(SKILL.md#command-conventions)|(SKILL.md)|' /tmp/closure/skills/work-planner/guidelines.md
<build> --root /tmp/closure/skills work-planner/modes/plan-mode.md
```

`mark.py` is the marking pass described above, written anywhere outside the extracted
tree:

```python
import re
import sys
from pathlib import Path

MARK = "¬"
LINK = re.compile(r"(?<!!)\[([^\]\[]*)\]\(([^()\s]+)\)")
FENCE = re.compile(r"^\s*(```|~~~)")


def reachable(path, root, target):
    if target.startswith(("http://", "https://", "mailto:", "#", "/")):
        return False
    head = target.split("#", 1)[0]
    if not head.endswith(".md"):
        return False
    resolved = (path.parent / head).resolve()
    return resolved.is_file() and root.resolve() in resolved.parents


def mark(path, root):
    out, fenced = [], False
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if FENCE.match(line):
            fenced = not fenced
            out.append(line)
            continue
        if fenced:
            out.append(line)
            continue
        out.append(
            LINK.sub(
                lambda m: m.group(0)
                if m.group(1).startswith(MARK) or not reachable(path, root, m.group(2))
                else "[" + MARK + m.group(1) + "](" + m.group(2) + ")",
                line,
            )
        )
    path.write_text("".join(out), encoding="utf-8")


root = Path(sys.argv[1])
for document in sorted(root.rglob("*.md")):
    mark(document, root)
```

The run is refused, so the figure is read off the refusal: `limits.Crossed` carries the
budget, the limit and the counted figure, and the diagnostic reports all three. Raising
`--max-output-bytes` publishes the bundle, and its size on disk equals the figure the
refusal named.

## What the measurement settles

The default refuses a real closure of the kind the tool was built for. Whether to raise
it is a decision about what a calling agent can hold in one message, not about this
tree — but it is now taken against a number. A budget of 327,680 admits this bundling
with 5% of headroom, which is the order the default reaches to admit the material
prosiform exists to bundle.
