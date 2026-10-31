# Validation — W10 A Value Naming No Markdown Document

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w10-a-value-naming-no` on branch `i05/e09/w10-a-value-naming-no`, at branch head `d33beb15` unless a section names another revision. The build under test was named by `PROSIFORM_BUILD` as the worktree's own `src/.venv/bin/pf`, the command the continuous-integration job supplies through `uv run --project src --frozen pf`.

The design clause the fixture declares is `a59b62fca8ad2a155e4e32ac7857761b871cf304`, the revision `README.md` pins.

## T1 — The fixture passes against the build

**Ran:** `make corpus` at `d33beb15`.

**Observed:** exit `0`.

```text
mock/a-value-naming-no-markdown-document-is-refused: pass
corpus check: 366 fixture(s), 366 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 365 to 366, which is the one this row lands.

## T2 — The same fixture fails against the code before the change

**Ran:** `checks/corpus.py` at `097160bd`'s `src/prosiform/cli.py`, placed ahead of the branch's own package on `PYTHONPATH`, with the new fixture in place.

**Observed:** exit `1`, one failure and no others.

```text
mock/a-value-naming-no-markdown-document-is-refused: fail
  expected.exit_status: expected 2, the run exited 0
  expected.bundles: the run wrote guide.bundle.md, which the manifest declares no bundle for
    53 bytes written, beginning b'# Guide\n\nRequire [the sh'
  expected.diagnostics: the run emits 1 diagnostic where 1 diagnostic is expected
    position 1: error E_INVALID_USAGE expected, warning W_MOCK_SUBSTITUTED produced
corpus check: 366 fixture(s), 365 pass, 1 fail, 0 awaited, 0 unexpected pass
```

The three differences are the row's whole claim: no refusal, a published bundle, and a warning in place of the error. The bundle it wrote is 53 bytes holding the link as its author wrote it, which is the entry taking effect as nothing.

**And the three unit cases the same way:** `src/tests/test_mock.py` with that same code ahead of the package reports three failures, and no other case in the file fails:

```text
FAILED src/tests/test_mock.py::test_a_value_naming_no_markdown_document_is_refused
FAILED src/tests/test_mock.py::test_a_value_naming_no_markdown_document_names_the_entry_it_author_wrote
FAILED src/tests/test_mock.py::test_a_value_naming_no_markdown_document_publishes_nothing
```

Each of the three asserts a status of `2` and meets `0`, which is the defect the row exists to close: the entry read as a redirect and took effect as nothing.

## T3 — What the defect looked like before the change

**Ran:** `pf -c -m rules.md=notes.txt guide.md` and `pf -m rules.md=notes.txt guide.md` over a tree whose `guide.md` links `rules.md`, against the code at `097160bd`.

| Command line | Status | What the run reported |
| --- | --- | --- |
| `pf -c -m rules.md=notes.txt guide.md` | `0` | `W_MOCK_SUBSTITUTED` naming `notes.txt` as the substitute, and nothing else |
| `pf -m rules.md=notes.txt guide.md` | `0` | the same warning, and a published bundle carrying `[the shared rules](rules.md)` as the source wrote it |

The warning states a substitution the bundle does not show. Both runs fail nothing, which is the disagreement between what the entry reads as and what it does.

## T4 — What the refusal says, through the JSON stream

**Ran:** `pf -d json -m rules.md=notes.txt guide.md` at `d33beb15`.

**Observed:** status `2`.

```json
{"severity": "error", "message": "the mapping entry 'rules.md'='notes.txt' gives a substitute naming no Markdown document, so the reference it redirects could only be published as text", "code": "E_INVALID_USAGE", "reference": "notes.txt", "remedy": "run pf -h for usage"}
```

The message names the pair its author wrote — `'rules.md'` and `'notes.txt'` — and the reference is the substitute, which is the side of the entry to edit. `E_INVALID_USAGE` and `run pf -h for usage` are what the three existing refusals carry, so a caller has one remedy for any malformed command line.

## T5 — The refusal is decided before any source is read

**Ran:** `src/tests/test_mock.py::test_a_value_naming_no_markdown_document_publishes_nothing`.

**Observed:** pass. The run is refused at status `2` and the `-o` folder holds no file, so the entry the mapping redirects is never opened and nothing is published. `substitution` runs in `execute` before `entry` resolves a positional reference, so the refusal reads the command line and nothing else.

## T6 — The message names the entry its author wrote

**Ran:** `src/tests/test_mock.py::test_a_value_naming_no_markdown_document_is_refused` and `::test_a_value_naming_no_markdown_document_names_the_entry_it_author_wrote`.

**Observed:** pass. The first asserts the code and the phrase `no Markdown document`; the second asserts both authored sides — `rules.md` and `notes.txt` — and that `reference` is the substitute.

## T7 — The three existing refusals are unchanged

**Ran:** `src/tests/test_mock.py` at `d33beb15`.

**Observed:** 62 tests pass, up from the 59 the branch's base carries, which is the three this row adds. The cases covering the duplicate key, the self-mock, the documentless key, the two keys of one document and the ordering ahead of an absent entry all pass, so the fourth test neither shifts the answer a pair with a Markdown substitute receives nor changes the order the other three answer in.

