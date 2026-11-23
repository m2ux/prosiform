# Inline Brief Plan

## Confirmed Goal

The user requests the same brief decorator and bundling strategy for inline and dispatch, with the execution destination as their distinguishing boundary. Inline points to a local section; dispatch points to a separate bundle. A plain reference does not acquire the decorator.

The request is planning only. No compiler source, fixture expectations or installed package changes in this phase. The classifier manual-review gate remains open.

## Expected Forms

| Authored call | Caller bundle | Execution destination |
| --- | --- | --- |
| Plain reference | Ordinary included target, with no brief decorator | Local target |
| Inline reference selecting a brief | Named section using dispatch's brief lead, execution-link position and child-section order | Local selected target in the same bundle |
| Dispatch selecting the same brief | The same named section and brief layout | Independently compiled target bundle |

The execution marker retains inline versus dispatch meaning. A local inline call uses the current agent and current model. A dispatch retains its capability map and sub-agent handoff. No prose instruction is invented to narrate the graph or duplicate the target Contract.

## Compiler Boundaries

- **Selection:** reuse effective preset and brief resolution in src/prosiform/closure.py. Default, named overrides, substitutions and refusal of conflicting briefs have the same owner for both calls.
- **Placement and content:** share the existing brief placement/emission in src/prosiform/dispatch.py and src/prosiform/composition.py. A resolved execution destination varies; a second brief renderer does not.
- **Inclusion and links:** retain ordinary target grouping and canonical local destinations through src/prosiform/bundle.py, rewrite.py and cli.py. An inline call adds no independently emitted bundle. Source-relative dependencies and composed children retain their own source context.
- **Provenance:** keep generated and authored regions attributable through src/prosiform/provenance.py and candidate.py. Existing pruning protects addressed identities and authored structure.
- **Contract:** update the current public operator, brief and invocation owners in docs and the engineering design contract. Code comments name the implementing owner rather than repeating another unit's rule.

These are affected responsibilities, not a demand to edit every listed module. The implementation uses the smallest shared path that satisfies the output contract.

## Sequence

1. **Specify paired fixtures.** Use one brief-bearing target reached by plain, inline and dispatch links, from prose and a diagram. Include direct document and selected-section calls. Record the expected decorator and exact local execution destination. Demonstrate the released compiler's missing inline behavior.
2. **Implement one shared decoration path.** Generalize call placement and execution-link resolution while preserving the dispatch output. Keep target inclusion within the caller for inline. Add focused tests for the shared selector, placement and destination maps.
3. **Complete contract and regression coverage.** Update canonical docs, guide, design and only the expectations affected by the new behavior. Run the focused tests and full make check. Retain failures and the final command log.
4. **Publish review evidence.** Provide source and both compiled variants with every child bundle linked. Open a draft delivering PR against main through Work Planner. Compiler review precedes package adoption or classifier rewrites.

This is one bounded compiler change. If the implementation proves to require independent language redesign or several hours of work, re-plan its separate deliverables before beginning a large implementation run.

## Regression Matrix

| Area | Required observations |
| --- | --- |
| Operator comparison | Plain lacks decorator; inline and dispatch share its ordered content; only the execution boundary differs |
| Entry and target selection | Whole-document and fragment targets; default and named brief; same effective selections share as their existing rules specify |
| Source forms | Markdown, reference-style links and clickable graph nodes |
| Selection and substitutions | Named override, identical selections, distinct preset selections, stub substitutions and source-relative dependency rewrites |
| Nested calls | Inline body and brief containing inline or dispatched calls; child bundle inventory reflects real dispatches only |
| Grouping | Shared fields and rules retain canonical ownership; repeated calls do not multiply the target implementation |
| Structure | Unique local anchors, same-text/different-target collisions, ordinary H6 overflow, explicit cycles and current refusal codes |
| Execution identity | Inline keeps current context/model and publishes no handoff or model suffix; dispatch keeps level resolution |
| Provenance and pruning | Candidate validation, region coverage, retained link identities and narrow empty-wrapper warnings |
| No selected brief | Existing applicable inline section composition and plain-reference behavior remain governed by their own rules; no synthetic Contract is invented |

The implementation must not add a compatibility switch, a second inline-only renderer or special classifier behavior. Any conflict between a confirmed behavior and an existing public rule is resolved in that rule and its fixtures, not hidden behind a fallback.

## Evidence And Acceptance

The five-case released specimen distinguishes compilation from agent execution. It proves dispatch carries the Contract and a separate bundle, explicit inline composition carries only its selected section, and a plain reference carries the target without decoration. It does not establish native workflow reliability or speed.

For delivery, compile the paired fixtures with the exact candidate compiler, inspect local anchors and compare normalized decorator output. Run src/tests/test_brief.py, the affected dispatch/composition/display/candidate tests, the corpus and make check. Record exact source and compiler revisions. Native classifier evaluation is a later source-bound acceptance step; no paid or private-input trial is part of planning.

## Current State

Planned. No implementation branch, code changes, PR, release or classifier adoption has started.
