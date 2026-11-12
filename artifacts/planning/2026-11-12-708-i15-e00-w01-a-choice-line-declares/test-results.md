# Test Results

Revision tested: `1a5a18fe4` on `i15/e00/w01-a-choice-line-declares`, based on `i15/e00/main` at `5d517e49e`. Every check ran from the unit checkout with `PROSIFORM_BUILD` naming that checkout's build: `uv run --project <unit-checkout>/src --frozen pf`.

## T1 Metadata Unit Tests

`uv run --frozen pytest tests/test_metadata.py` from `src/`.

- Result: every test passed; the 19 cases selected by `-k "choice or alternative or pick"` are the new ones.
- A non-empty one-line `choice` is carried on its preset, and `Conversion.alternatives` lists the presets holding one in declaration order, an ordinary preset's `choice` being absent.
- An empty string, a string holding `\n`, `\r`, `\u0085` or ` `, a trailing line break, a two-line block scalar, an integer, a boolean, a null, a sequence and a mapping each fail with `E_INVALID_CONVERSION_METADATA` at the value, naming `prosiform.Epic.choice`.
- A `choice` in `default` and in `Default` fails at its key; a preset named `?` fails at its key, empty or holding a `choice`.
- A top-level `choice` names a named preset as the place the field belongs, never `default`.
- The existing metadata tests pass unchanged: ordinary presets decode as before.

## T2 Refusal Fixtures

`make corpus`, the three new `frontmatter/` fixtures.

- `frontmatter/a-multi-line-choice-fails`: pass. A block-scalar `choice` fails with `E_INVALID_CONVERSION_METADATA` at `guide.md:4:13`, exit 1, nothing published.
- `frontmatter/a-choice-in-default-fails`: pass. Fails at the `choice` key, `guide.md:4:5`.
- `frontmatter/a-preset-named-the-pick-token-fails`: pass. Fails at the `"?"` key, `guide.md:5:3`.

## T3 Inclusion Fixture

`make corpus`, `inclusion/a-link-picks-an-alternative-beside-an-ordinary-preset`: pass.

- The link title `epic, checks` picks the `epic` alternative of `work-kind.md` beside its ordinary `checks` preset.
- The bundle routes `work-kind.md`'s link to `epic-body.md` and places the document under Reviews; the `initiative` route stays out of force.
- The run raises `W_SUBST_USED` for the used pair and `W_PRESET_UNUSED` for `initiative`, the warnings the build reports before W02 and W03 change them; those rows update this fixture's expected diagnostics.

## T4 Full Check

`make check`: exit 0.

- `corpus check: 555 fixture(s), 555 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- `make test` 1983 passed, `make harness` 992 passed; lint, format, typecheck, lock, smoke, layout, tables, links, vocabulary, invocation, conformance and independence each passed.
- Conformance: `0 declaration(s) naming no clause`. The new fixtures name clauses of the design the repository pins (`2f8d860e8`), since the `choice` clauses reach `engineering` only with the epic; W04 repins the design.
