# Test Results

Revision tested: `33e8f906b` on `i15/e00/w04-the-documentation-states-alternatives`, based on `i15/e00/main` at `ebe660cd7`, which carries W00 to W03. Every check ran from the unit checkout with `PROSIFORM_BUILD` naming that checkout's build: `uv run --project <unit-checkout>/src --frozen pf`.

## T1 Pages and Pins

`make links`, inside `make check`: `link check: every reference in 412 document(s) resolved`, the new design links at `c04f5d8e6` among them.

- `docs/sources.md`: the frontmatter table carries `choice`, and its paragraph states the choice line and the three `E_INVALID_CONVERSION_METADATA` refusals, linking Conversion metadata.
- `docs/selection.md`: Presets in force states alternatives, the exactly-one rule with `E_ALTERNATIVE_UNRESOLVED` and exit 2, and the unpicked-alternative exception to `W_PRESET_UNUSED`, linking Presets; The substitution mapping states routing pairs and their one warning beside an ordinary preset's two, linking Link classification.
- `invocation.md`: Conversion metadata states `choice`, the exactly-one failure, its exit status and remedy.
- `docs/glossary.md`: the alternative, choice line, pick and routing pair rows link the pages stating each rule, and the intro links the design.
- `docs/validation.md`: `E_ALTERNATIVE_UNRESOLVED` is listed with exit `2`, and the `choice` refusals under `E_INVALID_CONVERSION_METADATA`.
- No design link names `2f8d860e8`, and a grep for "its alternative", "two alternatives" and `pair.alternative` in the subst sense returns nothing.

## T2 Rename and Full Check

`make check`: exit 0.

- `make test` 2012 passed, `make harness` 1004 passed; lint, format, typecheck, lock, smoke, layout, tables, vocabulary, invocation and independence each passed.
- `corpus check: 565 fixture(s), 565 pass, 0 fail, 0 awaited, 0 unexpected pass`, the renamed `subst` refusal messages included.
- Conformance: `0 declaration(s) naming no clause`; `Conversion metadata — choice holds one line: 3 fixture(s)` and `Presets — Alternatives: 2 fixture(s)`.
- No `Subst.alternative` remains: `Subst.substitute` holds the side a pair redirects to.
