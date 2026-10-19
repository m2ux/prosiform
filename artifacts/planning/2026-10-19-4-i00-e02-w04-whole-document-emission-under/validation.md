# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, recording the output, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w04-whole-document-emission-under` |
| Tested revision | `f5ab36615042690c3b9c42cf420aaaf6fcb028e1` |
| Base revision | `7aac4ef` on `i00/e02/main`, the build the before-and-after corpus runs compare against |
| Contract revision | `a1bd6ec` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Build under test | `prototype/.venv/bin/prosiform`, named to the corpus runner as `PROSIFORM_BUILD` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and `uv run --frozen` builds the project into the environment it runs in, so every `make` run below was performed outside the session's sandbox, which has no network and no write access to the `uv` cache. The corpus runs and the per-suite `pytest` runs, which invoke an already-installed command, were performed inside it.

## T1 The set, in one pass

**Observes AC1.** The repository's checks run together, over a tree whose command publishes a bundle.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The per-item `ok` lines each check prints are omitted; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 1ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
24 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 23 source files
cd prototype && uv run --frozen pytest
245 passed in 0.14s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
124 passed in 0.36s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs two hundred and forty-five tests where the base ran one hundred and seventy-six. The corpus suite runs one hundred and twenty-four where the base ran one hundred and eighteen; the six are the schema validation of the six fixtures this task adds. The table check is unchanged at eleven commands and seven declarations: this task adds no `Makefile` target and no dependency, the emission being standard library over a parser already declared and locked. The vocabulary check is unchanged at thirty-four terms: *file group*, *entry line*, *preamble*, *group*, *region* and *destination* are each already marked by the design and already defined by the glossary, and this task marks no new term and changes no contract text.

## T2 The bundle's structure

**Observes AC1.** The file heading one path generates, the escaping that keeps it literal, the destination it carries, the region each block emits, and the two decisions a group makes about its own headings.

```bash
cd prototype && uv run --frozen pytest tests/test_bundle.py -q
```

**Pass.** Exit 0. Fifty-four tests: seven paths reduced to a file heading, the Markdown suffix classified case-insensitively and a suffix outside the profile kept; eleven escapings, one for each character that can open a construct the profile reads and two paths that need none; an escaped path reparsed to one text child carrying the original characters; seven slugs, the renderer's rule over case, punctuation, the hyphen and the underscore it keeps and the space it converts; the ordinal a repeated slug takes; the entry line for one reference, for three, and with its link text escaped; a container counted as one region and its contents as none; a group opening on its file heading; a title the path already names absorbed with its group's levels kept; a title the path does not name kept and shifted; a second H1, an H1 that is not the first heading, and a container-nested H1 each leaving the title unabsorbed; a document with no heading at all; a preamble after the file heading and before the first retained heading; a blank line above the first region not carried; a used and an unused reference definition each removed with no blank line left behind; seven regions carried as the bytes their sources wrote, the indented thematic break, the trailing-space delimiter, the TOML fence, the indented code block, the fenced example, the quote and the loose list among them; three blank lines between two regions emitted as one; a shift beyond the sixth level refused; the sixth level reached without overflow in an absorbed group; and a bundle ending in exactly one newline.

## T3 The command's statuses, its streams and its publication

**Observes AC1.** The bundle reaching standard output and nothing else, the file groups a run assembles, and the publication cases the corpus observes only through standard output.

```bash
cd prototype && uv run --frozen pytest tests/test_cli.py -q
```

**Pass.** Exit 0. Ninety-two tests, the seventy-six W03 carried among them. The sixteen this task adds: a successful run publishing the bundle to standard output and nothing to standard error; two sources sharing a basename in different directories headed by their own paths; groups ordered by root-relative path whatever order the references were given in; one document named twice bundled once; two paths differing only by Markdown extension failing with `E_AMBIGUOUS_FILE_GROUP` and publishing nothing; a heading beyond the sixth level failing with `E_HEADING_DEPTH_OVERFLOW` and publishing nothing; a fragment reference returning the unexpected-internal-error status and publishing nothing; an empty fragment bundling as the whole-document reference it is; a referring document contributing no group; a named output file carrying the bundle; that file published through exactly one rename and leaving nothing beside it; a failing run leaving an existing output file untouched; an output path the run cannot write failing with `E_PUBLICATION_FAILED`; a validation-only run bundling and publishing to neither stream nor file; and a validation-only run still reporting a bundle it cannot build.

The twelve tests W03 left asserting the unexpected-internal-error status as the end of a run now assert success, because a run that reads, strips and parses cleanly publishes.

## T4 The corpus against the build, before and after

