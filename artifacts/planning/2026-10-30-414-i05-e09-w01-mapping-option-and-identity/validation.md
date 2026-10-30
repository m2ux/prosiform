# Validation — W01 Mapping, Option and Identity

> Evidence record · Created 2026-10-30

Every check below ran in the worktree `.worktrees/i05/e09/w01-mapping-option-and-identity` on branch `i05/e09/w01-mapping-option-and-identity`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as `env PYTHONPATH=<worktree>/src <venv>/pf`, the same form the continuous-integration job supplies.

The design clause the fixtures declare is `f723a85dbe5fd2a3e379b951c2dfb5c58670f5e6`; the option's own `CLI contract` row is `9f58475d439693b04d4b84aa59527d6839eaf281`, which is the revision `README.md` now pins. W00 landed the first; this session landed the second.
    10|
## T1 — The three fixtures pass against the build

**Ran:** `make corpus`, at branch head `1a156299`, 351 fixtures.

**Observed:** exit `0`.

```text
mock/a-key-naming-an-absent-document-is-substituted: pass
mock/a-mocked-dependency-is-compiled: pass
mock/a-substitute-outside-the-writing-root-is-reachable: pass
corpus check: 351 fixture(s), 351 pass, 0 fail, 0 awaited, 0 unexpected pass
```

AC1, AC11 and AC18 each have the fixture the epic names. The count rose from 348 to 351, which is the three this row lands.
    20|
## T2 — The same trees without a mapping are refused

**Ran:** `pf -d json guide.md` in the fixture roots of `a-substitute-outside-the-writing-root-is-reachable` and `a-key-naming-an-absent-document-is-substituted`, each without `-m`.

**Observed:** exit `1` in both, with `E_TARGET_NOT_FOUND` naming `rules.md`:
    30|
```text
{"severity": "error", "message": "the reference 'rules.md' names no document under the allowed source root", "code": "E_TARGET_NOT_FOUND", "reference": "rules.md", "source": "guide.md:8", "chain": ["guide.md", "rules.md"]}
```

That pair is what makes AC11 and AC18 statements about the mapping rather than about the trees: the only difference between the pass and the refusal is `-m`. The manifests themselves cannot state the refusal, because a fixture declares one invocation and the runner compares it whole.
    40|
## T3 — The mapping is applied after the root check

**Ran:** `src/tests/test_mock.py::test_the_root_is_held_against_the_authored_path_before_the_mapping` and `::test_a_substitute_outside_the_writing_source_root_is_reached`.

**Observed:** both pass. A reference the authored root refuses still raises `OutsideRoot` however the mapping names its key, and a reference the authored root holds resolves to a substitute the root cannot contain. Applying the mapping before `covers` would fail the second case, which is the defect the epic's review found in the plan.

## T4 — The lookup's precedence
    50|
**Ran:** `src/tests/test_mock.py`, 22 tests.

**Observed:** pass. The cases that decide the order:

- `test_a_fragment_key_takes_the_section_it_names` — an exact `(path, fragment)` key wins.
- `test_a_document_key_covers_every_fragment_of_its_document` — a `(path, None)` key redirects the document and leaves the reference its section.
- `test_a_fragment_key_leaves_another_section_of_the_document_alone` — a section key does not narrow the document key beside it.
- `test_a_key_is_the_identity_a_reference_normalized_to` — `./docs/rules.md` from one directory and `rules.md` from another name one key.
- `test_a_mapping_is_a_value_the_run_cannot_rewrite` — the keys are a read-only view.

The first version of `substitute` returned the substitute's own fragment for a document key, which dropped the section the reference named. `test_a_document_key_covers_every_fragment_of_its_document` failed on it, and the method now returns the reference's fragment for that branch.
    60|
## T5 — Both resolution paths take the mapping

**Ran:** `src/tests/test_mock.py::test_a_mapped_entry_derives_its_name_from_the_substitute` and a manual run.

**Observed:** `pf -m guide.md=stand-in.md guide.md` writes `stand-in.bundles/stand-in.bundle.md`. The positional path is `cli.entry`, which applies the mapping after `resolve`; the link path is `closure.inside`. Both are held: a mapping threaded through `inside` alone would leave the command line's own reference unredirected.

## T6 — No stage resolves without the mapping

**Ran:** a read of every call site of `inside`, `resolvable`, `bundled`, `withholding_target` and `entry`.
    70|
