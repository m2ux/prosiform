# Test Results

Results for W01 at `1c18ef595` on `release/v0.25.0`, run on 2026-11-13 with `PROSIFORM_BUILD` naming the release worktree's `src/.venv/bin/pf`, created with `uv sync --frozen`.

## T1 Previous Corpus

`checks/corpus.py` from a detached worktree of `contract/v0.24.0`, run with the release environment's Python against the release build: 551 fixtures, 538 pass, 13 fail, 0 awaited, 0 unexpected pass. A failing previous corpus is an incompatible change, which below 1.0 moves the minor, so the release is 0.25.0 ([What the numbers mean](https://github.com/m2ux/prosiform/blob/3480e4abead720f8b0dc41b91b88a6eb7bf118f1/docs/versioning.md#what-the-numbers-mean)). The failing fixtures hold the retired tooltip rule, the retired `--presets` option, and the entry grammar the link invocation replaces:

- `cli/a-markdown-link-is-no-entry-destination`
- `cli/an-empty-preset-list-selects-default`
- `cli/informational-guide-response`
- `cli/informational-long-usage-response`
- `cli/informational-usage-response`
- `cli/unknown-preset-names-select-default`
- `composition/activated-title-selection-under-unrelated-headings`
- `identity/path-needing-escaping`
- `inclusion/a-dependencys-preset-comes-from-itself`
- `inclusion/a-followed-deferral-reads-its-preset`
- `inclusion/a-subst-entry-is-a-colon-pair`
- `inclusion/an-entry-name-reads-its-documents-presets`
- `reference/diagram-tooltips-supply-no-preset-selection`

Recorded in the release pull request, [#761](https://github.com/m2ux/prosiform/pull/761). Held.

## T2 Full Check

`make check` passes: lock consistency, lint, format, types, `make test` (2137 passed), harness (1054 passed), corpus (615 fixtures, 615 pass), smoke (`pf 0.25.0 (prosiform-markdown)` from the installed wheel), layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T3 Version

`pf -v` built from `main` at `d5a57469f`, the merge of #761, reports `pf 0.25.0 (prosiform-markdown)`. Held.

## T4 Tags

Annotated `contract/v0.25.0` and `python/v0.25.0` each name `d5a57469f`, the merge of #761 on `main`, with the messages below. Held.

## Tag Messages

Prepared for the release merge on `main`, in the shape of the `contract/v0.24.0` and `python/v0.24.0` messages.

`contract/v0.25.0`:

```text
Contract v0.25.0

Pre-1.0 contract revision for diagram click titles, where the marks opening a Mermaid click's quoted tooltip state the link's operator and the rest selects presets, and for link entries, where pf takes a published link as written and a deferral takes --pick, under profile prosiform-markdown. The current corpus holds 615 passing fixtures. Against this build, the v0.24.0 corpus has 538 passes and 13 failures; the revision fails the previous corpus, which moves the minor under the pre-1.0 version convention.
```

`python/v0.25.0`:

```text
Python build v0.25.0

Implements contract/v0.25.0 under profile prosiform-markdown. Package metadata reports 0.25.0. Validation: 2137 tests, 1054 harness tests, 615 corpus fixtures, lock consistency, and installed-package smoke check pass.
```
