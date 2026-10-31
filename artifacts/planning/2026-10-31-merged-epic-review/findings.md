# Findings

> Findings · Created 2026-10-31

Every finding below was delivered by an epic already merged into `main` and was checked against the tree at `23882b7d`. A row names the epic that delivered it, the area of the tree it affects, and the defect in one sentence. No row records style, naming or a speculative refactor.

## Findings

| # | Epic | Scope | Problem | Severity |
| --- | --- | --- | --- | --- |
| 1 | I05:E10 | eval | `--harness cursor` crashes on every default run: `sections_of` receives a run form where `TRANSITION` is keyed by corpus form, raising `KeyError: 'bundle'` | blocker |
| 2 | I05:E10 | eval | A sub-agent's trace is discarded: `keep()` globs `trace*` while the instruction tells the sub-agent to write `trace-<section>.log` | blocker |
| 3 | I05:E04 | build | `make steps` runs last, so a broken corpus reports moved bundle bytes from `corpus` instead of the rule from `steps` | blocker |
| 4 | I05:E03 | source | A dispatch link in an absorbed document title indexes a missing placement key, raising a bare `KeyError` and exit 4 | blocker |
| 5 | I02:E02 | example | Align Mode calls Record Verified Criteria without the verification evidence it re-runs, verifying one criterion twice in one revision | blocker |
| 6 | I05:E10 | eval | The opencode harness returns `done` for every start, so a dispatched question is unobservable and its cell is admitted rather than withheld | major |
| 7 | I05:E10 | eval | The opencode token guard reads only the last step, undercounting a session's spend by all but its final step | major |
| 8 | I05:E07 | eval | The Cursor harness crashes on the default form list, from the same run-form against corpus-form mismatch | major |
| 9 | I05:E07 | eval | `sequential_set` passes a record in which the set was split across two messages | major |
| 10 | I05:E07 | eval | A compiled step that restates its dispatch in prose escapes the guard, which inspects numbered lines only | major |
| 11 | I05:E05 | build | `make test` precedes `authoring`, so a file-relative link break reports a target-not-found code instead of naming the file and rule | major |
| 12 | I05:E06 | checks | The command-placement rule ignores an unlabelled fence and a code-span command, both of which the guidelines forbid | major |
| 13 | I05:E06 | checks | The Inputs rule accepts a step anchor as a contract section and skips an operation whose body is one bullet | major |
| 14 | I05:E04 | checks | A step at its procedure's own level passes, because the parent is taken as the nearest shallower heading | major |
| 15 | I05:E04 | checks | The duplicate-step rule compares heading text, not the anchor slug it claims to guard | major |
| 16 | I05:E04 | checks | The numbered-item pattern misses the `1)` and indented ordered-list forms the build refuses | major |
| 17 | I05:E04 | example | `plan-mode.md` names a step by role rather than by link, leaving AC5 unmet in the mode that epic rewrote | major |
| 18 | I05:E03 | source | A regular file standing at `<entry>.bundles` is renamed aside and unlinked: exit 0, unrelated bytes destroyed | major |
| 19 | I05:E02 | source | A `links` array renders live anchors in Mermaid but decodes to a list, so the run bundles neither document and exits 0 | major |
| 20 | I05:E02 | source | Any `<a href>` on a fence line is refused as a node label, including a `click` tooltip and a pie or sequence label | major |
| 21 | I05:E02 | fixture | The AC11 fixture ships a bundle Mermaid cannot parse, and the render check omits that fixture | major |
| 22 | I05:E01 | fixture | The linked form ships its own flowchart carrying the branch labels, so it cannot measure link-following | major |
| 23 | I05:E01 | eval | A budget-stopped run whose started sessions all errored reports `completed` with a 0% table | major |
| 24 | I05:E01 | eval | `--write-baseline` accepts a run that started nothing and cuts the committed baseline to zero cells | major |
| 25 | I05:E00 | source | A line carrying a second `click` matches neither, so both destinations escape rewriting and source paths publish | major |
| 26 | I02:E03 | example | The architecture overview says a written overview is kept while the protocol rewrites it on every run | major |
| 27 | I02:E03 | example | The board path's evidence-completeness guard can never fire, so a pull request titled without its initiative prefix is invisible | major |
| 28 | I02:E02 | source | A titled parent's whole-document reference resolves inside its own first section at grouping depth 1 | major |
| 29 | I02:E02 | docs | `docs/hierarchy.md` states the retired group-heading rule on the page a reader lands on for groups | major |
| 30 | I02:E01 | example | The example README states eighteen artifacts where the bundle it describes carries twenty | major |
| 31 | I02:E01 | example | No document on `main` names the `demo/i02` revision a reader must repeat the demonstration on | major |
| 32 | I02:E00 | example | Thirty-nine command blocks name a script path the example and the repository do not carry | major |
| 33 | I02:E00 | source | The coincidence warning skips a merged group's heading and the collision refusal ignores group names | major |
| 34 | I02:E00 | example | The step-verb rule the epic stated is broken by operation links using Use and through verbs | major |
| 35 | I01:E06 | source | The declared byte bound does not bound decoder work: a base-prefixed integer costs quadratic time inside the bound | major |
| 36 | I01:E06 | source | A root-not-found diagnostic reports a bare path segment, with no reference and no remedy | major |
| 37 | I01:E06 | source | Two distinct group names title-case to the same empty heading and publish as indistinguishable H1s | major |
| 38 | I01:E02 | source | Two title-case conventions in one bundle: one helper destroys separators where the other keeps them | major |
| 39 | I01:E02 | source | A member heading can be empty, emitting an empty heading and an empty-fragment destination with no diagnostic | major |
| 40 | I01:E02 | source | The overview wrapper is emitted with no above-depth content to carry, against AC1 | major |
| 41 | I05:E10 | eval | The unbootstrapped verdict is unreachable, and a bare `pf` with no arguments counts as a compile | minor |
| 42 | I05:E10 | eval | A diamond-drawn workflow loses the wrong-branch verdict, and a section's own routing goes unchecked | minor |
| 43 | I05:E10 | eval | The plain-box rule that distinguishes an escape from a transition is unenforced | minor |
| 44 | I05:E07 | eval | Heading-only matching lets a non-dispatch start satisfy a dispatch | minor |
| 45 | I05:E07 | docs | The eval README states a matrix count the corpus no longer holds | minor |
| 46 | I05:E05 | eval | A settings file that is not valid UTF-8 escapes the preflight as a decode error rather than a refusal | minor |
| 47 | I05:E06 | example | The planning-record artifact states the record-folder rule twice, the second a duplicated paragraph | minor |
| 48 | I05:E06 | example | The engineering branch and records folder are hard-coded where the configuration document owns them | minor |
| 49 | I05:E06 | example | The documented artifact count contradicts the bundle the page quotes | minor |
| 50 | I05:E06 | fixture | A fixture description states eight artifacts where its bundle carries twelve | minor |
| 51 | I05:E04 | example | The delivery-evidence child section opens straight onto its first step, against the guideline it serves | minor |
| 52 | I05:E04 | checks | The checks README states coverage the step guard does not have | minor |
| 53 | I05:E03 | source | A deferred dispatch mark with no text publishes an empty link, evading the empty-text refusal | minor |
| 54 | I05:E03 | source | The dispatch instruction line does not escape the bundle filename it interpolates | minor |
| 55 | I05:E03 | checks | The runner still counts two of the contract's outcomes after a third was added | minor |
| 56 | I05:E03 | checks | The manifest reader no longer holds the per-code rule its README states | minor |
| 57 | I05:E02 | checks | The render check's pass oracle reimplements slugs more weakly than the build does | minor |
| 58 | I05:E02 | docs | The references page says `click` applies in any diagram, where four grammars accept it | minor |
| 59 | I05:E02 | source | Refusals are yielded before being ordered, so the reported line depends on which family broke first | minor |
| 60 | I05:E01 | docs | The loop-miscount class fires for under-looping as well as over-looping, against the reference wording | minor |
| 61 | I05:E01 | eval | The committed baseline lacks the linked form the criterion requires | minor |
| 62 | I05:E01 | eval | A silent agent that wrote a trace is scored normally, contradicting three statements of when errored applies | minor |
| 63 | I05:E00 | docs | The link budget states and prints a set that excludes the diagram clicks it now counts | minor |
| 64 | I05:E00 | fixture | The specimen's carried-as-written section click is resolved and rewritten | minor |
| 65 | I05:E00 | checks | The link check blanks fenced blocks whole, so a click naming a missing document passes | minor |
| 66 | I02:E03 | example | Every board command hard-codes a user board where the rule admits an organisation board | minor |
| 67 | I02:E03 | example | The artifact-count criterion is unguarded and the count it asserts is already false | minor |
| 68 | I02:E02 | fixture | Two usage fixtures cite parent-arrangement coverage they cannot exercise | minor |
| 69 | I02:E01 | example | The README's run-from-the-root instruction contradicts the command section's skill-directory instruction | minor |
| 70 | I02:E01 | example | At the tag, the compiled-links construct has no exception for the dispatch mark its own bundle carries | minor |
| 71 | I02:E00 | checks | The link check joins paths raw, rejecting percent-encoded links the build decodes | minor |
| 72 | I02:E00 | docs | The skill declares Python 3.10 against the build's 3.13 | minor |
| 73 | I02:E00 | example | The guidelines require a structure file and a shared skill check the repository lacks | minor |
| 74 | I01:E06 | source | Signed base-prefixed integers read as strings, blinding the duplicate-key guard | minor |
| 75 | I01:E06 | source | The target budget never counts withheld targets, though the run reads and confirms them | minor |
| 76 | I01:E06 | checks | A metadata-preservation test asserts a path nothing writes, so it cannot fail | minor |
| 77 | I01:E06 | checks | The checks README describes the root-ownership guard this epic deleted | minor |
| 78 | I01:E02 | source | A parent's whole-document destination degrades silently to an unrelated variant heading | minor |
| 79 | I01:E02 | source | A member's duplicate section text produces two identical variant headings, unwarned | minor |

