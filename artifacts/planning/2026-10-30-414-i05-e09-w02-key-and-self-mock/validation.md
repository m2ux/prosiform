# Validation — W02 Key and Self-Mock Refusals

> Evidence record · Created 2026-10-30

Every check below ran in the worktree `.worktrees/i05/e09/w02-key-and-self-mock` on branch `i05/e09/w02-key-and-self-mock`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as `<worktree>/src/.venv/bin/pf`, the command the continuous-integration job supplies through `uv run --project src --frozen pf`.

The design clause the fixtures declare is `a59b62fca8ad2a155e4e32ac7857761b871cf304`, which `README.md` pins and which W01's correction moved the pin to.

## T1 — The three fixtures pass against the build

**Ran:** `make corpus`, at branch head `c9390ac3`, 355 fixtures.

**Observed:** exit `0`.

```text
mock/a-citation-outside-the-root-is-redirected: pass
mock/a-duplicate-key-is-refused: pass
mock/a-fragment-only-key-is-refused: pass
mock/a-key-naming-an-absent-document-is-substituted: pass
mock/a-mocked-dependency-is-compiled: pass
mock/a-self-mock-is-refused: pass
mock/a-substitute-outside-the-writing-root-is-reachable: pass
corpus check: 355 fixture(s), 355 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 352 to 355, which is the three this row lands.

## T2 — The same three fixtures fail against the code before the change

**Ran:** `checks/corpus.py` at `164a5200`'s `src/prosiform/cli.py`, installed into the same build, with the three new fixtures in place.

**Observed:** exit `1`, three failures and no others.

```text
mock/a-duplicate-key-is-refused: fail
mock/a-fragment-only-key-is-refused: fail
mock/a-self-mock-is-refused: fail
corpus check: 355 fixture(s), 352 pass, 3 fail, 0 awaited, 0 unexpected pass
```

Each fixture therefore holds the change rather than the tree it runs over.

## T3 — What the refusals say, through the JSON stream

**Ran:** `pf -d json <arguments> -c guide.md` in each fixture's `source`, and the same for two shapes no fixture states.

| Command line | Status | Message |
| --- | --- | --- |
| `-m rules.md=a.md -m ./rules.md=b.md` | `2` | `the mapping keys 'rules.md' and './rules.md' name one identity, so only one of them can redirect it` |
| `-m rules.md=./rules.md` | `2` | `the mapping entry 'rules.md'='./rules.md' names one identity on both sides, so the substitute stands in for itself` |
| `-m #escalation=stand-in.md` | `2` | `the mapping key '#escalation' names no document to redirect, so no reference can name it` |
| `-m rules.md=stand-in.md -m rules.md=guide.md` | `2` | the same duplicate message, with both spellings read as `rules.md` |
| `-m #a=#b` | `2` | the documentless message, naming `#a` |

Each carries `E_INVALID_USAGE` and `"remedy": "run pf -h for usage"`. The fifth row is the ordering the plan's second review addition records: a fragment-only key is refused as documentless rather than compared to its substitute as two empty identities, which would have reported a self-mock for a pair naming no document at all.

## T4 — The refusals are decided before any source is read

**Ran:** `src/tests/test_mock.py::test_a_mapping_shape_is_refused_before_any_source_is_read`.

**Observed:** pass. The run is given a duplicate key pair and the entry `absent.md`, and reports `E_INVALID_USAGE` at status `2` rather than the `E_TARGET_NOT_FOUND` at status `1` that reading the entry would give. `substitution` runs in `execute` before `entry` resolves the positional references, so the mapping is the whole of what a refusal reads.

## T5 — A document key and a section key of it are two keys

**Ran:** `src/tests/test_mock.py::test_a_document_key_and_a_section_key_of_it_are_two_keys`.

**Observed:** pass. `-m rules.md=stand-in.md -m rules.md#escalation=guide.md` compiles the substitute, so the identity a key names is its document and its section together and the duplicate check does not refuse two keys that state two different things.

## T6 — The message names both authored spellings

