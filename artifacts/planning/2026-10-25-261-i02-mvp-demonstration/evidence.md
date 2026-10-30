# Evidence

The measured baseline the plan stands on, and the gaps the measurements exposed.

## Baseline

Measured in the prosiform checkout (`md-composer/.project/main`) at commit `bd3b0665` on branch `main`. Every figure below is a command's output on that commit.

| Measure | Value | How it was measured |
| --- | --- | --- |
| Example tree size | 4 Markdown files | `find example/work-tracker -name '*.md'` |
| Example files carrying `prosiform` frontmatter | 4 | `grep -rl "^prosiform:" example` |
| Usage-example fixtures | 5 | `ls fixtures/usage-example` |
| `modes/plan-mode.md` bundle | 5,057 bytes | `pf -o out.md modes/plan-mode.md` from the example directory |
| Authored links left in that bundle | 2 | the two `»` dispatch links, which retain their working-directory-relative destination by contract |
| Repository checks | `make check` exits 0 | 1099 unit tests, 626 harness tests, every other target green |
| Corpus | 260 fixtures, 260 pass | `checks/corpus.py` with `PROSIFORM_BUILD` naming the build |

The example bundles and its fixtures are green on this commit, so no defect in the example motivates the migration. Two facts do.

- **A four-file tree cannot show the construct its users write.**
  One routing document, one mode and two artifacts reach no protocol, no second mode, and no folder holding more than two members.

- **The replacement tree's premise is measured, not assumed.**
  The skill holds 49 Markdown files and 346,559 bytes of Markdown, which exceeds the 262,144-byte default output budget, so a whole-tree bundle is impossible and per-mode bundling is forced.

## The replacement tree's current incompatibility

The skill the example is to carry declares no conversion metadata: `grep -rl "^prosiform:"` over `skills/work-planner` returns nothing across its 49 files. Bundled today, a mode of that tree leaves 116 authored `../` link occurrences unresolved, over 82 distinct targets.

The cause is the root rule, not the grouping rule. A file that declares no `prosiform.root` resolves its links from the invocation working directory, so `../artifacts/issue.md` climbs out of the allowed source root, and the contract leaves such a link authored and contributes nothing. The migration epic's `root: ".."` declaration on each folder is what closes this.

## Measured shape of the migration epic's target

A synthetic four-folder tree was built to the migration epic's specification and bundled from a mode, to test whether the epic's grouping model works without the open Parent Merge defect.

| Construct | Result |
| --- | --- |
| Group declared on a member file | Member nested beneath the file that links it, at the declared depth |
| Two members in one group | One merged group; each member's preamble under `Overview`, each named by a subsection |
| `group-heading: false` | Group name omitted; members stay at `H2` |
| Protocol group at depth 1 | Group heading emitted, protocol content directly beneath |
| Mode as the entry | The `modes` group is absent and the mode's own title leads the bundle |
| Authored links remaining | 0 |

The last row is the one that matters for planning: the model produces a resolving bundle without the Parent Merge change, so that change is not a prerequisite for the demonstration.

## Gaps the measurements found

- **G1. A mode bundle cannot demonstrate the `modes` group.**
  A mode is the entry of its own bundle, so the group its peers belong to is absent from it. The demonstration must either enter at a routing document, or accept that `modes` is shown by the second group rather than its own.

- **G2. The migration epic's file-count criterion is the only check on copy fidelity.**
  Its first criterion compares file counts between the skill and the example. A file copied with its content altered passes that comparison, so fidelity rests on the fixtures of the later rows rather than on the copy row.
