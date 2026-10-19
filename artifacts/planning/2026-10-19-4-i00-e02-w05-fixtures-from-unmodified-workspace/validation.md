# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, recording the output, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w05-fixtures-from-unmodified-workspace` |
| Tested revision | `c58469f8e46f0530726c44808c14410e8beab86f` |
| Base revision | `60b67b3` on `i00/e02/main`, the build the before-and-after corpus runs compare against |
| Contract revision | `d70b05a` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Source of the copies | `skills/` of the `md-composer` workspace, held upstream in `m2ux/workflow-server` on branch `workspace` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Build under test | `prototype/.venv/bin/prosiform`, named to the corpus runner as `PROSIFORM_BUILD` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and `uv run --frozen` builds the project into the environment it runs in, so every `make` run below was performed outside the session's sandbox, which has no network and no write access to the `uv` cache. The corpus runs, the accounting runs and the byte-identity run were performed inside it.

This task changes no source of the build. `prototype/` is untouched at this head, so the six fixtures observe the emission `I00:E02:W04` delivered, against documents that emission was not written for.

## T1 The set, in one pass

**Observes AC6.** The repository's checks run together, over a tree carrying six fixtures whose sources are copies.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The per-item `ok` lines each check prints are omitted; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.75ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
24 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 23 source files
cd prototype && uv run --frozen pytest
245 passed in 0.19s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
130 passed in 0.39s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs two hundred and forty-five tests, as it did at the base: this task adds no build code. The corpus suite runs one hundred and thirty where the base ran one hundred and twenty-four; the six are the schema validation of the six fixtures this task adds. The table check is unchanged at eleven commands and seven declarations, and the vocabulary check at thirty-four terms.

**The link check reads six documents, as it did at the base.** It reads none of the twelve Markdown files this task adds, source and expected bundle alike. The exception is the corpus, discovered as the directories that hold a `manifest.toml`, so `fixtures/real-source/` is excepted by the same rule that excepts every other family rather than by anything written for it. The copied documents carry eight fragment references between them and no reference to another document, so the exception costs nothing here — but it is what would keep a copied document's sibling links from being read, and the check confirms it holds rather than the plan assuming it.

## T2 Byte-identity of every copy against its source

**Observes AC6.** Each fixture source against the workspace skill document it was taken from.

```bash
bash identity.sh
```

The script compares the six pairs with `cmp -s` and prints the SHA-256 of each side. It is a session check rather than a repository check because its reference side lives in another repository: `skills/` is not part of `m2ux/prosiform`, so no check in this repository can reach it.

**Pass.** Exit 0. Six pairs, each identical, each digest equal:

```text
2bd697ce3df16c907bca4461027c12e46486e71cf0a3580a505dd8758e26598f  skills/work-planner/artifacts/repository-labels.md
                                                                  fixtures/real-source/absorbed-title-and-self-references/source/artifacts/repository-labels.md
a9f3ecbc2272fb811c325df3d376f6d99b74acca397a1280641f8dc1dbb296ca  skills/workflow-canon/templates/integration-review.md
                                                                  fixtures/real-source/tables-and-brace-placeholders/source/templates/integration-review.md
a4d6e8003c4a822c380b0e81b2fa0d642612236c734a9d51834e362c4be52f33  skills/gitnexus/gitnexus-impact-analysis/SKILL.md
                                                                  fixtures/real-source/frontmatter-and-a-shifted-group/source/gitnexus-impact-analysis/SKILL.md
9ae8afc051fcf49a239e075a58a7a6278aa94768767e88354cae2d0cb82d02a6  skills/workflow-canon/references/design-flow.md
                                                                  fixtures/real-source/preamble-above-the-first-heading/source/references/design-flow.md
e28f79d4ea2473efa0f197611a75bc25428fb4296aeeb54d1e31de2e39ccd8ad  skills/gitnexus/gitnexus-cli/SKILL.md
                                                                  fixtures/real-source/heading-text-outside-ascii/source/gitnexus-cli/SKILL.md
70205d8405f94c7e45b487f01d55138ee618334bcfcad274a74de84f1b96285e  skills/work-planner/artifacts/architecture-overview.md
                                                                  fixtures/real-source/markdown-inside-a-code-example/source/artifacts/architecture-overview.md
byte-identity: exit 0
```