## T8 — `make conformance` maps the clause against the fixtures naming it

**Ran:** `make conformance` at `d33beb15`.

**Observed:** exit `0`.

```text
CLI contract — -m ORIGINAL=ALTERNATIVE: 8 fixture(s)
Link classification and resource handling — The substitution mapping: 18 fixture(s)
Exit status and JSON diagnostics — 2: 10 fixture(s)
conformance report: 305 clause(s) the design states, 54 covered by no fixture, 0 declaration(s) naming no clause; ...
```

The mapping's clause count rises from 17 to 18, the option's row from 7 to 8 and the exit status from 9 to 10 — one fixture, declaring four clauses. The clause count stays at 305 and the uncovered count falls from 55 to 54, so the fixture reaches a clause the corpus did not.

Each manifest declares `Link classification and resource handling — The substitution mapping`, `CLI contract`, `CLI contract — -m ORIGINAL=ALTERNATIVE` and `Exit status and JSON diagnostics — 2`: the clause the epic's `fixtures.md` requires of every mock fixture, and the three rules a refusing run reaches.

## T9 — `make invocation` still agrees with the help output

**Ran:** `make invocation` at `d33beb15`.

**Observed:** exit `0`, `30 statement(s)`. The option's row is unchanged, because this row adds a refusal rather than grammar.

## T10 — `make independence` finds no implementation term in the new claims

**Ran:** `make independence` at `d33beb15`.

**Observed:** exit `0`, `every shaped term of every fixture declaration and every report entry is one the contract names`. The new description and carried substrings state `rules.md`, `notes.txt`, `no Markdown document`, `Markdown`, `substitute` and `text`, each a term the contract names.

## T11 — `make check`

**Ran:** every target of `make check` on branch head `d33beb15`, in the Makefile's order.

**Observed:** every target green except the two this sandbox cannot run, set out below.

- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `179 files already formatted`; `typecheck` — `Success: no issues found in 81 source files`.
- `test` — `1371` collected: `1358 passed, 13 errors`.
- `harness` — `1022 passed`.
- `authoring` — `0 finding(s)`.
- `corpus` — `366 fixture(s), 366 pass`.
- `layout` — `4 tree(s) present`; `tables` — `21 command(s) and 8 declaration(s)`; `links --online` — `every reference in 212 document(s) resolved`.
- `vocabulary` — `3332 term(s)`.
- `invocation` — `30 statement(s)`; `conformance` — `305 clause(s)`, `54 covered by no fixture`, `0 declaration(s) naming no clause`; `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — `every procedure in 59 document(s)`.
- `mock-scenarios` — `5 scenario(s), 5 pass`.

**The two targets this sandbox cannot run:**

- `make smoke` fails because it installs the wheel into a throwaway environment and the sandbox has no network: `Failed to fetch: https://pypi.org/simple/ruamel-yaml/`, `dns error`.
- `make check`'s `test` target reports `1358 passed, 13 errors`, all thirteen in `tests/test_linked_bootstrap.py`, each an `uv pip install` of that same wheel failing for the same absent network. The publication tests, which the brief names as failing on `/tmp`'s inability to take the atomic folder swap, pass on this branch.

Both reproduce on this host wherever the sandbox has no network, and neither names this change: `make test` in the settled W02 worktree at its own head reports `1325 passed, 13 errors` with the same thirteen ids, and a clean checkout of `origin/i05/e09/main` cannot be built at all here because `uv` must fetch `hatchling` to build it. The `test` target's count is up by 33 from that worktree, none of which is an error.

## T12 — Delivery

**Ran:** `gh api` against the pull request, its Test Plan and the epic.

**Observed:** the pull request [merged](https://github.com/m2ux/prosiform/pull/446) to `i05/e09/main` at `f21985cc5efffb51cff53c7716a228b85ff46733`, merged from head `d33beb15`. Its `Checks` run reported `success` on `d33beb15` at `06:46:57Z`, the pull request read `mergeable: true`, `mergeable_state: clean` against `i05/e09/main`, and the base's own `Checks` run reported `success` on the merge commit `f21985cc`.

Its Development link to #414 was set with `addCloseIssueReferences` and read back through `closingIssuesReferences`, which reports `{number: 414}`. That mutation ran before the merge, so it needed no reference freed by another row; it did not answer `Issue exceeds manual reference limit`.

`sync.py` linked epic row `W12` to #446, reported `AC24` ready to verify, ticked it, and reported `done: W12`. The body it wrote was published, and row `W12` reads `✓`.

The epic's rows were renumbered while this session ran, from a folder pairing migrating in as W09–W11. This row moved from `W10` to `W12`; the record folder keeps its `w10` name because that is the identity the brief and [#432](https://github.com/m2ux/prosiform/issues/432) name it by.

**One finding this row does not cause and does not change:** `sync.py` reports `#428 W01: AC15 covered and named by no test`, which is W01's pull request body declaring `AC15` in a way `format.py` reads as a row's coverage. #428 is merged and its body is not this row's to rewrite, so it is left standing, as W02's record also left it.
