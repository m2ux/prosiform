# Validation

The checks this task carries, as they were run. Every run below was performed and its output is the output it produced; nothing is reported that was not observed. Each failing case was produced by editing the working tree so that it carried one fault and nothing else, running the named command, recording the output, and reverting the edit.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e02/w02-profile-configuration-and-source` |
| Tested revision | `b765a0e9c579bb45a70123a95dd7a7874ed8e97a` |
| Base revision | `410fdd4` on `i00/e02/main`, the build the before-and-after corpus runs compare against |
| Contract revision | `4010ed8` on `engineering`, which the catalogue and vocabulary checks read as `origin/engineering` |
| Run from | the repository root of the task worktree |
| Runner | GNU Make 4.4.1 |
| Toolchain | `uv 0.11.14`, CPython 3.13.7, `pytest 9.1.1`, `jsonschema 4.26.0`, `ruff 0.17.1`, `mypy 2.4.0`, `markdown-it-py 4.2.0` |
| Build under test | `prototype/.venv/bin/prosiform`, named to the corpus runner as `PROSIFORM_BUILD` |
| Date | 2026-10-19 |

The link check reaches addresses outside the repository and `uv run --frozen` builds the project into the environment it runs in, so every `make` run below was performed outside the session's sandbox, which has no network and no write access to the `uv` cache. The corpus runs, which invoke an already-installed command, were performed inside it.

## T1 The set, in one pass

**Observes AC5, AC7, AC9.** The repository's checks run together, over a tree the profile now configures.

```bash
make check
```

**Pass.** Exit 0. The runner ran `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `corpus`, `layout`, `tables`, `links` and `vocabulary` in that order. The per-item `ok` lines each check prints are omitted; the verdicts are not.

```text
cd prototype && uv lock --check
Resolved 22 packages in 0.92ms
uv run --project prototype --frozen ruff check --config prototype/pyproject.toml prototype/src prototype/tests checks
All checks passed!
uv run --project prototype --frozen ruff format --check --config prototype/pyproject.toml prototype/src prototype/tests checks
20 files already formatted
uv run --project prototype --frozen mypy --config-file prototype/pyproject.toml prototype/src prototype/tests checks
Success: no issues found in 19 source files
cd prototype && uv run --frozen pytest
98 passed in 0.08s
uv run --project prototype --frozen pytest --config-file prototype/pyproject.toml --rootdir . checks/tests
86 passed in 0.36s
python3 checks/layout.py
layout check: 3 tree(s) present
python3 checks/tables.py
table check: 11 command(s) and 7 declaration(s), each declared by the project and named by a table
python3 checks/links.py --online
link check: every reference in 6 document(s) resolved
python3 checks/vocabulary.py
vocabulary check: 34 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 20 source(s)
```

The build's suite runs ninety-eight tests where the base ran forty-eight. The corpus suite runs eighty-six where the base ran eighty-two; the four are the schema validation of the four fixtures this task adds. The table check is unchanged at eleven commands and seven declarations: this task adds no `Makefile` target and no dependency, `markdown-it-py` having been declared and locked already. The vocabulary check is unchanged at thirty-four terms: *profile*, *selected content* and *closure* are already marked by the design and already defined by the glossary, and this task marks no new term.

## T2 The profile clauses against the build's own parser

**Observes AC5, AC7, AC9.** Each clause of `## Markdown and source-heading profile` against the configuration in `prosiform.profile`, and each recognition rule in both of its directions.

```bash
cd prototype && uv run --frozen pytest tests/test_profile.py -q
```

**Pass.** Exit 0. Thirty-eight tests: the pinned version; pipe tables; double-tilde strikethrough; task markers as source text; typographic substitution off; raw HTML as a token of its own; a definition turning neither `[x]` nor `[X]` into a link; a bracketed label outside a marker position still resolving; four Markdown suffixes classified and four non-Markdown suffixes rejected; ten recognized constructs refused; ten look-alikes passing untouched; and a refusal naming its line and the spelling it found.

## T3 The command's statuses and diagnostics over a parsed source

**Observes AC7, AC9.** Each refusal reported as the input failure it is, each look-alike reaching the absent bundling stage, and each of the catalogued failures a run that reads files can now name.

```bash
cd prototype && uv run --frozen pytest tests/test_cli.py -q
```

**Pass.** Exit 0. Sixty tests, the forty-two W01 carried among them. The eighteen this task adds: six constructs failing with status 1, no code, and a `source` naming `guide.md` and a line; five look-alikes reaching status 4; a referring document read under the profile; a refusal naming `[[page]]` at `guide.md:3`; a suffix outside the profile failing; `GUIDE.MARKDOWN` accepted; an absent document failing with `E_TARGET_NOT_FOUND`; a reference normalizing outside the root failing with `E_SOURCE_OUTSIDE_ROOT`.

## T4 The corpus against the build, before and after

