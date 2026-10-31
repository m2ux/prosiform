# Validation — W10 A Folder Key's Absent Substitute and Unused Report

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i08/e07/w10-a-folder-key-s` on branch `i08/e07/w10-a-folder-key-s`, at branch head `b4a39250` unless a section names another revision. The build under test was named by `PROSIFORM_BUILD` as the worktree's own `src/.venv/bin/pf`.

The design clause the fixtures declare is `Link classification and resource handling — The substitution mapping`, read at `a59b62fca8ad2a155e4e32ac7857761b871cf304`, the revision `README.md` pins. The pin does not move: this row adds a shape of the mapping, not a clause.

## T1 — The two fixtures pass against the build

**Ran:** `make corpus` at `b4a39250`.

**Observed:** exit `0`.

```text
mock/an-unused-folder-key-warns: pass
mock/a-folder-substitute-that-is-absent-fails: pass
corpus check: 373 fixture(s), 373 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 371 to 373, which is the two this row lands.

## T2 — Each fixture fails against the code before the change

This is the check the epic's own record warns about. W05's corpus fixture passed both ways, so a fixture is not evidence until it has been shown to fail without the change.

**Ran:** `checks/corpus.py` at `b4a39250` with `PROSIFORM_BUILD` naming the build at `/tmp/w10base`, a clean checkout of `origin/i08/e07/main` at `40a3b947` built with `uv sync --frozen`. The whole corpus ran; the two fixtures below are the only ones this row adds.

**Observed:** exit `1`, two failures and no others.

```text
mock/a-folder-substitute-that-is-absent-fails: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    'stubs/blue.md' is absent
    produced "the reference 'rules/blue.md' names no document under the allowed source root"
  expected.diagnostics: diagnostic 1 carries no resolved
    expected resolved 'stubs/blue.md'
mock/an-unused-folder-key-warns: fail
corpus check: 373 fixture(s), 371 pass, 2 fail, 0 awaited, 0 unexpected pass
```

Each difference is the row's own claim, read from the other side:

- **`a-folder-substitute-that-is-absent-fails`.** The base does refuse the run, with the right code and the right status, but the message is the one every absent target carries: it names the reference and stops. Nothing states the key that derived the path, and no `resolved` field names it, so a reader of the message cannot tell an author's absent link from a folder key's absent substitute.
- **`an-unused-folder-key-warns`.** The base performs the redirect the folder key derived for `notes/note.txt` — a resource — and records a substitution for it, so it states `W_MOCK_SUBSTITUTED` where the fixture declares `W_MOCK_UNUSED`. This is the fault the row corrects: a redirect the bundle does not carry out is not a substitution, and a key that produced only such redirects substituted nothing.

**And the unit cases the same way.** The branch's `src/tests/test_mock.py` was copied over the base's and run against the base package. Two cases fail, and no other case in the file does.

```text
FAILED tests/test_mock.py::test_a_folder_substitute_that_is_absent_names_all_three
FAILED tests/test_mock.py::test_a_folder_key_answering_only_text_is_unused
2 failed, 91 passed in 0.21s
```

The five further cases this row adds pass on the base as well, which is what they are for: `test_a_folder_substitute_that_is_absent_is_refused` and `..._publishes_nothing` hold the status and the empty publication the base already reaches, `test_a_document_key_naming_an_absent_document_keeps_its_shape` holds the behaviour the row deliberately leaves alone, and `test_a_folder_key_answering_only_text_publishes_the_reference_as_authored` compares a bundle whose bytes do not move with the change. They are regression guards rather than evidence of this row's claim, and none is counted as proof.

## T3 — The three-part refusal, from the command line

**Ran:** `pf -d json -m rules/=stubs/ guide.md` over the `a-folder-substitute-that-is-absent-fails` tree, at `b4a39250`.

**Observed:** exit `1`.

```json
{"severity": "error", "message": "the reference 'rules/blue.md' is redirected by the mapping key 'rules/' to 'stubs/blue.md', which names no document under the allowed source root", "code": "E_TARGET_NOT_FOUND", "reference": "rules/blue.md", "resolved": "stubs/blue.md", "source": "guide.md:3", "chain": ["guide.md", "stubs/blue.md"], "remedy": "name a folder whose documents the key's remainder reaches"}
```

