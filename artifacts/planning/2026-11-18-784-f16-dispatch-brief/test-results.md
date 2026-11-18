# Test Results

Results for F16 at `6d4cde584` on `f16-dispatch-brief`, run on 2026-11-18 in the unit checkout, with the docs pinning the design at `d4a467ef4`. Every fixture named below sits under `fixtures/dispatch-brief/` unless its path says otherwise.

## T1 Lifted Dispatch

`a-dispatch-to-a-target-declaring-a-brief-is-lifted-into-a-sub-section`: a `⇉` link to a target whose `default` declares a brief publishes `### ⇉ Investigate` one level below its section, after the section's own content and before its child section, holding the brief and then `[⇉ Investigate](investigate.bundle.md)`; the authored link is published as `[Investigate](#⇉-investigate)`. `a-brief-s-sections-follow-its-dispatch-line`: a brief holding a composition directive and a subsection publishes its lead content, the dispatch line, then the composed section and the subsection one level below. `a-briefed-dispatch-in-a-heading-points-at-its-sub-section`: the heading publishes the link without its mark, pointing at the sub-section. Held in `make corpus`.

## T2 Named-Preset Brief

`a-brief-in-a-named-preset-is-carried-by-the-dispatch-selecting-it`: a dispatch titled `briefed` is lifted with the brief, and a dispatch of the same target selecting no preset publishes in place with its mark. Held in `make corpus`.

## T3 Diagram Dispatch

`a-click-dispatch-to-a-target-declaring-a-brief-points-at-its-sub-section`: a Mermaid click on a node whose text opens with `⇉` is published as `click Intake href "#⇉-investigate"`. Held in `make corpus`.

## T4 Picking Dispatch

`a-picking-dispatch-carries-its-brief-around-its-pick-lines` places the brief in `⇉ Dispatch Pick` around the pick lines. `a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` and `a-picking-dispatch-to-an-alternative-declaring-a-brief-is-refused` each fail with `E_ALTERNATIVE_UNRESOLVED`, exit status 2, listing the alternatives. Held in `make corpus`.

## T5 Dispatch Set

`a-set-publishes-each-briefed-member-as-its-brief-and-its-line` and `a-set-lifts-a-briefed-member-with-children-beside-a-bare-member`: a set holding a briefed member lifts every member into a `#### ⇉ <text>` sub-section in written order, the briefed member's holding its brief's lead content, its line and its sections one level further down, the bare member's its line alone. `a-briefed-set-member-s-brief-dispatches-inside-the-member`: the brief's own dispatch publishes inside the member and the set's lines name its two members alone. `a-set-of-one-briefed-target-is-lifted-as-a-dispatch`: a set of one is lifted as a `⇉` link is. Held in `make corpus`.

## T6 Brief Compilation and Copies

`a-brief-s-links-are-followed-into-the-dispatching-bundle`: the brief's link joins the dispatching bundle and the target's bundle keeps the section unchanged. `one-brief-dispatched-at-two-depths-is-copied-at-each`, `a-brief-nested-in-a-copied-brief-is-copied-at-each` and `a-brief-dispatched-inside-two-copies-of-another-brief-is-copied-at-each`: every copy is complete, its headings at its own depth, its links and nested sub-sections its own. `a-brief-s-sections-each-place-their-own-dispatches`: each section of a brief places its own dispatches. `a-brief-s-links-to-its-own-children-point-at-its-copy`: a Contract brief's preamble links point at each copy's own children. Held in `make corpus`.

## T7 Refusals and Preset Rules

