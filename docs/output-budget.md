# The output budget, measured

The `output-bytes` budget defaults to 262,144. The figure is an engineering default, and
the bundling it has to admit or refuse is the one the proposal used as its evidence:
the closure of Plan Mode in the `work-planner` skill, 39 documents and 318,018 bytes
read whole.

**That bundling is refused by the default.** The complete bundle is **307,209 bytes**,
45,065 over the budget, and the run publishes nothing:

```text
E_RESOURCE_LIMIT: the run reached 307209 bytes of the complete bundle, which crosses the output-bytes budget of 262144
  remedy: restructure the sources, or raise --budget output-bytes
```

The bundle is 96.6% of the bytes its sources hold: the link-reference definitions it
removes and the destinations it shortens to one fragment cost more than the one
top-level heading per document it adds. A closure of this shape therefore bundles to
about what it reads, and the default admits roughly five sixths of it.

## The closure

It is this repository's own history. The `work-planner` skill sits on the `workspace`
branch, and the proposal measured it at
[acac858](https://github.com/m2ux/prosiform/blob/acac85867ca963df00251e4cf00a4db11b14bf24/skills/work-planner/modes/plan-mode.md),
so the tree is recovered from a clone rather than fetched from elsewhere. The 39
documents are the skill's own 38 plus `skills/guidelines.md`, which
`skills/work-planner/guidelines.md` cites from the directory above. That document's
derived boundary is therefore `skills/` rather than the skill, and the run below is made
from `skills/` so that every path it names sits under its working directory.

## The tree as it stands

The skill was written for an agent that follows links by reading prose rules, so its
closure is the Markdown link graph it already carries. prosiform's closure is the same
graph, because a reference naming a Markdown document that declares `prosiform` is a
dependency and nothing else is. The measured commit predates the declaration, so the
re-taking below opens each of the 39 documents with `prosiform: {}`; that block is
frontmatter the bundle drops, and every other byte is measured as its author wrote it.

One more reference needs a hand. `skills/work-planner/guidelines.md` names
`SKILL.md#command-conventions`, a heading `SKILL.md` does not carry at that commit, and
a reference naming a heading its declaring target does not carry is refused with
`E_TARGET_NOT_FOUND`, so
the run publishes nothing. Pointing it at the document carries `SKILL.md`, and the
three documents reachable only through it, into the closure the proposal counted.

Left undeclared, `skills/guidelines.md` is a citation the bundle carries as text, and
the closure is 38 documents and **291,227 bytes** — still 29,083 over the budget.

## Re-taking it

From a clone of this repository, with `<build>` the command line of the build under
test:

```bash
mkdir -p /tmp/closure
git archive acac858 skills/work-planner skills/guidelines.md | tar -x -C /tmp/closure
sed -i 's|(SKILL.md#command-conventions)|(SKILL.md)|' /tmp/closure/skills/work-planner/guidelines.md
cd /tmp/closure/skills
find . -name '*.md' -print0 | xargs -0 perl -0pi -e 's/\A---\n/---\nprosiform: {}\n/ or s/\A/---\nprosiform: {}\n---\n/'
<build> work-planner/modes/plan-mode.md
```

The run is refused, so the figure is read off the refusal: `limits.Crossed` carries the
budget, the limit and the counted figure, and the diagnostic reports all three. Raising
`output-bytes` publishes the bundle, and its size on disk equals the figure the
refusal named.

## What the measurement settles

The default refuses a real closure of the kind the tool was built for. Whether to raise
it is a decision about what a calling agent can hold in one message, not about this
tree — but it is now taken against a number. A budget of 327,680 admits this bundling
with 5% of headroom, which is the order the default reaches to admit the material
prosiform exists to bundle.
