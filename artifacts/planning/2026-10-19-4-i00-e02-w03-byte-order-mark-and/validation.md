# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, recording the output, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w03-byte-order-mark-and` |
| Tested revision | `913552159943eef1574a2e594ef1896322194405` |
| Base revision | `7f8fe64` on `i00/e02/main`, the build the before-and-after corpus runs compare against |
| Contract revision | `8e42cc0` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Build under test | `prototype/.venv/bin/prosiform`, named to the corpus runner as `PROSIFORM_BUILD` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and `uv run --frozen` builds the project into the environment it runs in, so every `make` run below was performed outside the session's sandbox, which has no network and no write access to the `uv` cache. The corpus runs, which invoke an already-installed command, were performed inside it.

## T1 The set, in one pass

**Observes AC2, AC8.** The repository's checks run together, over a tree that strips transport metadata and requires its sources to be valid UTF-8.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The per-item `ok` lines each check prints are omitted; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.83ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
22 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 21 source files
cd prototype && uv run --frozen pytest
170 passed in 0.11s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
95 passed in 0.36s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs one hundred and seventy tests where the base ran ninety-eight. The corpus suite runs ninety-five where the base ran eighty-six; the nine are the schema validation of the nine fixtures this task adds. The table check is unchanged at eleven commands and seven declarations: this task adds no `Makefile` target and no dependency, the scan being standard library and the parser already declared and locked. The vocabulary check is unchanged at thirty-four terms: *frontmatter* is already marked by the design and already defined by the glossary, and this task marks no new term.

## T2 The scan, in both of its directions

**Observes AC2, AC8.** Each case the frontmatter policy includes beside each case it excludes, and the decode that refuses to substitute.

```bash
cd prototype && uv run --frozen pytest tests/test_source.py -q
```

**Pass.** Exit 0. Fifty-six tests: one leading mark removed and a second left as content; a mark elsewhere in the document untouched; a block closed by three hyphens and one closed by three dots; a mark before the opener removed with the block; CRLF-terminated delimiters recognized and a CRLF body carried through unconverted; an empty block; the blank lines below a closer preserved; a block closing on the last line and one whose closer carries no terminator; the first closer closing the block; the body after a removal byte-identical to its source; eleven first lines that open no block, the indented delimiter, the trailing space, the tab, `+++`, `{` and `***` among them; a blank line before the delimiter; a YAML example inside a code block; a thematic break below the first line; an empty document; six unterminated openers; the coordinate mapping in both the stripped and the unstripped case; the line division ending a line at a line feed and at neither a form feed nor a line separator; a line compared without its terminator; valid UTF-8 and a mark decoded; and four byte strings that are not valid UTF-8 raising rather than decoding.

## T3 The command's statuses, diagnostics and coordinates

**Observes AC2, AC8.** The two failures this row introduces reported as the input failures they are, and every location reported against the file rather than against the text the parser read.

```bash
cd prototype && uv run --frozen pytest tests/test_cli.py -q
```

**Pass.** Exit 0. Seventy-six tests, the sixty W02 carried among them. The sixteen this task adds: a source that is not valid UTF-8 failing with status 1, no code and a `source` naming the document; the same source reaching no generic handler; an unterminated opener failing with `E_UNTERMINATED_FRONTMATTER` at `guide.md:1`; transport metadata reaching no parse, shown by a refusal raised against content below a stripped mark and block; a diagnostic below a stripped block naming `guide.md:6` and one below a mark alone naming `guide.md:3`; six first lines that open no block shifting no coordinate; a CRLF-delimited block stripped through the command; a CRLF source read without newline translation; a referring document stripped like any other; and a stripped source the profile accepts reaching the absent bundling stage.

## T4 The corpus against the build, before and after

