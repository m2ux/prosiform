## Overview

What this delivery was held to, the revisions each check ran against, and what each observed. The branch is `i00/e11/w30-a-suppressed-reference-lookup`, cut from `i00/e11/main` at `232a528`, and every figure below is measured against that base.

## The Boundary

The parser's ceiling sits at the declared nesting budget plus a fixed headroom of 20 levels, and inline nesting counts into it while the declared budget counts containers alone. With `--max-nesting` left at its default of 64 the ceiling stands at 84, which a source reaches by opening brackets and nesting no container at all.

| Open brackets before the reference | Observed |
| --- | --- |
| 84 | The lookup resolves and the parse returns `plan.md` |
| 85 | The lookup is declined and the parse raises |

The declining source is 135 bytes against an input budget of 16777216 and a file budget of 1048576, names one reference against a link budget of 32768, opens one source against a file budget of 256, nests no container against a nesting budget of 64, and sits one hop from the entry against an expansion budget of 8. So the boundary is reached with every declared budget at its default, which is the condition the family names and the one no fixture stated.

## The Reference the Failure Names

The declined scan stops inside a label the parser had opened. The span from that point to the end of the inline content is read with a parser of its own, under the source's definition environment, and the destination its construct spells is the reference the lookup would have made.

| Span the scan abandoned | Named |
| --- | --- |
| A label closing on an inline destination | `plan.md` |
| A label closing on a definition the source declares | `plan.md`, resolved through that definition |
| A label the span never closes | Nothing, and the source it could not index is named instead |

The span is read after the parse that abandoned it has finished, so the reading answers for the span rather than for the source: the watch belongs to the document parse and the reader carries none.

## The Corpus Fixtures

`fixtures/parser-limit/` runs against the build `PROSIFORM_BUILD` names. The corpus went from 226 passing fixtures to 228, and all four fixtures of the family pass.

| Fixture | What it holds | Result |
| --- | --- | --- |
| `parser-limit/a-lookup-suppressed-below-every-declared-budget` | An invocation naming the entry reference alone, one bracket past the ceiling, fails with `E_PARSER_REFERENCE_LIMIT`, names `plan.md` as the reference and `guide.md:3` as the span, carries the chain that reached the source, and publishes nothing | Passed |
| `parser-limit/a-budget-spent-on-the-last-valid-reference` | The same invocation exactly at the ceiling resolves that last valid reference, bundles `plan.md`, and succeeds carrying only the entry-destination warning | Passed |
| `parser-limit/a-reference-lookup-the-parser-declines` | The gate fixture, now expecting the reference the failure names | Passed |
| `parser-limit/a-nesting-ceiling-the-last-valid-reference-reaches` | The gate fixture at a lowered ceiling, unchanged | Passed |

The second fixture is what a build cannot meet by failing whenever the ceiling is reached, and the first is what it cannot meet by reaching the ceiling only when an invocation lowered it.

## The Unit Cases

Six cases were added and the build's suite went from 682 to 688. The corpus harness went from 527 to 529, which is the two new manifests validated against the schema and their declared paths required to exist.

| Test | What it holds | Result |
| --- | --- | --- |
| `test_a_declined_lookup_names_the_reference_it_would_have_made` | The raise carries `plan.md`, and the message names it | Passed |
| `test_a_declined_reference_style_lookup_names_its_definition` | A reference-style spelling resolves through the definition the source declares | Passed |
| `test_a_declined_scan_spelling_no_destination_names_no_reference` | A span whose construct never closes names nothing | Passed |
| `test_the_ceiling_is_reached_under_every_budget_at_its_default` | Both depths hold at the default nesting budget, not only at a lowered one | Passed |
| `test_a_declined_lookup_names_the_reference_under_the_default_budgets` | The command fails as an input failure carrying the code, `plan.md` and `guide.md:3`, and publishes nothing | Passed |
| `test_a_budget_spent_on_the_last_valid_reference_bundles_it` | The command succeeds, bundles the plan, and reports no suppression | Passed |

## The Gate

`make check` run in the unit's worktree against the build `PROSIFORM_BUILD` names.

| Revision | Run | Result |
| --- | --- | --- |
| `232a528`, the base | Before the change, so the result is attributable to the branch | Passed |
| `81d40bc`, the branch | After the change | Passed |

Both runs cover the lock check, lint, format, types, the build's tests, the corpus harness, the corpus, the installed-wheel smoke run, the layout, table, link and vocabulary checks, and the documented invocation.

The implementation-independence check is the repository's `make vocabulary` target, which holds every contract term the design marks to the glossary and the sources that carry it. It passes on the branch: nothing this delivery added prints a parser, package or module name, since the fixtures declare codes and the diagnostic names a reference the source itself spells.

## The Review

- **The span names a reference only where its construct completes.**
  The reading takes the first inline token of the restored span and names a destination only when that token opens a link. A span the scan stopped in part-way through a label yields text rather than a link, so the reference stays unnamed and the diagnostic falls back to the source it could not index, which is the reading the base already published.
- **The reading leaves the document parse alone.**
  The watch is cached per nesting budget and the reader carries none, so reading a span cannot record a decline of its own against the parse that raised. The existing case holding that a later parse reads no earlier declined lookup still passes.
- **The gate fixtures still state what they declare.**
  Both keep the viability-gate clause and the lowered ceiling their invocation sets. Only the failing one's expected reference moved, because the run now names the reference rather than the source, and its description states that.
