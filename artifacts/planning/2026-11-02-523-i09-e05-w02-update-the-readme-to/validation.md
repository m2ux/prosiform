# Validation — The Front Pages Read Against the Build

> Validation record · I09:E05 W02–W06 · Created 2026-11-02

Each page was read whole against the build at `main` [74b00cd9](https://github.com/m2ux/prosiform/tree/74b00cd9) (`pf 0.16.0 (skill-markdown-v4)`) and the design the README pins, [4958ad38](https://github.com/m2ux/prosiform/blob/4958ad38bc2bb6a0786f93aa6de30a7b6a2e27c9/artifacts/planning/2026-10-17-prosiform-v1/design.md). Every claim the page carried was held to the source named beside it; each correction is listed with what showed it. Claims not listed held.

## Readme Read

AC3. `README.md` against `pf -h`, the guide `pf` prints, `pf -C`, and the corpus fixtures the page cites.

- **Corrected: one bundle.** The opening said a run returns its content "as one validated bundle". `pf -h` says "into validated bundles", and `fixtures/dispatch/a-dispatched-target-is-a-bundle-of-its-own` publishes two. The opening now names the bundle each dispatched target takes.
- **Added: declaring a source.** The page named the `prosiform` declaration but not what it holds. A *Declare a Source* section states the frontmatter, `default` and title-selected presets, `group` and `subst`, and links [Sources](https://github.com/m2ux/prosiform/blob/main/docs/sources.md#frontmatter), which owns the rule.
- **Added: deferral.** The page named `⇉`, `⫽` and arrows but not `¬`. A *Defer a Link* section runs `fixtures/deferral/a-marked-reference-is-not-compiled`, whose expected bundle carries the link with its mark removed.
- **Added: the option surface.** Usage now points at the invocation guide for every option, budget and exit status `pf -h` reports, `-C` among them, rather than restating them.
- **Held.** The guide summary matches `pf`'s output; the run-folder, `-o` made-if-absent, `+` join and swap-in claims match `pf -h` and the `fixtures/cli` publication fixtures; the dispatch sub-section, `# Prosiform`, `## Dispatch`, `## Parallel dispatch` and `## Run pf first` claims match the expected bundles of the dispatch and parallel-dispatch fixtures; Python 3.13+ matches `requires-python = ">=3.13"`.

## Invocation Read

AC4. `invocation.md` against `make invocation`, `pf -h` and the pinned design's *CLI contract*, *Presets* and *Conversion metadata*.

- **Corrected: `subst` reach.** The page said "the section linking that document selects which of its presets apply". `cli.py` `governing` builds one table per document from every reference reaching it (review finding F2). The page now says a pair redirects under the presets every reference reaching the document selects.
- **Added: preset agreement.** The union rule and its refusals (`agreed`, `disagreeing`, both `E_INVALID_USAGE`, exit 2) were absent. One sentence states them and links Sources, which owns the rule.
- **Added: invalid usage.** The design refuses a command line the grammar does not admit, an undeclared option and an invalid value among them (`fixtures/cli/an-option-the-contract-does-not-declare`, `diagnostics-format-unknown`); the page now says so beneath the option table.
- **Added: standard output and `-o -`.** The design's "Standard output carries no bundle" and the refusals of `-o -` and of a run folder holding a captured source (`fixtures/cli/standard-output-named-as-the-output-folder`, `run-folder-holding-a-dependency-source`, both exit 2) are now in Output.
- **Added: deferred directive.** `[¬→]` is named beside the arrow directive, linking Composition.
- **Added: the guide's folder.** The guide `pf` prints says "The run makes it if it is not there"; the Guide paragraph now carries it (W30's departure, F1).
- **Held.** Every option, budget and exit row reproduces `pf -h` (`make invocation`: 28 statements held). The five worked commands run over a copy of `fixtures/cli/several-entries-joined-into-one-name/source`, each exit 0, writing `notes_rules.bundles/`, `guide__run.bundles/`, `build/notes_rules.bundles/` and `notes_rules+guide__run.bundles/`, `-c` writing nothing.

## Checks Page Read

AC5. `checks.md` against `make tables` and the `Makefile`.

- **Corrected: three outside, two listed.** The page said three commands sit outside `make check` and its table listed two. `make eval-diagrams` is now a row, its variables left to the eval README, which owns them.
- **Corrected: `make invocation`.** The row named arguments and exit statuses; `checks/invocation.py` also compares every budget, the profile `-v` reports and the required statements. The row now names all three.
- **Corrected: tool environments.** `make examples` and `make eval-diagrams` run through `$(UV_RUN)` and `make render` under `python3`; the lists now carry them.
- **Added: harness cases.** `checks/tests/test_authoring.py` (worked commands, hyphens) and the check-parser and slug cases had no bullet under *The Harness*; two bullets state them.
- **Clarified: layout.** "the four trees" now names `fixtures/`, `src/`, `docs/` and `evals/`, `checks/layout.py`'s `REQUIRED_TREES`.
- **Held.** Every `Makefile` target is named by a Command row (`make tables` passes in both directions); `make check`'s order and members match the `check:` rule.

## Checks Readme Read

AC6. `checks/README.md` against `make tables` and every file under `checks/`.

- **Corrected: layout.** The row named three trees; `layout.py` requires four, `evals/` included.
- **Corrected: a step check.** The suite paragraph named "the step check", which no file under `checks/` holds; the clause is removed.
- **Corrected: vocabulary ref.** The page said the design is read "as `origin/engineering`"; `vocabulary.py` reads the revision the README's design link pins (`4958ad38`), as `make vocabulary` reports. The sentence now says so.
- **Corrected: smoke.** `smoke.py` makes a missing `-o` folder, checks `-c` publishes nothing and checks the installed build ships the glossary; the row now states each. The `publishes` docstring in `smoke.py` still said a missing folder refuses the write and is corrected with it.
- **Corrected: invocation row.** A budget the command reports and no table names is now among its failures.
- **Added: authoring cases.** `tests/test_authoring.py` is now described.
- **Held.** Every script (`click.mjs`, `conformance.py`, `corpus.py`, `documents.py`, `independence.py`, `invocation.py`, `layout.py`, `links.py`, `manifests.py`, `render.py`, `runner.py`, `smoke.py`, `tables.py`, `vocabulary.py`) and `tests/` is described.

## Docs Index Read

AC7. `docs/README.md` against `make links` and every page under `docs/`.

- **Corrected: a dropped link.** "states each target the  declares" had lost its `Makefile` link; it is restored.
- **Corrected: two summaries.** Bundles also covers the bundle set and the output folder; Diagram Renderer covers two scripts, the architecture examples among them.
- **Held.** Every page under `docs/` (14, `images/` aside) has a row; the architecture rows follow `architecture.md`'s section order.

## Checks Run

`make check` in the worktree at af1248fb with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`: exit 0. 1663 check tests, 1161 build tests, 498 of 498 fixtures, smoke, layout (4 trees), tables, links (143 documents), vocabulary (49 terms), invocation (28 statements), conformance and independence all pass.