**Observes AC2.** Every fixture in the corpus, run against the build under test and compared with its manifest, at the base revision and at the tested revision.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python corpus.py
```

**Pass, as a measurement.** The base run reports **3 of 10 fixtures pass**; the run at this head reports **4 of 19**.

The three at the base are `cli/group-rule-depth`, `cli/group-rule-repeated-slug` and `cli/group-rule-unknown-slug`, which fail before any source is read. They pass at this head too, and the fourth is the fixture this row adds for the failure it completes:

```text
frontmatter/unterminated-block: pass
```

The other eight fixtures this task adds declare the bundle the contract names, so each fails on the absent bundling stage exactly as the seven already in the corpus do:

```text
frontmatter/crlf-delimiters: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/delimiter-with-trailing-spaces: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/dot-terminated: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/indented-delimiter: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/leading-blank-line: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/optional-mark: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/toml-fence: fail
  expected.exit_status: expected 0, the run exited 4
frontmatter/yaml-example-in-a-code-block: fail
  expected.exit_status: expected 0, the run exited 4
```

The ten fixtures already in the corpus are unedited, and their verdicts at this head are the verdicts they had at the base.

Each of the eight reaching status 4 is itself an observation: the scan accepted all eight sources, the indented delimiter, the trailing space, the TOML fence, the leading blank line and the YAML example among them, and refused none of them as an unterminated block.

**AC8 has no fixture, and will not until W07 lands a code.** A manifest requires a catalogued code for every diagnostic it declares, and the design's catalogue holds no code for a source that is not valid UTF-8, so the corpus structurally cannot state the run AC8 names. The criterion's failing direction is held by T2 and T3.

## F1 The leading mark not removed

**Observes AC2.** The scan leaves a byte-order mark at the head of the content.

```python
body = text
```

```bash
cd prototype && uv run --frozen pytest -q
```

**Failed as expected.** Exit 1, three tests.

```text
FAILED tests/test_source.py::test_one_leading_mark_is_removed - AssertionErro...
FAILED tests/test_source.py::test_a_second_mark_is_content - AssertionError: ...
FAILED tests/test_source.py::test_a_mark_before_the_opener_is_removed_with_the_block
```

Reverted.

## F2 The three-dot closer dropped

**Observes AC2.** Only a line of three hyphens closes a block, so a block closed by three dots runs to the end of the document.

```python
CLOSERS = ("---",)
```

**Failed as expected.** Exit 1, two tests.

```text
FAILED tests/test_cli.py::test_a_stripped_source_the_profile_accepts_reaches_the_absent_stage
FAILED tests/test_source.py::test_a_block_closed_by_three_dots_is_removed - p...
```

Reverted.

## F3 The coordinate shift not applied

**Observes AC2.** A location is reported at the line of the stripped content rather than the line of the file.

```python
return at
```

**Failed as expected.** Exit 1, four tests.

```text
FAILED tests/test_cli.py::test_a_diagnostic_below_a_stripped_block_names_the_line_of_the_file
FAILED tests/test_cli.py::test_a_crlf_source_reaches_the_parse_unconverted - ...
FAILED tests/test_cli.py::test_a_referring_document_is_stripped_too - Asserti...
FAILED tests/test_source.py::test_the_recorded_line_maps_a_parsed_location_to_the_file
```

Reverted. The first of those test names is the one this record's T3 lists as `test_a_crlf_delimited_block_is_stripped_by_the_command`; the rename landed with the test added under F6.

## F4 The decode substituting replacement characters

**Observes AC8.** A source that is not valid UTF-8 decodes with `U+FFFD` in place of each undecodable byte, and the run continues.

```python
return data.decode(ENCODING, "replace")
```

**Failed as expected.** Exit 1, six tests.

```text
FAILED tests/test_cli.py::test_a_source_that_is_not_valid_utf8_is_an_input_failure
FAILED tests/test_cli.py::test_a_source_that_is_not_valid_utf8_reaches_no_generic_handler
FAILED tests/test_source.py::test_bytes_that_are_not_valid_utf8_fail_rather_than_decoding[# Guide\n\n\xe9\n]
FAILED tests/test_source.py::test_bytes_that_are_not_valid_utf8_fail_rather_than_decoding[\xff\xfe# Guide\n]
FAILED tests/test_source.py::test_bytes_that_are_not_valid_utf8_fail_rather_than_decoding[\xc3]
FAILED tests/test_source.py::test_bytes_that_are_not_valid_utf8_fail_rather_than_decoding[\xed\xa0\x80]
```

Reverted.

## F5 The line division taken from the standard library

**Observes AC2.** `str.splitlines` ends a line at every character Unicode calls a line break, which is more characters than end one in CommonMark.

```python
return text.splitlines(keepends=True)
```

**Failed as expected.** Exit 1, two tests, each naming a character that ends no line.

```text
FAILED tests/test_source.py::test_a_line_ends_at_a_line_feed_and_nowhere_else[a\x0cb\n-1]
FAILED tests/test_source.py::test_a_line_ends_at_a_line_feed_and_nowhere_else[a b\n-1]
```

Reverted.

## F6 The read translating newlines

**Observes AC2.** The source is opened in text mode with universal newlines, so a CRLF document reaches the scan as LF.

```python
text = path.read_text(encoding=ENCODING)
```

**Passed, which was the finding.** The suite as it stood reported nothing: every CRLF case then in it observed a diagnostic's line number, and a translation that rewrites a terminator leaves line numbers alone.

```text
169 passed in 0.11s
```

`test_a_crlf_source_is_read_without_newline_translation` was added to observe the content itself rather than a coordinate over it, and the same fault was then run again.

**Failed as expected.** Exit 1, one test.

```text
FAILED tests/test_cli.py::test_a_crlf_source_is_read_without_newline_translation
```

Reverted.

## T5 Continuous integration

**Observes AC2, AC8.** The same set, run by the `Checks` workflow on the pushed head rather than on a working copy.

```bash
gh run view 39239212555 --repo m2ux/prosiform --log
```

**Pass.** Conclusion `success`, head `913552159943eef1574a2e594ef1896322194405`, which is the revision tested above and the head the pull request merges from.

```text
Resolved 22 packages in 0.65ms
All checks passed!
22 files already formatted
Success: no issues found in 21 source files
170 passed in 0.36s
95 passed in 0.53s
layout check: 3 tree(s) present
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

## T6 The epic base after the merge

**Observes AC2, AC8.** The same set, run by the `Checks` workflow on `i00/e02/main` at merge commit `3af44a1`.

```bash
gh run view 39239750538 --repo m2ux/prosiform --log-failed
```

**Fail, on a condition this row does not carry.** One test of ninety-five, and it is the catalogue test:

```text
FAILED checks/tests/test_catalogue.py::test_a_catalogue_is_the_codes_the_design_declares[error-E_]
  Extra items in the right set:
  'E_ROOT_NOT_FOUND'
  'E_UNEXPECTED_INTERNAL_ERROR'
  'E_INVALID_USAGE'
  'E_UNSUPPORTED_CONSTRUCT'
  'E_PUBLICATION_FAILED'
  'E_UNSUPPORTED_ENTRY_SUFFIX'
  'E_RAW_HTML'
1 failed, 94 passed in 0.56s
```

The catalogue test holds `fixtures/manifest.schema.json` to the set of `E_`-prefixed codes the design carries on `origin/engineering`. W07 declared seven further codes there at `a073271`, between the run on this row's head at `10:41` and the run on the base at `10:45`, and the schema enumerating them is W07's own change. Every branch of the repository fails this test while those two land apart, and the condition clears when W07's pull request merges.

The nine fixtures this row adds validate against the schema in that same run, as the ninety-four passing tests include them.

**No code in the seven names a source that is not valid UTF-8.** The gap AC8's fixture waits on is still open after W07's catalogue, which is a finding for that row rather than a change made here.