**Observed:** each takes the mapping. `cli.required`, `cli.withheld`, `cli.dispatches`, `cli.refusals_of_operators`, `bundle.target`, `bundle.group`, `bundle.emitted_visible`, `grouping.prepared`, `dispatch.written_in`, `candidate.intended` and `candidate.preserved` pass it through. The second and third reads are what the row exists for: `bundle.target` rewrites the destination and `candidate.intended` compares it, so a mapping held only at discovery would emit the authored target and fail validation against the mocked one.

## T7 — A dispatched target's bundle takes the same mapping

**Ran:** a manual run over a tree whose `guide.md` dispatches `rules.md`, with `-m rules.md=stand-in.md`.

**Observed:** exit `0`; `guide.bundles/` holds `guide.bundle.md` and `stand-in.bundle.md`, and the dispatch sub-section names `stand-in.bundle.md`. `cli.dispatched_set` passes the mapping to each dispatched compilation.

## T8 — `make conformance` maps both clauses

**Ran:** `make conformance` at branch head `1a156299`, with `README.md` pinned to `9f58475d`.

**Observed:** exit `0`.
    80|
```text
CLI contract — -m ORIGINAL=ALTERNATIVE: 3 fixture(s)
Link classification and resource handling — The substitution mapping: 3 fixture(s)
conformance report: 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; ...
```

The clause count rose from 304 to 305, which is the option's row, and the uncovered count fell from 56 to 55. The option's row was **uncovered** on the first run — `0 fixture(s)` — because every manifest declared only the mapping's clause; each of the three now names the option's row as its second clause.

## T9 — `make invocation` fails until the row exists, and passes with it
    90|
**Ran:** `make invocation` at `1a156299` before and after the `invocation.md` row was written.

**Observed:** exit `1` before:

```text
FAIL -m, --mock ORIGINAL=ALTERNATIVE — the command offers this option and no table names it
invocation check: 1 documentation fault(s)
```

and exit `0` after, `30 statement(s)`, up from the 29 W00 recorded. This is the plan correction this session applied: `w01.md` held that `invocation.md`'s row belonged to W09, on the ground that the row cannot exist before the option does. That is true, and it is also why the row cannot wait for W09 — `checks/invocation.py` compares the table with the help output in **both** directions, so an option the command offers and no table names fails the check, and `make check` runs it.
    100|
## T10 — `make check`

**Ran:** every target of `make check` on branch head `1a156299`, in the Makefile's order.

**Observed:** exit `0` throughout.

- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `177 files already formatted`; `typecheck` — `Success: no issues found in 79 source files`.
- `test` — 1338 passed; `harness` — 965 passed.
- `authoring` — `0 finding(s)`.
- `corpus` — `351 fixture(s), 351 pass`.
- `smoke` — the installed command is named on the path, independent of the working directory and of this repository.
- `layout` — `4 tree(s) present`.
- `tables` — `21 command(s) and 8 declaration(s)`.
- `links --online` — `every reference in 212 document(s) resolved`.
- `vocabulary` — `46 contract term(s) ... on 9f58475d`, every one defined in `docs/glossary.md`.
- `invocation` — `30 statement(s)`.
- `conformance` — `305 clause(s)`, `55 covered by no fixture`, `0 declaration(s) naming no clause`.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — `every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections`.

## T11 — Delivery
    110|
**Ran:** `gh api` against the pull requests and the epic base.

**Observed:** #428 merged to `i05/e09/main` at `19665104bf49652cf9a1beab55d6eb52a0314278`, its `Checks` run reported `success` on `1a156299`. #429 merged to the same base at `d0eced6f12ec37aca3d78320095d76224091979d`, its `Checks` run `success` on `3f13ef0e`, and the base's own run `success` at that merge. Both hold a Development link to #414, verified through `closingIssuesReferences`. Row `W01` on #414 links #428 and is ticked done; `AC1`, `AC11` and `AC18` are ticked.

## T12 — The correction #429 landed

**Ran:** `src/tests/test_mock.py::test_a_title_carrying_a_withheld_link_is_headed_by_the_text_it_emits` at `3f13ef0e`, and the full suite.

**Observed:** pass; `src/tests` 1339 passed, `make corpus` 351 pass, and `invocation`, `conformance` and `independence` unchanged. The defect was found after #428 merged, and a fix belongs to the branch whose code it fixes, so it was raised as #429 against the same base rather than left on the branch.

`cli.file_named` read a document's file heading without the mapping, so a title carrying a withheld link whose target only the mapping supplied resolved to nothing there and was compared as a heading it is not. Both the warning and the emission now read the mapping.
