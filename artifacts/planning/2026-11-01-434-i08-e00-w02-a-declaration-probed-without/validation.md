# Validation

Evidence for each check the [work item](w02.md) names, run in the unit's worktree at `ec8fcdb7` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 head read tests

`src/tests/test_access.py` passes under `make test`.

- `test_a_head_read_stops_at_the_line_that_answers`: a declaring file followed by 1,000 body lines reads to its closer and no further; a file opening on `# Silent` reads its first line alone.
- `test_a_head_read_stops_at_its_budget`: an opener never closed within a 20-byte budget reads 21 bytes, so a crossing head is told from one that fills the budget.
- `test_a_head_read_follows_no_link`: a symbolic link below the root is refused with `Symlinked`, as `read_source` refuses it.

## T2 delimiter tests

`src/tests/test_source_metadata.py::test_a_head_closes_at_the_first_line_or_the_closer` passes: a first line opening no block, an indented opener, a `---` or `...` closer with LF or CRLF, and an undecodable line end the head; an opener, a BOM-led opener, a payload line and a closer carrying a trailing space do not.

## T3 probe tests

`src/tests/test_cli.py` passes under `make test`.

- `test_a_probe_answers_a_silent_target_whatever_its_size`: a 600-byte document with no frontmatter, and one whose frontmatter carries no `prosiform`, answer undeclared under `-B 64`.
- `test_a_probe_answers_a_declaring_target`: a BOM-led CRLF block closed by `...` answers declared.
- `test_a_probe_crossing_the_byte_budget_before_its_closer_fails`: a block longer than `-B 64` fails with `E_RESOURCE_LIMIT`.
- `test_a_probe_refuses_an_invalid_declaration`: an unknown `prosiform` key fails with `E_INVALID_CONVERSION_METADATA`, an unclosed opener with `E_UNTERMINATED_FRONTMATTER`.
- `test_a_probe_refuses_a_link`: a symbolic link fails with `E_SOURCE_SYMLINK`.

## T4 inclusion fixtures

Under `make corpus`:

- `fixtures/inclusion/an-oversized-declaring-target-fails: pass` — `huge.md` declaring `prosiform` and larger than `-B 64` fails with `E_RESOURCE_LIMIT`, chain `guide.md`, `huge.md`.
- `fixtures/inclusion/a-probe-follows-no-link: pass` — `linked.md`, a symbolic link to a declaring document, fails with `E_SOURCE_SYMLINK` at `guide.md:6`.
- `fixtures/inclusion/an-oversized-silent-target-is-text: awaited, awaiting I08:E00:W03` — the probe answers `huge.md` undeclared (T3); classification reads that answer when W03 lands, and lifts the marker.

## T5 full check

`make check` exits 0: corpus `378 fixture(s), 376 pass, 0 fail, 2 awaited, 0 unexpected pass`; conformance `0 declaration(s) naming no clause`.