**Observes AC5, AC7, AC9.** Every fixture in the corpus, run against the build under test and compared with its manifest, at the base revision and at the tested revision.

```bash
PROSIFORM_BUILD=…/prototype/.venv/bin/prosiform python corpus.py
```

**Pass, as a measurement.** Both runs report **3 of 10 fixtures pass**, and the three are `cli/group-rule-depth`, `cli/group-rule-repeated-slug` and `cli/group-rule-unknown-slug`, which fail before any source is read.

The three older fixtures' pass count is **unchanged at 0 of 3**. Each still fails on its exit status, because each describes a run that publishes a bundle or resolves a reference, and neither stage exists:

```text
extraction/nested-section-target: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_NESTED_SECTION_TARGET expected, error (no code) produced
identity/whole-document: fail
  expected.exit_status: expected 0, the run exited 4
  expected.stdout: the bytes differ
    186 bytes expected, 0 produced
normalization/root-escape: fail
  expected.exit_status: expected 1, the run exited 4
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_SOURCE_OUTSIDE_ROOT expected, error (no code) produced
```

The four fixtures this task adds fail the same way and for the same reason, each reaching status 4 with no bundle:

```text
profile/extension-lookalikes: fail
  expected.exit_status: expected 0, the run exited 4
profile/html-in-a-code-example: fail
  expected.exit_status: expected 0, the run exited 4
profile/task-markers-and-typography: fail
  expected.exit_status: expected 0, the run exited 4
profile/task-markers-protected-from-definitions: fail
  expected.exit_status: expected 0, the run exited 4
```

That each reaches the absent bundling stage rather than a refusal is itself the observation the look-alike direction needs: the profile accepts all four sources, including the escaped wiki link, the code-span brace block and the HTML inside a code fence.

## F1 The task-marker protection removed

**Observes AC5.** The parse no longer returns a linked marker to text.

```python
if False and linked_marker(inline):
```

```bash
cd prototype && uv run --frozen pytest -q
```

**Failed as expected.** Exit 1, two tests.

```text
    @pytest.mark.parametrize("marker", ["[x]", "[X]"])
    def test_a_definition_cannot_turn_a_task_marker_into_a_link(marker: str) -> None:
        source = f"- {marker} done\n\n{marker}: page.md\n"
>       assert links(source) == []
E       AssertionError: assert ['page.md'] == []

FAILED tests/test_profile.py::test_a_definition_cannot_turn_a_task_marker_into_a_link[[x]]
FAILED tests/test_profile.py::test_a_definition_cannot_turn_a_task_marker_into_a_link[[X]]
```

Reverted.

## F2 The escape condition dropped from recognition

**Observes AC7.** Recognition stops reading the source the parser read, so an escaped spelling fires the rule.

```python
if found is None:
```

**Failed as expected.** Exit 1, two tests, both naming the escaped case and nothing else.

```text
FAILED tests/test_cli.py::test_a_source_the_profile_accepts_reaches_the_absent_stage[# Guide\n\nAn escaped \\[\\[page\\]\\] is literal text.\n]
FAILED tests/test_profile.py::test_prose_resembling_a_construct_passes_untouched[An escaped \\[\\[page\\]\\] is literal text.\n]
```

Reverted.

## F3 The text-children condition dropped from recognition

**Observes AC7, AC9.** Recognition reads the raw inline source instead of the text the parser left as text, so a code span fires the rule.

```python
found = pattern.search(inline.content)
```

**Failed as expected.** Exit 1, three tests, each naming a code span.

```text
FAILED tests/test_cli.py::test_a_source_the_profile_accepts_reaches_the_absent_stage[# Guide\n\nA code span naming `[[page]]` is prose about a wiki link.\n]
FAILED tests/test_profile.py::test_prose_resembling_a_construct_passes_untouched[A code span naming `[[page]]` is prose about a wiki link.\n]
FAILED tests/test_profile.py::test_prose_resembling_a_construct_passes_untouched[A regular expression `[^abc]` matches one character.\n]
```

Reverted.

## F4 The refusal not raised

**Observes AC7, AC9.** The command parses each source and ignores what the profile refuses, so every refused source reaches the absent bundling stage instead.

```python
if False and refusal is not None:
```

**Failed as expected.** Exit 1, nine tests.

```text
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n<div>raw</div>\n]
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nA paragraph carrying <span>raw</span> markup.\n]
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nSee [[page]] for the procedure.\n]
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n![[page]]\n]
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\nA claim[^1] needing support.\n]
FAILED tests/test_cli.py::test_a_construct_the_profile_refuses_fails_the_run[# Guide\n\n## Run {#custom-id}\n]
FAILED tests/test_cli.py::test_the_referring_document_is_read_under_the_profile
FAILED tests/test_cli.py::test_a_refusal_names_the_construct_and_where_it_sits
FAILED tests/test_cli.py::test_a_fragment_reference_reads_the_whole_document_it_names
```

Reverted.
