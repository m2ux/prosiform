# Validation

Evidence for each check the [work item](w03.md) names, run in the unit's worktree at `039ce9a7` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 classification tests

`src/tests/test_closure.py` passes under `make test` (1,388 tests pass).

- `test_a_link_naming_a_declaring_document_is_a_dependency`: a target the record answers declared is a dependency.
- `test_a_link_naming_a_silent_document_is_text`: a target answered silent is no dependency, from `bundled` and `resolvable` alike.
- `test_a_withheld_link_naming_a_silent_document_withholds_nothing`: a deferral to a silent target is no withheld target.
- `test_a_target_is_probed_once_however_many_links_name_it`: three links, two spellings and a fragment, cost one probe.
- `test_a_citation_naming_no_markdown_document_is_never_probed`: a resource and a remote link are never probed.
- `test_the_probe_is_handed_the_occurrence_that_asked`: the probe receives the link's origin and its chain.

## T2 declaring target

`fixtures/inclusion/a-declaring-target-is-compiled: pass` under `make corpus` — the bundle carries `# Rules` after the guide and the link is rewritten to `#rules` (AC1).

## T3 silent target

`fixtures/inclusion/a-silent-target-is-text: pass` — `rules.md` with no frontmatter leaves the link as authored, the bundle carries the guide alone, and `-F 1` passes (AC3). `fixtures/inclusion/no-block-does-not-declare: pass` with its marker lifted.

## T4 oversized silent target

`fixtures/inclusion/an-oversized-silent-target-is-text: pass` with its marker lifted — `huge.md` larger than `-B 64` declaring nothing is text and the run exits `0`; `fixtures/inclusion/an-oversized-declaring-target-fails: pass` — the same target declaring fails with `E_RESOURCE_LIMIT` (AC6).

## T5 full check

`make check` exits 0 before opening, and the epic base held no newer commit before merging; CI on `039ce9a7` passes. Corpus `380 fixture(s), 380 pass, 0 fail, 0 awaited, 0 unexpected pass`; harness and conformance pass.