**Observes AC1.** Every fixture in the corpus, run against the build under test and compared with its manifest, at the base revision and at the tested revision.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python corpus.py
```

**Pass, as a measurement.** The base run reports **11 of 26 fixtures pass**; the run at this head reports **30 of 32**.

Thirteen of the fifteen failing at the base declared a successful bundling and failed on the absent bundling stage. All thirteen pass at this head, and so do the six this task adds:

```text
frontmatter/crlf-delimiters: pass
frontmatter/delimiter-with-trailing-spaces: pass
frontmatter/dot-terminated: pass
frontmatter/indented-delimiter: pass
frontmatter/leading-blank-line: pass
frontmatter/optional-mark: pass
frontmatter/toml-fence: pass
frontmatter/yaml-example-in-a-code-block: pass
identity/whole-document: pass
profile/extension-lookalikes: pass
profile/html-in-a-code-example: pass
profile/task-markers-and-typography: pass
profile/task-markers-protected-from-definitions: pass
identity/path-needing-escaping: pass
identity/paths-differing-only-by-suffix: pass
identity/same-basename-in-two-directories: pass
identity/title-the-path-does-not-carry: pass
profile/invalid-byte-mid-document: pass
profile/utf16-byte-order-mark: pass
```

No fixture already in the corpus was edited. **Every one of the thirteen bundles authored ahead of this row states the contract**, and the emitter was written to them rather than them to it: the entry line, the file heading, the absorbed title, the bytes each region preserves and the single blank line between two regions are each a clause of `design.md`, and the two disagreements the work item names are settled in the fixtures' favour there.

**Two fixtures still fail, each on a stage a later epic carries.**

```text
extraction/nested-section-target: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_NESTED_SECTION_TARGET expected, error E_UNEXPECTED_INTERNAL_ERROR produced
normalization/root-escape: fail
  expected.exit_status: expected 1, the run exited 0
  expected.stdout: the bytes differ
    0 bytes expected, 158 produced
  expected.diagnostics: the run emits 0 diagnostics where 1 diagnostic is expected
    position 1: error E_SOURCE_OUTSIDE_ROOT expected, the run emits none
```

`extraction/nested-section-target` names a fragment, and section selection is `I00:E03:W02`. The run reports the status that says this build cannot carry the request out, which is the same verdict it reported at the base.

`normalization/root-escape` declares a reference leaving the allowed root, and that reference is a link inside the document rather than an entry. Dependency traversal is `I00:E04`, so no link is followed and nothing leaves the root; the run bundles the document it was given and succeeds. **Its verdict changed category rather than improving**: at the base it failed with status 4, and at this head it fails with status 0 and a published bundle. A run that publishes a document carrying an unfollowed link is what a build without closure does, and the fixture is the measure of the stage that fixes it.

## F1 The entry line not emitted

**Observes AC1.** The bundle opens on its first file heading, with no line naming what it was built for.

```python
return SEPARATOR.join([one.text for one in groups]) + TERMINATOR
```

**Failed as expected.** Exit 1, three tests.

```text
FAILED tests/test_bundle.py::test_a_bundle_ends_in_exactly_one_newline
FAILED tests/test_cli.py::test_a_successful_run_publishes_the_bundle_and_nothing_else
FAILED tests/test_cli.py::test_a_named_output_file_carries_the_bundle
```

The corpus run under the same fault reports **14 of 32**, so sixteen fixtures turn on the line alone. Reverted.

## F2 The path not escaped

**Observes AC1.** The file heading carries the path as the filesystem spells it, so punctuation in it is read as markup.

```python
return text
```

**Failed as expected.** Exit 1, ten tests, eight of them the escaping cases and two the heading and the entry line built from one.

```text
FAILED tests/test_bundle.py::test_an_escaped_path_opens_no_construct
FAILED tests/test_bundle.py::test_the_entry_line_escapes_the_text_of_the_heading_it_names
```

The corpus run under the same fault reports **29 of 32**: `identity/path-needing-escaping` is the fixture that observes it. Reverted.

## F3 A region's terminator carried into the bundle

**Observes AC1.** A region ends at the last byte of its last line rather than at the last byte of its content, so the separation between two regions is whatever the source left there.

```python
return "".join(carried)
```

**Failed as expected.** Exit 1, twenty-two tests, the region, separation and whole-bundle cases among them.

```text
FAILED tests/test_bundle.py::test_the_separation_between_two_regions_is_one_blank_line
FAILED tests/test_bundle.py::test_a_region_carries_the_bytes_its_source_wrote[- one\n\n- two]
FAILED tests/test_cli.py::test_a_successful_run_publishes_the_bundle_and_nothing_else
```

The corpus run under the same fault reports **14 of 32**. This is the fault the two disagreements the work item settles would have produced: the blank line a removed definition left behind and the blank line above a preamble both reappear. Reverted.

## F4 No title absorbed

**Observes AC1.** Every group shifts, so a document whose path already names its title emits that name twice at its head.

```python
if carried or not carried:
    return None
