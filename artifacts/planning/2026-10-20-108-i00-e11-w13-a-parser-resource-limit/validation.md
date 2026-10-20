## Overview

What was measured for `I00:E11:AC15`, and what the delivery was measured to do at `ab1165e` in the unit's worktree.

## The Signal That Was Chosen

`markdown_it` 4.2.0 declines work against `maxNesting` in two places. `ParserInline.tokenize` stops applying rules at the ceiling and takes the character as literal text; `ParserInline.skipToken` abandons a label scan to the end of the paragraph. Only the second is a reference lookup: `skipToken` is reached from `parseLinkLabel`, which is entered only where a link, an image or a definition label is being read.

A differential run decided whether watching `skipToken` alone is enough. Random nested sources of depth 15 to 40, built from link, image, reference and emphasis shapes, were parsed twice — once at a ceiling of 21 and once at 5000 — and every link and image destination compared, including those inside image alternative content.

| Measurement | Figure |
| --- | --- |
| Sources parsed | 4,000 |
| Sources whose destinations differed between the two ceilings | 987 |
| Differing sources the `skipToken` watch did not report | 0 |
| Sources the watch reported whose destinations did not differ | 8 |
| Sources reaching the `tokenize` ceiling without reaching `skipToken` | 0 of a further 1,500 |

The watch reports every source the ceiling changed the result of, and over-reports eight whose result it did not, which is the conservative direction the design permits. The `tokenize` ceiling was never reached without the label scan reaching it first, so the watch is a single override of `skipToken` rather than a copy of the parser's own loop.

## The Boundary

With `--max-nesting 1` the parser's ceiling stands at 21, which is the nesting budget plus the profile's headroom. A marked dependency under 21 open brackets resolves; one under 22 does not.

| Open brackets | Deepest level reached | Scan abandoned | Run |
| --- | --- | --- | --- |
| 19 | 18 | No | Succeeds |
| 20 | 19 | No | Succeeds |
| 21 | 20 | No | Succeeds, `plan.md` bundled |
| 22 | 21 | Yes | Fails with `E_PARSER_REFERENCE_LIMIT` at `guide.md:3` |

Before this row, the 22-bracket source succeeded and published a bundle carrying no `plan.md` and no diagnostic about it.

## The Corpus Fixtures

`fixtures/parser-limit/` states both halves of the gate against the build `PROSIFORM_BUILD` names. Both pass, and the corpus went from 203 fixtures to 205.

| Fixture | What it holds | Result |
| --- | --- | --- |
| `parser-limit/a-reference-lookup-the-parser-declines` | A marked dependency one bracket past the ceiling fails with `E_PARSER_REFERENCE_LIMIT`, naming `guide.md:3`, the chain that reached the source, and publishing nothing | Passed |
| `parser-limit/a-nesting-ceiling-the-last-valid-reference-reaches` | The same dependency exactly at the ceiling resolves, `plan.md` is bundled, and the run succeeds carrying only the entry-destination warning | Passed |

The second fixture is what a build cannot meet by failing whenever the ceiling is reached.

## The Unit Cases

Five cases were added and the unit suite went from 603 to 608.

| Test | What it holds | Result |
| --- | --- | --- |
| `test_a_lookup_the_nesting_ceiling_declines_is_reported` | The profile's parse raises `Suppressed`, carrying line 3 | Passed |
| `test_a_ceiling_reached_by_the_last_valid_reference_resolves_it` | The parse at the ceiling returns the reference resolved to `plan.md` | Passed |
| `test_a_later_parse_reads_no_earlier_declined_lookup` | A parse after a declined one returns its own links, so the watch carries no state between parses | Passed |
| `test_a_lookup_the_parser_declines_fails_the_run` | The command fails as an input failure with the code, `guide.md:3` and the chain, and publishes nothing | Passed |
| `test_a_ceiling_reached_by_the_last_valid_reference_bundles_it` | The command succeeds, bundles the plan, and reports the entry destination alone | Passed |

## The Gate

`make check` run in the unit's worktree at `ab1165e`, against the build `PROSIFORM_BUILD` names.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | Success: no issues found in 44 source files |
| `make test` | 608 passed, up from 603 by this row's five |
| `make harness` | 381 passed |
| `make corpus` | 205 fixture(s), 203 pass, 0 fail, 2 awaited, 0 unexpected pass |
| `make smoke` | Installed, resolved outside the repository, and bundled |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 34 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## The Review

The watch holds no state across parses: `parse` clears the record before each run and the content stack unwinds in a `finally`. The profile's cache keys the watch on the nesting budget, so two budgets in one process read with two parsers and two watches.

A parse of the bundle the run built is not guarded by this failure. Such a parse reaching the ceiling means the candidate the run assembled cannot be indexed by the parser that assembled it, which is an internal defect rather than a source one, and it raises and publishes nothing.

The eight conservative over-reports are sources whose brackets the ceiling abandoned a scan over and whose destinations were unchanged. A run meeting one fails naming a span its author can write the reference out of, which is the gate's own remedy, and the alternative — resolving the lookup to decide — is the lookup the ceiling declined.