**Ran:** `src/tests/test_mock.py::test_two_spellings_of_one_key_are_refused_naming_both`, `::test_a_self_mock_is_refused` and `::test_a_key_carrying_no_document_is_refused`.

**Observed:** pass. The duplicate case asserts the message carries `rules.md` and `./rules.md`, which is the whole point of keeping the authored text beside the identity set: a set alone can say a key repeats one and not which two options to edit.

## T7 — `make conformance` maps the clause against the fixtures naming it

**Ran:** `make conformance` at `c9390ac3`.

**Observed:** exit `0`.

```text
CLI contract — -m ORIGINAL=ALTERNATIVE: 7 fixture(s)
Link classification and resource handling — The substitution mapping: 7 fixture(s)
Exit status and JSON diagnostics — 2: 9 fixture(s)
conformance report: 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; ...
```

The mapping's clause count rose from 4 to 7, the option's row from 4 to 7, and the exit status from 6 to 9 — the three fixtures, each naming four clauses. The clause count and the uncovered count are unchanged, which is what a row that adds fixtures rather than clauses must show.

Each manifest's declaration is `Link classification and resource handling — The substitution mapping`, `CLI contract`, `CLI contract — -m ORIGINAL=ALTERNATIVE` and `Exit status and JSON diagnostics — 2`. The first is the clause the epic's `fixtures.md` requires of every mock fixture; the other three are the rules the run reaches when it refuses, and `0 declaration(s) naming no clause` states that each resolves against the pinned design.

## T8 — `make invocation` still agrees with the help output

**Ran:** `make invocation` at `c9390ac3`.

**Observed:** exit `0`, `30 statement(s)`. The option's row is unchanged, because this row adds refusals rather than grammar.

## T9 — `make independence` finds no implementation term in the new claims

**Ran:** `make independence` at `c9390ac3`.

**Observed:** exit `0`, `every shaped term of every fixture declaration and every report entry is one the contract names`. The new descriptions and carried substrings state `rules.md`, `./rules.md`, `#escalation`, `one identity`, `one identity on both sides` and `no document`, none of which is a term the contract does not name.

## T10 — `make check`

**Ran:** every target of `make check` on branch head `c9390ac3`, in the Makefile's order.

**Observed:** exit `0` throughout.

- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `177 files already formatted`; `typecheck` — `Success: no issues found in 79 source files`.
- `test` — 1338 passed; `harness` — 969 passed.
- `authoring` — `0 finding(s)`.
- `corpus` — `355 fixture(s), 355 pass`.
- `smoke` — the installed command is named on the path, independent of the working directory and of this repository.
- `layout` — `4 tree(s) present`.
- `tables` — `21 command(s) and 8 declaration(s)`.
- `links --online` — `every reference in 212 document(s) resolved`.
- `vocabulary` — `46 contract term(s) ... on a59b62fca8ad2a155e4e32ac7857761b871cf304`.
- `invocation` — `30 statement(s)`.
- `conformance` — `305 clause(s)`, `55 covered by no fixture`, `0 declaration(s) naming no clause`.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — `every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`.

`test` reports 1338 passed and `harness` 969 passed. `src/tests/test_mock.py` collects 30 tests, up from the 25 the branch's base carries, which is the five this row adds beside the parametrized pair case already there.

## T11 — Delivery

**Ran:** `gh api` against the pull request and the epic base.

**Observed:** the pull request [merged](https://github.com/m2ux/prosiform/pull/431) to `i05/e09/main` at `b91e45ff779483ab3d983286d475e73bfb0ecf5e`; its `Checks` run reported `success` on `c9390ac3` at `20:23:33Z`, and the base's own run reported `success` on the merge commit `b91e45ff`. It holds a Development link to #414, verified through `closingIssuesReferences`. `sync.py` linked row `W02` to #431, ticked `AC9`, `AC10` and `AC23`, and the body it wrote was published; row `W02` reads `✓`.

The same `sync.py` run reports one finding this row did not cause and does not change: `#428 W01: AC15 covered and named by no test`, which is W01's pull request body declaring `AC15` in a way `format.py` reads as a row's coverage. It is left standing rather than edited, because #428 is merged and its body is not this row's to rewrite.