## T3 The corpus against the build, before and after

**Observes AC6.** Every fixture in the corpus, run against the build under test and compared with its manifest, at the base revision and at the tested revision.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python corpus.py .
```

**Pass, as a measurement.** The base run reports **30 of 32 fixtures pass**; the run at this head reports **36 of 38**. The six this task adds all pass:

```text
real-source/absorbed-title-and-self-references: pass
real-source/frontmatter-and-a-shifted-group: pass
real-source/heading-text-outside-ascii: pass
real-source/markdown-inside-a-code-example: pass
real-source/preamble-above-the-first-heading: pass
real-source/tables-and-brace-placeholders: pass

36 of 38 fixtures pass
```

The two failing at the base still fail, unchanged and untouched: `extraction/nested-section-target` wants section selection, which is `I00:E03`, and `normalization/root-escape` wants reference traversal, which is `I00:E04`.

## T4 Each expected bundle accounted against the contract

**Observes AC6.** The difference between each copied document and the bundle recorded for it, every line of it explained by a clause the contract names.

```bash
python verify.py prototype/src fixtures/real-source fixtures.txt
```

An expected bundle produced by running the build and saving the output asserts only that the build does what it does. This check reads the two files the fixture holds and runs no build. Whole-document bundling permits exactly seven changes, and the check holds each bundle to them:

| Clause | What the check requires |
| --- | --- |
| Frontmatter policy, steps 1 through 5 | One leading byte-order mark and one leading `---` block removed, and nothing else removed from the head |
| Entry line | The first line is `This bundle was built for [{escaped path}](#{slug of path}); everything else is material it references.`, followed by one blank line |
| File-scoped hierarchy, the file heading | The third line is `# {escaped path}`, the path with the Markdown suffix removed and each construct-opening character backslashed, followed by one blank line |
| File-scoped hierarchy, Absorbed title | Where the source's only H1 slugs to the final path segment, that one line is absent from the bundle and no heading is shifted |
| File-scoped hierarchy, Group shift | Otherwise every emitted ATX heading carries exactly one more `#` than the source wrote, and no other line changes |
| Block boundaries | Blank runs between document-level blocks are reported with the content line they follow, and a blank run opening the group fails |
| Validation and failure contract, Preservation | The bundle's content lines are the source's content lines, in order, each identical or shifted by one, none added and none lost |

**Pass.** Exit 0. Zero unaccounted differences across the six.

```text
== absorbed-title-and-self-references  1189 source bytes, 1329 bundle bytes
   ENTRY-LINE  This bundle was built for [artifacts/repository-labels](#artifactsrepository-labels); everything else is material it references.
   FILE-HEADING  # artifacts/repository-labels
   ABSORBED  # Repository Labels
   SHIFT  0 heading(s) moved down one level
   CONTENT  25 content line(s) carried, none added or lost
== tables-and-brace-placeholders  2149 source bytes, 2291 bundle bytes
   FILE-HEADING  # templates/integration-review
   ABSORBED  # Integration Review
   SHIFT  0 heading(s) moved down one level
   CONTENT  27 content line(s) carried, none added or lost
== frontmatter-and-a-shifted-group  2919 source bytes, 2835 bundle bytes
   FILE-HEADING  # gitnexus-impact-analysis/SKILL
   FRONTMATTER  4 line(s) removed, the block
   SEPARATION  1 blank line(s) above the first region
   SHIFT  8 heading(s) moved down one level
   CONTENT  69 content line(s) carried, none added or lost
== preamble-above-the-first-heading  3144 source bytes, 3275 bundle bytes
   FILE-HEADING  # references/design-flow
   ABSORBED  # Design Flow
   SHIFT  0 heading(s) moved down one level
   CONTENT  49 content line(s) carried, none added or lost
== heading-text-outside-ascii  3445 source bytes, 3315 bundle bytes
   FILE-HEADING  # gitnexus-cli/SKILL
   FRONTMATTER  4 line(s) removed, the block
   SEPARATION  1 blank line(s) above the first region
   SHIFT  9 heading(s) moved down one level
   CONTENT  52 content line(s) carried, none added or lost
== markdown-inside-a-code-example  6013 source bytes, 6161 bundle bytes
   FILE-HEADING  # artifacts/architecture-overview
   ABSORBED  # Architecture Overview
   SHIFT  0 heading(s) moved down one level
   CONTENT  102 content line(s) carried, none added or lost

unaccounted differences: 0
```

What was read, clause by clause, and what it establishes:

- **The file heading.** Six paths, each carrying one `/` and no other character the escaping touches, so each file heading is the path verbatim with the `.md` removed. `gitnexus-impact-analysis/SKILL` and `gitnexus-cli/SKILL` keep the capitalised final segment the filesystem holds, as the suffix rule requires: the suffix is classified case-insensitively and the name is not.
- **The escaping.** No selected path needs a backslash, which is itself the observation: workspace filenames are lowercase, hyphenated and ASCII, so the escaping clause has no real-source case. `identity/path-needing-escaping` remains its only coverage.
- **The absorbed title.** Four of the six have an H1 whose slug is the final path segment, and in all four it is absent from the bundle and no heading moves. `markdown-inside-a-code-example` is the one that earns its place here: its H1 is the only H1 in the document only because the `# Architecture Overview — {{Change Name}}` inside its four-backtick fence is a code example and not a heading. Had the parser counted it, there would be two H1s, no absorption, and a shifted group — so the absorption this bundle records is evidence that the fence held.
- **The shift.** Two of the six are headed by a path whose final segment is `SKILL`, which no title can slug to, so every heading moves down one level: eight in one, nine in the other, reaching H4. Each shifted line differs from its source by exactly one `#`, in the first three characters, with the heading text untouched — including the five headings of `gitnexus-cli/SKILL.md` that carry an em dash.
- **The entry line.** Six lines, each naming the file heading's visible text as link text and the slug of that text as its destination. `/` is punctuation the slugging discards, so `artifacts/repository-labels` resolves at `#artifactsrepository-labels`; that is the renderer's own rule and T5 confirms it resolves in the bundle.
- **The region boundaries.** None of the six carries two consecutive blank lines, so the normalisation of a blank run to one is a no-op in every one of them and no inter-region gap changed. The blank line above the first region is dropped twice, in the two documents whose frontmatter leaves one, and the blank line beneath an absorbed title goes with the title. The collapse of a longer run is uncovered by real source and stays with the authored fixtures.
- **The frontmatter.** Two documents open on a four-line `---` block; the block, its delimiters and the closing delimiter's terminator are gone and the body below it is intact, the first blank line of that body included as a line the group does not carry.
- **The trailing newline.** Six bundles, each ending in exactly one.

## T5 Every destination in each bundle resolves

**Observes AC6.** The published bundle reparsed, its headings walked under the renderer's ordinal rule, and every internal reference in it required to name one of them.

```bash
python verify.py prototype/src fixtures/real-source fixtures.txt
```

**Pass.** Exit 0, in the same run as T4.

```text
absorbed-title-and-self-references   8 destination(s), 3 fragment reference(s), each resolving
tables-and-brace-placeholders        9 destination(s), 1 fragment reference(s), each resolving
frontmatter-and-a-shifted-group      9 destination(s), 1 fragment reference(s), each resolving
preamble-above-the-first-heading     2 destination(s), 1 fragment reference(s), each resolving
heading-text-outside-ascii          10 destination(s), 1 fragment reference(s), each resolving
markdown-inside-a-code-example      17 destination(s), 7 fragment reference(s), each resolving
```

No destination occurs twice in any bundle, so no ordinal is assigned and no ordinal is needed. The references counted include the entry line's own link, so each of the six says what its reader finds. Eight of the fourteen are the documents' own section references, carried unchanged and still resolving because the headings they name survive at the same slug.

## F1 The shift applied to a group whose title is absorbed

`bundle.py` reduced to `by = SHIFT`, so a group absorbs its title and shifts the rest.

```text
real-source/absorbed-title-and-self-references: fail
real-source/frontmatter-and-a-shifted-group: pass
real-source/heading-text-outside-ascii: pass
real-source/markdown-inside-a-code-example: fail
real-source/preamble-above-the-first-heading: fail
real-source/tables-and-brace-placeholders: fail

23 of 38 fixtures pass
```

The four fixtures whose titles are absorbed fail and the two shifted groups are unaffected, which is the division the fixtures were chosen for. Reverted.

## F2 The frontmatter not stripped

`source.py` returning the whole text, so a leading block reaches the bundle as body.

```text
real-source/absorbed-title-and-self-references: pass
real-source/frontmatter-and-a-shifted-group: fail
real-source/heading-text-outside-ascii: fail
real-source/markdown-inside-a-code-example: pass
real-source/preamble-above-the-first-heading: pass
real-source/tables-and-brace-placeholders: pass

30 of 38 fixtures pass
```

Exactly the two documents that carry frontmatter fail. Reverted.

## F3 A word changed inside a carried region of an expected bundle

One word of `preamble-above-the-first-heading/expected/stdout.md` altered, with its source left alone. This is the fault the accounting exists to catch, because the corpus comparison would report it as a byte difference without saying which clause it broke.

```text
FAIL UNACCOUNTED  '… A single arrow is a transformation. A double arrow is a comparison.\n'
               -> '… A single arrow is a transform. A double arrow is a comparison.\n'
unaccounted differences: 1
```

Reverted.

## F4 A content line removed from an expected bundle

One table row of the same expected bundle deleted.

```text
FAIL UNACCOUNTED  the source carries 50 content line(s) and the bundle 48
unaccounted differences: 1
```

The count is fifty against forty-eight rather than fifty against forty-nine because the absorbed title is credited only when the bundle is one content line short of the source; two lines short, and the absorption is not credited either. The check fails for the right reason and reports a count rather than the line, which is a weakness of the message and not of the check. Reverted.

## F5 A document whose self-reference names the title the file heading absorbs

A document written for this case only, outside `fixtures/`, carrying `[Repository Labels](#repository-labels)` under `# Repository Labels` at `artifacts/repository-labels.md`.

```text
   ABSORBED  # Repository Labels
   CONTENT  3 content line(s) carried, none added or lost
   DESTINATIONS  2 emitted heading(s), each destination once
   FAIL REFERENCES  unresolved: ['repository-labels']
```

The accounting passes and the resolution check fails, which is what makes the two checks worth running separately: the build broke no clause of the emission and still published a bundle carrying a link to nothing. **No workspace document does this** — all eighty-five were checked — so this is a hazard the corpus does not carry rather than a defect a real document exposed. It is recorded under Findings as a design question about what an absorbed title does to a reference that names it.

## T6 Continuous integration

**Observes AC6.** The checks run by the workflow on the pushed head rather than in the session.

```bash
gh run list --repo m2ux/prosiform --branch i00/e02/w05-fixtures-from-unmodified-workspace
```

**Pass.** Run `39250633006` on `c58469f`, conclusion `success`.

## T7 The epic base after the merge

**Observes AC6.** The checks run on `i00/e02/main` once this task's pull request merges into it.

```bash
gh run list --repo m2ux/prosiform --branch i00/e02/main
```

**Pass.** Pull request `#54` merged as `56ad50f`, a merge commit, with `mergeStateStatus` `CLEAN` and the head check `Checks` already `success` on `c58469f`. Run `39251700519` on `56ad50f` reports conclusion `success`. The epic base was brought up to date with `origin/main` before the merge and was already up to date.

## The Documents Selected

Six documents, from four of the workspace's skills, 1.2 KB to 6.0 KB, 18.9 KB in all.

| Fixture | Document | Constructs it contributes |
| --- | --- | --- |
| `absorbed-title-and-self-references` | `work-planner/artifacts/repository-labels.md` | Absorbed title; ordered list; two fenced `bash` examples whose `<owner>`, `<repo>` and `<label>` placeholders the parser never offers as text; emphasis delimiters excluded from heading text; two fragment-only self-references still resolving |
| `tables-and-brace-placeholders` | `workflow-canon/templates/integration-review.md` | Absorbed title with no preamble; two six-column pipe tables; headings ending in a `{{…}}` brace block, which is prose because a heading attribute is spelled `{#…}`; nested list; no code |
| `frontmatter-and-a-shifted-group` | `gitnexus/gitnexus-impact-analysis/SKILL.md` | YAML frontmatter removed; a title the path cannot name, so eight headings move down one level; blockquote; column-padded tables whose cells carry `<5 symbols` and `>15 symbols`; a fenced checklist whose `- [ ]` markers are a code example |
| `preamble-above-the-first-heading` | `workflow-canon/references/design-flow.md` | Absorbed title above five blocks of preamble; three pipe tables; two fenced diagrams carrying `-->`, `<-->` and `-.->`; en dash, em dash, middle dot and arrows in body text |
| `heading-text-outside-ascii` | `gitnexus/gitnexus-cli/SKILL.md` | YAML frontmatter; nine headings shifted, reaching H4; five heading texts carrying an em dash; three column-padded tables; a one-line preamble |
| `markdown-inside-a-code-example` | `work-planner/artifacts/architecture-overview.md` | A four-backtick fence holding a three-backtick fence holding a `---` block, carrying an H1 that must count as no heading or the title could not be absorbed; blockquote; pipe table; seventeen headings; six fragment-only self-references |

**Why several small documents rather than a few large.** An expected bundle is a file in the corpus that a person opens and reads, and a 25 KB document makes a 25 KB expected bundle. The largest here is 6.1 KB and the median 3.0 KB. Twenty-eight of the eighty-five documents are larger than the largest selected; each was rejected where it carried nothing a smaller document already carries.

**Why two documents this project did not write.** `skills/gitnexus` is vendored. A document composed under another house style — padded table columns, checklists inside code fences, arrows in prose, a `SKILL.md` filename the title cannot name — is stronger evidence that ordinary Markdown bundles than one written by the hands that wrote the contract.

## The Documents Rejected

| Document | Size | Rejected because | Unblocked by |
| --- | --- | --- | --- |
| `work-planner/protocols/review-pull-request.md` | 1.8 KB | Nine links to sibling documents. The contract traverses them and the closure of this fixture is one file, so the correct expected result is `E_TARGET_NOT_FOUND`, not the bundle this build publishes | `I00:E04` |
| `workflow-canon/references/reporting.md` | 7.0 KB | Six sibling links. It is the **only** workspace document carrying a tilde fence, and that fence holds headings, pipe tables and a link that must not be read as structure | `I00:E04` |
| `work-planner/modes/plan-mode.md` | 8.4 KB | Forty sibling links. It is the document the design's own usage example names | `I00:E04` |
| `work-planner/guidelines.md`, `work-planner/modes/revise-mode.md`, `workflow-canon/references/guidelines.md`, `workflow-canon/references/revise-mode.md`, `workflow-canon/references/coverage.md` | 3.5–23.9 KB | The five documents whose links leave their skill directory, each reaching `skills/guidelines.md` through `../guidelines.md` or `../../guidelines.md`. They cannot be bundled from a skill root at all | `I00:E04`, and a root the caller widens |
| `work-planner/artifacts/board.md`, `delivery-branches.md`, `issue.md`, `pull-request.md`, `epic-issue-body.md`, `initiative-issue-body.md` | 11.0–24.8 KB | Size. `board.md`, `delivery-branches.md` and `issue.md` carry no sibling link and would have been eligible; each would put an 11 to 18 KB expected bundle in the corpus for constructs the selected six already carry | — |
| `workflow-canon/test/fixtures/audit-qualification/**`, eleven documents | 85 B–2.4 KB | They are another skill's test fixtures. They would have supplied the two things no prose in the workspace does — a document with no H1 at all, and an eighty-nine-character path — but a source authored for a test is the category this task exists to get away from | A real document acquiring either property |
| The remaining fifty-odd | — | Carry no construct the selected six do not, or carry sibling links | — |

## Findings

What a real document exposed. Each is reported rather than fixed, and none caused a document to be edited.

### Build boundaries a real document meets

- **A bundle names documents it does not carry, and says nothing.** Every work-planner mode, protocol and artifact document links to siblings: `deliver-mode.md` carries seventy-seven, `plan-mode.md` forty, `review-pull-request.md` nine. Run against a tree holding only the entry document, the build exits 0 and publishes a bundle whose links point at files the reader does not have. This is the same success-shaped failure `normalization/root-escape` records, on ordinary documents rather than an adversarial one, and it is why the family admits only documents whose closure is themselves. `I00:E04`.
- **The design's usage example names a root too narrow for its own entry.** `design.md` spells `prosiform --root skills/work-planner modes/plan-mode.md`. Walking that entry's local Markdown links to a fixed point gives a closure of forty-nine documents. Forty-eight are present under `skills/work-planner`. The forty-ninth is `../guidelines.md`, reached from `guidelines.md` and from `modes/revise-mode.md`, and it normalises to `skills/guidelines.md` — above the root the example names. Once traversal exists, the design's own usage example fails with `E_SOURCE_OUTSIDE_ROOT`. The contract already says the root must contain the closure, and that a refused reference says the root is too narrow at least as often as it says the link is wrong; the example does not follow that rule. **A design gap: the example should root at `skills/`, or the design should say why a skill directory is not a root.**
- **No real document reaches `E_RAW_HTML` or `E_HEADING_DEPTH_OVERFLOW`.** No raw HTML, block or inline, occurs in any of the eighty-five, confirming the brief's reading of `work-planner` and extending it to the rest. No document's deepest heading plus a shift reaches H6; the deepest emitted level in the whole workspace is H4. Both codes keep only authored coverage.

### Constructs the profile names and the workspace does not carry

All eighty-five documents were parsed under the profile. Eight constructs have no instance anywhere, so no real-source fixture can cover them and the authored fixtures remain their only coverage: **double-tilde strikethrough** (the one `~~` in the workspace opens a tilde fence), **indented code blocks**, **thematic breaks**, **Setext headings**, **reference-link definitions and reference-style uses**, **images**, **ordinary autolinks**, and **task-list markers outside a code fence** — every `- [ ]` in the workspace is inside a fence, `gitnexus-impact-analysis/SKILL.md`'s included.

Three more have no eligible instance: a **tilde fence** occurs in one document, which carries six sibling links; **no document combines a shifted group with a heading-like code example**, so the clause that leaves heading-like text in code untouched under a shift has no real-source case; and **no document carries two headings whose slugs collide**, so the ordinal rule has none either.

This is the strongest single observation of the task. The contract's profile is wider than the prose it was written for: **more than half of what `skill-markdown-v1` declares has no instance in the eighty-five documents the tool exists to bundle.** That is not an argument for narrowing the profile — a document acquiring a strikethrough tomorrow must still bundle — but it is an argument for saying so, and `design.md` currently reads as though the profile describes the corpus.

### Design questions a real document raises

- **A reference naming an absorbed title resolves to nothing.** The contract says an absorbed title "is not emitted, contributes no destination segment, and is not a target". A document that opens `# Repository Labels` and refers to `[Repository Labels](#repository-labels)` — an ordinary pattern — therefore names no target once the file heading absorbs that title, and today the build publishes the dead link with exit 0 and no diagnostic (F5). The contract has two answers available and names neither: the reference could resolve to the file heading, which names the same thing, or it could fail with `E_TARGET_NOT_FOUND`. **A design gap.** No workspace document does this, so it is a hazard rather than an observed break; `I00:E04` is where the reference would first be resolved at all.
- **A heading carrying non-ASCII punctuation slugs differently from GitHub.** `gitnexus-cli/SKILL.md` has five headings of the form `analyze — Build or refresh the index`. `slug()` discards ASCII punctuation only, so the em dash survives and the slug is `analyze-—-build-or-refresh-the-index` where GitHub produces `analyze--build-or-refresh-the-index`. No bundle in this family is affected, because a divergent slug becomes a destination only when something references that heading, and nothing does. `I00:E03:AC7` owns it, and this is the real-source case it did not have.
- **The workspace's own naming convention makes a routing document's title unabsorbable.** Absorption compares the title's slug with the literal final path segment, so `SKILL.md`, whose segment is `SKILL`, can never absorb any title: `slug("Skill")` is `skill`. Nine documents in the workspace are named `SKILL.md`. None of them is titled "Skill", so nothing is lost today, but the rule's case-sensitivity is reachable by a convention the workspace already follows rather than by a contrived filename. Worth a line in the contract rather than a change.

### A weakness in this task's own instrument

The accounting reports a deleted content line as a count rather than naming the line (F4), because the absorbed title is credited by a length comparison that a second missing line defeats. The check fails correctly; the message is poorer than it should be. The instrument is a session script and is not committed, so this is a note for whoever writes the corpus runner's own preservation check rather than debt in the repository.
