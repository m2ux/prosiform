# Guide Fix

The guide told an agent to resolve every link from the document carrying it, and a bundle's deferred links are already named from the working directory. Escalation [#728](https://github.com/m2ux/prosiform/issues/728); pull request [#729](https://github.com/m2ux/prosiform/pull/729) into `i15/e01/main`.

## Defect

Bare `pf` printed, under "Compiling a link": "Resolve the destination from the linking document, then express it from the command's working directory." A compiled bundle sits in `<name>.bundles/` and publishes each deferred link already expressed from the working directory, as the design's "A deferred link's destination" clause and the fixture `deferral/a-deferred-destination-named-from-the-working-directory` state. In the agent-pick workflow, `states/classify.md` holds `[¬↳ Route](../reference/work-kind.md#route "?")` and `workflow.bundles/workflow.bundle.md` publishes `[↳ Route](reference/work-kind.md#route "?")`; resolved from the bundle's folder, that reaches `workflow.bundles/reference/work-kind.md`, which does not exist. Shakedown `agent-pick-shakedown-2` (2026-11-12) session `unknown-kind-held` did exactly that, then globbed and opened the source, and failed as `read_source`. Disposition `defect`, in the guide: the published path is working-directory relative by design.

## Fix

- The guide's "Compiling a link" block states that a link in a bundle runs as written, from the directory `pf` compiled that bundle in, and that a link in a source document resolves from that document and is expressed from the working directory. The rest of the guide is unchanged.
- `invocation.md` restates the same two cases. The glossary's "guide" row names the compile step only and stays as it is.
- The design's Guide clause on `engineering` carries the build's "Compiling a link" text (`ab6b9833a`). No document cites the Guide clause at its pin, so no pin moves.
- The bare-command test, the entry-presets guide test and the `cli/informational-guide-response` fixture hold the new wording.

## Tests

Run against `i15/e01/fix-guide-link-resolution` at `f5623b01c`, on `i15/e01/main` at `3ee6480f3`. No live model session ran.

### T1 Reproduction

- **Procedure.** Copy `evals/diagram-following/workflows/agent-pick/compiled` to a scratch folder and run `pf workflow.md` there.
- **Observation.** `workflow.bundles/workflow.bundle.md` publishes `[↳ Route](reference/work-kind.md#route "?")`; `workflow.bundles/reference/` does not exist, and `reference/work-kind.md` exists beside `workflow.md`.

### T2 Guide Text

- **Procedure.** `uv run --project src --frozen pytest -q src/tests/test_cli.py src/tests/test_entry_presets.py`
- **Observation.** Passed: the bare command prints the guide, which states both link cases and the existing quoting rules.

### T3 Eval Harness

- **Procedure.** `make eval-harness`
- **Observation.** 762 passed.

### T4 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0. Lint clean; `make test` 2039 passed; `make harness` 1022 passed, the guide fixture among them; corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass.

## Design guide text

The design's Guide clause states that bare `pf` prints exactly the text it reproduces. Outside "Compiling a link", that text differed from the `GUIDE` constant in `src/prosiform/cli.py` at `i15/e01/main` `7a7256a4e`. The design now reproduces the build byte for byte:

- **`⫽` entry.** "⇉ items in the sub-section headed ⫽ <that section's title> dispatch set." reads "⇉ lines in the sub-section headed ⫽ Dispatch Set.", with "Give each bundle …" opening the next line.
- **`?` entry.** "in a link's title, a preset you pick: pass the title as --presets as usual and pf lists the alternatives and when to pick each; rerun with ? replaced by the one that fits your task" reads "among a link's title tags leaves the pick to you: pass the title as --presets as usual, read the alternatives pf lists, and rerun with ? replaced by the one that fits your task".

Both build texts agree with the design's other rules: **Parallel dispatch sub-sections** heads the sub-section `⫽ Dispatch Set` and lists bare `⇉` lines, and **The agent's pick** places `?` among a link's title tags. No other clause changes. No document on `i15/e01/main` or `main` links the Guide clause by anchor; the whole-document and section pins there stand at `c04f5d8e6`, which predates both this change and `ab6b9833a`.