`a-lifted-heading-equal-to-an-authored-heading-is-refused`, `two-briefed-dispatches-of-one-text-and-two-selections-are-refused` and `a-brief-s-composed-section-equal-to-its-child-is-refused` fail with `E_HEADING_COLLISION`; `a-brief-naming-another-document-is-refused` and `a-brief-naming-a-malformed-fragment-is-refused` with `E_INVALID_CONVERSION_METADATA`; `a-brief-naming-a-missing-heading-is-refused` with `E_TARGET_NOT_FOUND`; `a-brief-dispatching-its-own-target-is-a-cycle`, `a-cycle-of-briefs-is-refused`, `a-cycle-of-briefs-starting-deep-is-refused-as-a-cycle`, `a-cycle-of-briefs-in-a-deep-set-is-refused-as-a-cycle` and `a-brief-composing-the-section-dispatching-it-is-a-cycle` with `E_DISPATCH_CYCLE`, naming the chain and the closing dispatch. Unit tests: `src/tests/test_brief.py` and the brief tests in `src/tests/test_metadata.py`. Held.

## T8 Documented Rule

A reading of `docs/dispatch.md` (Briefs, The guide, Generated headings), `docs/sources.md` (the `brief` key), `docs/composition.md` (Composed content), `invocation.md`, the guide `pf` prints and the design's **Dispatch briefs**, **`brief` names a section of its own document**, **The source of composed content** and **Generated heading collisions**: each states the brief, its placement around the dispatch line, its compilation as a composition and its copies; the guide states that the text above a `⇉` line in the sub-section a link points at, and the sections beneath it, are the bundle's brief, done before the bundle is handed on. Held.

## T9 Eval Unit Tests

`make eval-harness` with the worktree's `pf` first on `PATH`: 855 passed. The `dispatch-brief` workflow is written in `compiled` and `briefed` forms around a `## Contract` brief whose preamble links its `Given`, `Leaves` and `Answers` sub-sections, the copied value living in `Given` alone; `test_the_dispatch_brief_forms_differ_only_in_the_brief`, `test_a_lifted_brief_links_its_own_children` and the `premature_dispatch` tests in `test_score.py` hold. Held.

## T10 Live Run

Both runs were made at `4cbd9db52` on the `opencode` harness and `openrouter/deepseek/deepseek-v4.1-flash-1017`, under the user's USD 5 cap, by the coordinating session on the user's direct approval.

- **Shakedown** `dispatch-brief-shakedown`: 4 sessions, 1 passed, USD 0.024484 over 800 977 tokens; the largest session's 260 255 tokens set the run's session cap at 530 000 and its token budget at 10 600 000, and 20 sessions at the doubled mean come to about USD 0.25. Its three `read_source` failures are each a `miss`.
- **Run** `dispatch-brief`: 20 of 20 sessions started, USD 0.116679 over 3 583 711 tokens. `briefed` passed 3 of 10 (30%), failing on `overcompiled` 4 and `read_source` 3; `compiled` passed 2 of 10 (20%), failing on `overcompiled` 5 and `read_source` 3. No session took `premature_dispatch`: every session wrote the `Given` value before starting its sub-agent.
- **Triage**: each of the 15 failures is a `miss` in `results/dispatch-brief/dispositions.json`, read into the committed report. The `overcompiled` sessions ran `pf` on a bundle file, a published dispatch link, a source section, a directory, an unknown word or no entry; none ran `pf` on the Contract preamble's links, and the scenario states no compile run. The `read_source` sessions opened the workflow's sources beside the bundles.
- **Committed**: `evals/diagram-following/dispatch-brief.json` and `dispatch-brief.md`, the README's Dispatch-brief run section and the runbook's run and shakedown rows.

The briefed form does not measurably outperform the unbriefed one: 30% against 20% over ten sessions each is no reliable difference, neither form dispatched before acting on the Contract, and the failures are unrelated to the brief. Held.

## T11 Full Check

`make check` with `PROSIFORM_BUILD` naming the worktree's `pf` exits 0 at `6d4cde584`: lint, format, typecheck, `make test` (2257 passed), harness (1107 passed), corpus (668 fixtures, 668 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T12 Copy-Local Links

`fixtures/composition/a-composed-section-s-link-to-its-own-subsection-points-at-its-copy`: a section composed twice links its own subsections, and each contribution's links point at its own copies, with no further copy bundled. `fixtures/composition/a-composed-subsection-an-inclusion-also-carries-keeps-its-link`: where an ordinary link also includes the subsection, the included group carries it and its link points at its own copy. Held in `make corpus`.
