# Source Title-Tag Validation

## Revision and Scope

- Head: `6740227d364a406b68a3bf5c93c7a04dd17a9676`.
- Base: `b0ec538dacc97ca546ad5d5d83748764f511e258` (`i10/e07/main`).
- Component: `src/prosiform/source.py`; observing source tests and two resource/diagram corpus fixtures accompany it.
- `Use.tags` is a `frozenset[str]` from the shared decoded-list reader. `Use.title` remains the containing section's heading context until the selection consumers adopt explicit tags.

## Source Reader Checks

At the committed head:

```sh
uv run --project src --frozen pytest --config-file src/pyproject.toml src/tests/test_source.py src/tests/test_tags.py
```

Result: **302 passed**. [Source reader output](source-reader-check.txt) records the run.

The instrument observes inline links and full/collapsed/shortcut reference links, all supported title delimiters, decoded entities and escapes, preamble/section/heading/table/container contexts, repeated destinations with distinct title lists, absent and empty lists, operator-labelled links and first-definition resolution outside a selected section. Images, external links and Mermaid click/class/menu text expose empty tag sets independently of the containing heading and label.

Local non-image links carry their parsed title list before closure knows the destination's type. Closure retains target classification, so a non-Markdown target cannot select a declared preset. The reader does not duplicate profile extension checks or URI normalization.

## Resource and Diagram Corpus

The corpus includes two new observing fixtures:

- `resource/resource-titles-supply-no-preset-selection`: image, external and stylesheet titles preserve their authored text; an image naming a declaring Markdown document contributes no content.
- `reference/diagram-tooltips-supply-no-preset-selection`: a click tooltip and node labels naming preset tokens leave the followed document under default, preserve tooltip text and produce its unused named-preset warning.

The committed-head corpus run passes **518 fixtures**, including both additions, with zero failures or awaited cases. [Full output](make-check.txt) records each fixture result under the revision below.

## Full Deterministic Check

At the committed head:

```sh
PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w02-source-links-carry-title/src --frozen pf' make check
```

Result: **passed**, exit status 0. [Full output](make-check.txt) records:

- 1,775 source tests, including the new occurrence cases.
- 1,404 deterministic check/harness tests.
- 518 corpus fixtures.
- Lock, lint, formatting, strict typing, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence checks all pass.

The standing runtime contract pin reports 361 clauses, zero declarations naming no clause and zero diagnostic-code mismatches. Its 64 uncovered clauses and other reported gaps are existing conformance observations. Candidate design-pin adoption remains with the CLI/guide/fixture unit. No paid agent session is started.

## Diff Review

The source reader obtains titles from parser attributes and calls the one normalized-list reader. The new field has no effect on target classification, containing-heading context, byte-preserving publication or current preset matching. Its default is the absent-title selection. Image and diagram constructors carry that empty value, and external link occurrences explicitly carry it. The field is independent of visible labels and the order in which repeated destinations are encountered.

The new source tests directly observe occurrence data, and the resource/diagram corpus cases execute publication through the compiler. The full diff and immediate caller boundaries were reviewed; no defect or outside-scope debt was found. The [criterion-boundary clarification](changes.md) records the source-tag exclusion invariant separately from runtime heading/label independence. This unit establishes parsed title data and exclusion boundaries; source-to-reference retention and runtime preset matching remain their declared delivery work.

## Delivery Readback

Task PR [#667](https://github.com/m2ux/prosiform/pull/667) merges at `227069a8fed00554deb7f044da37f396f35a3208` after local and hosted checks pass. The exact merged revision passes the observing instrument `pytest src/tests/test_source.py src/tests/test_tags.py`, as [merged-check.txt](merged-check.txt) records. Current issue readback links every unit row to that merged PR and ticks its covered criteria and Done. The updated main integration remains a draft until the complete epic passes review.

The coordinator continues with W03 under the epic-wide authorization. No further unit confirmation is required.