```

**Failed as expected.** Exit 1, eighteen tests.

```text
FAILED tests/test_bundle.py::test_a_title_the_path_already_names_is_absorbed
FAILED tests/test_bundle.py::test_an_absorbed_group_keeps_its_source_heading_levels
FAILED tests/test_bundle.py::test_an_absorbed_group_reaches_the_sixth_level_without_overflow
```

The corpus run under the same fault reports **16 of 32**. Reverted.

## F5 The depth guard off by one

**Observes AC1.** A shift is refused at the eighth level rather than the seventh, so a heading beyond H6 reaches the bundle.

```python
if depth > MAX_LEVEL + 1:
```

**Failed as expected.** Exit 1, three tests.

```text
FAILED tests/test_bundle.py::test_a_shift_beyond_the_sixth_level_is_an_overflow
FAILED tests/test_cli.py::test_a_heading_beyond_the_sixth_level_fails_and_publishes_nothing
FAILED tests/test_cli.py::test_a_validation_only_run_still_reports_a_bundle_it_cannot_build
```

Reverted.

## F6 The output file written in place

**Observes AC1.** The bundle is written to the destination directly rather than to a neighbouring file renamed onto it, so a reader can see a partial document.

```python
destination.write_text(text, encoding=ENCODING, newline="")
```

**Failed as expected.** Exit 1, one test.

```text
FAILED tests/test_cli.py::test_a_named_output_file_is_published_through_one_rename
```

Reverted. The surrounding cases pass under this fault, which is why the rename is observed by a test of its own: a file whose bytes are correct says nothing about how they arrived.

## T5 Continuous integration

**Observes AC1.** The same set, run by the `Checks` workflow on the pushed head rather than on a working copy.

```bash
gh run view 39245901878 --repo m2ux/prosiform --log
```

**Pass.** Conclusion `success`, head `f5ab36615042690c3b9c42cf420aaaf6fcb028e1`, which is the revision tested above and the head the pull request merges from.

```text
Resolved 22 packages in 1ms
All checks passed!
24 files already formatted
Success: no issues found in 23 source files
245 passed in 0.37s
124 passed in 0.52s
layout check: 3 tree(s) present
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

## T6 The epic base after the merge

**Observes AC1.** The same set, run by the `Checks` workflow on `i00/e02/main` at merge commit `60b67b3`.

```bash
gh run view 39246467576 --repo m2ux/prosiform --log
```

**Pass.** Conclusion `success`. The catalogue test, which failed on this base while W03 and W07 landed apart, passes here: the design on `origin/engineering` and the schema on the base carry the same twenty codes.

```text
All checks passed!
24 files already formatted
Success: no issues found in 23 source files
245 passed in 1.98s
124 passed in 0.54s
layout check: 3 tree(s) present
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 6 document(s) resolved
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

## The Criteria This Bundle Makes Observable

Not ticked here. Each is another row's criterion, and each now has a fixture that shows it end to end for the first time.

| Criterion | Now shown by | What the bundle made observable |
| --- | --- | --- |
| AC2 | `frontmatter/optional-mark`, `crlf-delimiters`, `dot-terminated` | A leading mark and a leading frontmatter block absent from bundled content, with the body below them carried byte for byte. Before a bundle existed the strip could only be observed through a diagnostic's line number. |
| AC3 | every fixture declaring `exit_status = 0` | A successful run writing the bundle to standard output and nothing else to that stream, compared byte for byte, with standard error empty. |
| AC5 | `profile/task-markers-and-typography`, `task-markers-protected-from-definitions` | Task-list markers surviving bundling as the three characters the source wrote, and punctuation inviting typographic substitution reaching the bundle unchanged. |
| AC7 | `profile/extension-lookalikes` beside `profile/unsupported-construct` | The passing direction: prose, a code span and an escape that resemble an unsupported construct bundling untouched, where only the refusing direction had a fixture. |
| AC9 | `profile/html-in-a-code-example` beside `profile/raw-html-in-selected-content` | The passing direction: an HTML example inside a fence and inside an indented block carried byte for byte, where only the refusing direction had a fixture. |
| AC8 | `profile/source-not-utf8`, `utf16-byte-order-mark`, `invalid-byte-mid-document` | Three encoding fixtures where the criterion's wording names fixtures in the plural, the failure reachable at a source's first byte and below its first section alike. |

AC6 is `I00:E02:W05`'s and has no fixture yet: no document taken unmodified from a workspace skill is in the corpus. AC4 and AC10 were observable before this row and remain so.

## What This Row Took from E03, and What It Left

| Clause | State | Owner |
| --- | --- | --- |
| The per-group shift decision and the title absorption that selects it | Delivered | `I00:E03:AC9`, whose fixtures and the multi-H1 and non-first-H1 cases remain |
| The level edit on a document-level ATX heading | Delivered | `I00:E03:AC3`, whose fixtures remain |
| The depth guard refusing a shift beyond the sixth level | Delivered | `I00:E03:AC6`, whose fixtures remain |
| Setext conversion, including the multiline source form | Not delivered | `I00:E03:AC4` |
| The shift inside a retained container | Not delivered | `I00:E03:AC3`, Containers |

A group that keeps its own title and carries a Setext heading or a container-nested heading emits that heading at its source level. No fixture asserts otherwise and no source in the corpus carries one. The multiline Setext form has no settled conversion — ATX carries no line break — and that is the question `AC4` exists to answer, so taking the conversion here would have answered it without a criterion.