The three parts the criterion names are the reference as its author wrote it (`rules/blue.md`), the key (`rules/`) and the path the redirect resolved to (`stubs/blue.md`). The location and the chain are the ones an absent target already carries. The remedy states the fix a folder key's author can make: the substitute folder has no document at that remainder.

## T4 — A document key's message is unchanged

**Ran:** `src/tests/test_mock.py::test_a_document_key_naming_an_absent_document_keeps_its_shape`, and the corpus at `b4a39250`.

**Observed:** pass. The message is still `the reference 'absent.md' names no document under the allowed source root`, with no `resolved` field and no mention of a mapping key. The absence of a document key is decided by the mapping grammar rather than at the read, so the refusal's shape is the one every author-written absent target receives.

## T5 — An unused folder key warns once

**Ran:** `pf -d json -m rules/=stubs/ -m notes/=stubs/ -m other/=spare/ guide.md` over the `an-unused-folder-key-warns` tree, at `b4a39250`.

**Observed:** exit `0`, and these four warnings.

```text
W_RESOURCE_PORTABILITY    the bundle names at least one resource
W_MOCK_SUBSTITUTED        source rules/red.md   resolved stubs/red.md
W_MOCK_SUBSTITUTED        source rules/blue.md  resolved stubs/blue.md
W_MOCK_UNUSED             source notes/
W_MOCK_UNUSED             source other/
```

`rules/` answered two references and states two `W_MOCK_SUBSTITUTED`, one per target, and no `W_MOCK_UNUSED` — the used set holds the key, not the references it served. `notes/` answered one reference whose target is text, and `other/` answered none; each states one `W_MOCK_UNUSED`, in the spelling its caller wrote, separator included.

## T6 — The reading the work item asks for: a folder matching only text

**Ran:** `pf -d json -m rules/=stubs/ guide.md` over a tree whose only `rules/` reference is `rules/note.txt`, at `b4a39250`; and the same tree at `40a3b947`.

**Observed:** at `b4a39250`, exit `0` with `W_MOCK_UNUSED` naming `rules/` and the bundle carrying `(rules/note.txt)` as authored. At `40a3b947`, exit `0` with `W_MOCK_SUBSTITUTED` naming `stubs/note.txt` — a substitution for a link the bundle publishes unchanged, which is the report the row corrects.

The outcome is a **warning case**, and `w10.md` states why: the warning follows from the mechanism rather than being added to it, because a redirect whose substitute is a resource is one the bundle does not perform, so the key served no compiled reference.

## T7 — `make conformance` maps the clause against the fixtures naming it

**Ran:** `make conformance` at `b4a39250`, and at `40a3b947` for comparison.

**Observed:** exit `0` at both.

```text
b4a39250: Link classification and resource handling — The substitution mapping: 25 fixture(s)
40a3b947: Link classification and resource handling — The substitution mapping: 23 fixture(s)
conformance report: 305 clause(s) the design states, 54 covered by no fixture, 0 declaration(s) naming no clause; 37 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes
```

The clause count stays at 305 and the uncovered count at 54, so the fixtures reach a clause the corpus already covered rather than a new one. Both report every figure identically, so this row adds no uncovered clause and no unnamed declaration.

## T8 — `make invocation` still agrees with the help output

**Ran:** `make invocation` at `b4a39250`.

**Observed:** exit `0`, `30 statement(s)`. The option's row and its help string are unchanged: this row adds a shape of the value rather than an option. The folder form's documented row is `AC29`'s and lands with `W11`.

## T9 — `make independence` finds no implementation term in the new claims

**Ran:** `make independence` at `b4a39250`.

**Observed:** exit `0`, `every shaped term of every fixture declaration and every report entry is one the contract names`. The new descriptions and carried substrings state `folder`, `key`, `reference`, `document`, `substitute`, `resource`, `text` and `identity`, each a term the contract names.

## T10 — The other mapping behaviour is unchanged

**Ran:** `make test` at `b4a39250`; and `src/.venv/bin/python -m pytest` in the worktree and in the clean base checkout at `40a3b947`, for comparison.

