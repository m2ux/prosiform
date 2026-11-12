# Validation

The checks the task pull request's Test Plan records, run against task branch `i15/e01/w04-the-documentation-states-the` at `5a8b6c21b`, from the unit checkout with the locked development environment (`uv sync --frozen`).

## T1 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0. Lint, format, type and lock checks clean; `make test` 2039 passed; `make harness` 1022 passed; corpus 583 fixtures, 583 pass, 0 fail; `link check: every reference in 412 document(s) resolved`, the new `#the-pick-token` anchors and the design's `#presets` and `#link-classification-and-resource-handling` anchors at `c04f5d8e6` among them; `vocabulary check: 51 contract term(s) marked … every one defined in docs/glossary.md, and every definition carried by the contract`, the new **pick token** row included; `invocation check: 29 statement(s)` hold; smoke, layout, tables, conformance and independence pass.

## T2 Page Read

- **Procedure.** A read of `docs/references.md`, `invocation.md` and `docs/glossary.md` at the tested revision.
- **Observation.** Each fact has one home:
  - **The `?` tag, where it is accepted and refused.** `docs/references.md` § The pick token: `?` alone or beside fixed tags; accepted on `¬` and `¬↳`, refused on an ordinary link, a composition directive, a dispatch and a parallel dispatch; a deferral to a document declaring alternatives names exactly one or carries `?`, and a `?` deferral to a document declaring none is refused; each refusal `E_UNSUPPORTED_CONSTRUCT`, exit `1`. It links the design's Presets and Link classification sections at `c04f5d8e6`. Selection by reference points to it.
  - **How an agent resolves it.** `invocation.md` § Guide states the guide's `?` entry; § Examples shows the kind router fixture's published link, the listing its command draws (exit `2`) and the rerun naming `epic`; § Conversion metadata links References for the `?` route.
  - **The term.** `docs/glossary.md` defines **pick token** and links References; the **guide** row names the pick token, and the **pick** row states the token names none.
  - `docs/selection.md` (Exactly one alternative) names `?` among the inputs the listing failure answers.

## T3 Contradiction Grep

- **Procedure.** `grep -rn -i "three symbols\|three marks\|skill's directory\|skill's bootstrap\|absent pick and a name\|title tags as written\|compiled as written" --include=*.md .`, excluding `fixtures/`.
- **Observation.** No statement the `?` rules contradict. The remaining hits name a skill's directory as a boundary example (`docs/sources.md`) or as an eval's working directory (`evals/diagram-following/README.md`), neither a statement about title tags. The glossary's stale guide row (`<destination>` from the skill's directory) is corrected to the guide's compile step.

## T4 Checks Workflow

- **Procedure.** The repository's Checks workflow, which runs `make check`, on pull request [#724](https://github.com/m2ux/prosiform/pull/724) at head `5a8b6c21b`.
- **Observation.** The `Checks` run completed with conclusion success: [run 43199498667](https://github.com/m2ux/prosiform/actions/runs/43199498667/job/131118873435).