## Disposition

| Column | Meaning |
| --- | --- |
| # | Stable finding number, assigned in the review and never reused |
| Epic | The epic that delivered the finding |
| Scope | The area of the tree it affects |
| Problem | The defect in one sentence |
| Severity | `blocker`, `major` or `minor` |
| Where | The task in the delivering epic, or the epic that took the finding elsewhere |

## Where Each Finding Goes

| Task | Scope | Findings |
| --- | --- | --- |
| W01 | build | 3, 11 |
| W02 | source | 4, 18 |
| W03 | source | 19, 20, 25 |
| W04 | source | 37, 39 |
| W05 | source | 28, 38, 40 |
| W06 | source | 35, 36 |
| W07 | eval | 1, 8 |
| W08 | eval | 6, 7 |
| W09 | eval | 9, 23, 24 |
| W10 | eval | 21, 22, 61 |
| W11 | example | 5, 26, 27 |
| W12 | example | 30, 31 |
| W13 | example | 17, 29, 81 |

Findings 10, 12, 13, 14, 15, 16, 33, 34, 52, 55, 56, 65, 71, 76 and 77 are rules the design or a check states imprecisely, which the epic [I01:E03](https://github.com/m2ux/prosiform/issues/187) holds by its own stated boundary. Finding 32 is taken by [I06:E00](https://github.com/m2ux/prosiform/issues/406), whose Problem names the same command lines.

## Totals

| Severity | Recorded | In this epic | Elsewhere |
| --- | --- | --- | --- |
| blocker | 5 | 5 | 0 |
| major | 36 | 28 | 8 |
| minor | 41 | 8 | 33 |
| **total** | **82** | **41** | **41** |

## Corroboration

Three findings were reached independently by more than one epic's reviewer, which separates a real defect from an artefact of one reading.

| Finding | Rows | Readers |
| --- | --- | --- |
| The example README's artifact count is eighteen where the bundle carries twenty | 30, 49, 67 | I02:E01, I05:E06, I02:E03 |
| The checks README describes a guard the code no longer holds | 56, 77 | I05:E03, I01:E06 |
| The Cursor harness crashes on the default form list | 1, 8 | I05:E10, I05:E07 |

## Patterns

- **Reach narrower than the stated rule.** Eleven findings across six epics are guards that state a rule broader than the cases they inspect.
- **A criterion that enumerates documents.** Five findings are a rule changed in code and in the documents the criterion named, but left standing in an unlisted page.
- **The example is read but never run.** Six findings follow from validating the example skill as documents alone.
