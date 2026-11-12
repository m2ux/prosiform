# Validation

The checks the task pull request's Test Plan records, run against task branch `i15/e01/w01-a-pick-tag-rides` at `589e4aacb` (code at `c84f8fa87`, fixtures at `589e4aacb`), from the unit checkout with the locked development environment (`uv run --frozen`).

## T1 Tag Reader Unit Tests

- **Procedure.** `cd src && uv run --frozen pytest tests/test_tags.py`
- **Observation.** 23 passed. `?` is read apart from the names beside it, alone, padded and beside other names; a list without the whole token, `checks?` and `why?` among them, leaves no pick; every earlier normalization case selects as before.

## T2 Command Unit Tests

- **Procedure.** `cd src && uv run --frozen pytest tests/test_cli.py -k "pick_token or compiled_link or stating_no_one_pick or one_pick_or_needing_none or no_alternative_in_force"`
- **Observation.** 20 passed. A `¬` and a `¬↳` link carrying `?`, alone and beside `checks`, publish the title as authored; an ordinary, `↳`, `⇉` and `⫽` link carrying `?` to a declaring document is refused with `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, naming the link; a link to a document declaring nothing keeps `?` as text; a deferral to a document with alternatives naming none, an ordinary preset alone, two, or one beside `?` is refused naming the target's alternatives; `?` to a document without alternatives is refused; a deferral naming one alternative, and one to a document without alternatives, publish.
- **Limitation.** An ordinary link carrying `?` now meets the pick-token refusal rather than `E_ALTERNATIVE_UNRESOLVED`, so the earlier `?` case of `test_a_document_with_no_alternative_in_force_is_refused` is removed; the entry's `--presets ?` path is unchanged.

## T3 Deferral Fixtures Publishing the Pick Token

- **Procedure.** `make corpus` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** `deferral/a-deferral-carries-the-pick-token` and `deferral/a-deferred-directive-carries-the-pick-token-beside-a-fixed-tag` pass: the bundle publishes `[Populate the body](work-kind.md "?")` and the deferred composition line `[↳ Populate](work-kind.md#populate "checks, ?")` as authored.

## T4 Fixtures Refusing the Pick Token on a Compiled Link

- **Procedure.** The T3 corpus run.
- **Observation.** `deferral/an-ordinary-link-carrying-the-pick-token-is-refused`, `deferral/a-directive-carrying-the-pick-token-is-refused`, `dispatch/a-dispatch-carrying-the-pick-token-is-refused` and `dispatch/a-parallel-dispatch-carrying-the-pick-token-is-refused` pass: each exits 1 with `E_UNSUPPORTED_CONSTRUCT` naming the link text and `guide.md:8`, and publishes nothing.

## T5 Deferral Fixtures Checking the Pick

- **Procedure.** The T3 corpus run.
- **Observation.** `deferral/a-deferral-naming-no-alternative-is-refused`, `deferral/a-deferral-naming-two-alternatives-is-refused`, `deferral/a-deferral-naming-an-alternative-beside-the-pick-token-is-refused` and `deferral/a-pick-token-deferral-to-a-document-without-alternatives-is-refused` pass, each exiting 1 with `E_UNSUPPORTED_CONSTRUCT` naming the target and its alternatives; `deferral/a-deferral-naming-one-alternative-publishes` passes, publishing `"task, checks"` as authored.

## T6 Repository Checks

- **Procedure.** `make check` with the T3 `PROSIFORM_BUILD`.
- **Observation.** Exit 0. Lint, format, type and lock checks clean; `make test` 2039 passed; `make harness` 1017 passed; corpus 578 fixtures, 578 pass, 0 fail; smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass, the conformance report naming 0 declarations that name no clause.

## T7 Checks Workflow

- **Procedure.** The repository's Checks workflow, which runs `make check`, on pull request [#721](https://github.com/m2ux/prosiform/pull/721) at head `589e4aacb`.
- **Observation.** The `Checks` run completed with conclusion success: [run 43196599299](https://github.com/m2ux/prosiform/actions/runs/43196599299/job/131109039176).