**Observed:** `make test` at head reports `1401 passed`, exit `0`. The base at `40a3b947` collects `1395` cases, so the difference is the six this row adds to `test_mock.py`.

A direct `.venv/bin/python -m pytest` invocation reports `6 failed, 1395 passed` at head and `6 failed, 1389 passed` at the base: the same six `test_handoff_round_trip.py` publication cases, failing with `E_PUBLICATION_FAILED` because the atomic folder swap is refused where `/tmp` holds the target. The six reproduce identically on the clean base, so they are the environment difference the delivery brief names and not this row's. The two invocation styles differ because `uv run` is what `make test` uses and it does not place the run's temporary folder where the direct invocation does.

The cases covering the document key, the fragment key, the four existing refusals, the entry redirect, the two warnings, the substitute as a source and the dispatch and deferral targets pass unchanged under both.

## T11 — `make check`

**Ran:** every target of `make check` on branch head `b4a39250`, in the Makefile's order. Exit `0`.

| Target | Observed |
| --- | --- |
| `lock-check` | `Resolved 24 packages`, no resolution |
| `lint` | `All checks passed` |
| `format-check` | `179 files already formatted` |
| `typecheck` | `Success: no issues found in 81 source files` |
| `test` | `1401 passed` |
| `harness` | `1029 passed` |
| `authoring` | `0 finding(s)` |
| `corpus` | `373 fixture(s), 373 pass` |
| `smoke` | wheel built, installed and run outside the repository; `ok` on every line |
| `layout` | `4 tree(s) present` |
| `tables` | `22 command(s) and 8 declaration(s)`, each declared by the project and named by a table |
| `links --online` | every reference in 212 documents resolved |
| `vocabulary` | `3332 term(s)` |
| `invocation` | `30 statement(s)` |
| `conformance` | `305 clause(s)`, `54 covered by no fixture`, `0 declaration(s) naming no clause` |
| `independence` | every shaped term is one the contract names |
| `steps` | every procedure in 59 documents |
| `mock-scenarios` | `5 scenario(s), 5 pass` |

The delivery brief expects `test_linked_bootstrap` and the publication tests to fail in this sandbox. `test_linked_bootstrap` passes here, which means this host reaches the package index; the publication tests fail on the `/tmp` swap as T10 records, and they are asserted against the base in T10 rather than counted as this row's.

## T12 — Delivery

**Ran:** `gh api` against the pull request, its checks and the epic.

**Observed:** the pull request [merged](https://github.com/m2ux/prosiform/pull/469) to `i08/e07/main` at `01653cf8725ced5ff737de32dc8cd925ebb62d8a`, merged from head `b4a39250`. Its `Checks` run reported `success` on `b4a39250` and `success` on the merge commit `01653cf8`.

`sync.py` mapped epic row `W10` to #469, reported `AC27` and `AC28` ready to verify, and reported row `W10` delivered once the pull request merged. The body it produced was published for the row and the two criteria, and row `W10` reads `✓`.

**One blocker, this row does not clear.** The Development link to #414 could not be set: `addCloseIssueReferences` answered `Issue exceeds manual reference limit`, because ten pull requests already hold that issue's manual references — #425, #428, #431, #433, #437, #438, #439, #440, #446 and #447. No slot is free, and unlinking another row's record is not this row's to do. The pull request number to be linked is **#469**, whose node id is `PR_kwDOVNSvEM8AAAABL9uVFQ`, against issue node id `I_kwDOVNSvEM8AAAABbF3srA`. That mutation is the one command still to be run for this delivery.

**Findings this row does not cause and does not change:**

- `sync.py` reports eleven rows — `W00` to `W09` and `W12` — as linking pull requests whose titles do not name `I08:E07`. Each merged under the epic's old reference, `[I05:E09]`, so the conflict is a fact about the titles rather than about the delivery. #469 is the first row whose title names the epic's current reference.
- `sync.py` reports `AC6`, `AC11` and `AC20` unticked on rows it otherwise reads as delivered, and its rewrite clears the Done cells of `W01` and `W07`. That disagreement predates this row, so those two cells and the three criteria are left as they stood.
