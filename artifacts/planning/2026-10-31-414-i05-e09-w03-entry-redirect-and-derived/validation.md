# Validation — W03 Entry Redirect and Derived Name

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w03-entry-redirect-and-derived` on branch `i05/e09/w03-entry-redirect-and-derived`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as `env PYTHONPATH=<worktree>/src <venv>/pf`, the same form the continuous-integration job supplies.

The venv is the sibling worktree's (`w02-key-and-self-mock/src/.venv`): this worktree's own `uv sync` cannot run in the sandbox, because `uv` fetches `hatchling` to build the package and the sandbox has no network. `PYTHONPATH` names this worktree's `src`, so the build under test is this branch's code — verified by resolving `prosiform.cli.__file__` before the runs below.

The design clause the fixtures declare is `Link classification and resource handling — The substitution mapping`, byte-identical at the pin `827b66fc` W04 moved it to.

## T1 — The two fixtures pass against the build

**Ran:** `make corpus`, at branch head `7a662612`, then again after the rebase at the rebased head.

**Observed:** exit `0`.

```text
mock/a-redirected-entry-derives-its-name-from-the-substitute: pass
mock/a-redirected-referrer-carries-its-entry: pass
corpus check: 360 fixture(s), 360 pass, 0 fail, 0 awaited, 0 unexpected pass
```

The count rose from 358 to 360, which is the two this row lands. Each fixture is a statement about the run's folder, not only its bytes: `compare_bundles` requires that the folder a run creates is named for one of the bundles the manifest declares, so `a-redirected-entry-derives-its-name-from-the-substitute` fails a run that derives `entry.bundles` without ever reading a byte.

## T2 — Both fixtures fail without the redirect

**Ran:** `make corpus` with `PROSIFORM_BUILD` naming a copy of this branch's package at `/tmp/w03probe/src-neg`, made by removing the mapping from `entry` and from the `-f` call in `execute` — two string replacements, nothing else.

**Observed:** exit `1`, and exactly the two new fixtures failed of the 360:

```text
mock/a-redirected-entry-derives-its-name-from-the-substitute: fail
  expected.bundles: the run wrote its bundles into entry.bundles, which names no bundle the manifest declares
  expected.bundles: the run wrote entry.bundle.md, which the manifest declares no bundle for
  expected.bundles: the run wrote no stand-in.bundle.md
  expected.diagnostics: position 1: warning W_MOCK_SUBSTITUTED expected, warning W_MOCK_UNUSED produced
mock/a-redirected-referrer-carries-its-entry: fail
  expected.bundles: the run wrote its bundles into guide__run.bundles, which names no bundle the manifest declares
  expected.bundles: the run wrote guide__run.bundle.md, which the manifest declares no bundle for
  expected.bundles: the run wrote no stand-in__run.bundle.md
corpus check: 360 fixture(s), 358 pass, 2 fail, 0 awaited, 0 unexpected pass
```

That pair is what makes both fixtures statements about the redirect rather than about their trees: the only difference between the pass and the failure is the mapping.

## T3 — The unit cases hold, and fail without the redirect

**Ran:** `src/tests/test_mock.py`, 46 tests at the branch head; then the four new cases against the same `/tmp/w03probe/src-neg` copy.

**Observed:** all 46 pass at the head. Against the redirect-free copy all four new cases fail:

- `test_a_section_entry_derives_the_section_the_substitute_carries` — `status` is `1` where `0` is expected.
- `test_a_document_key_leaves_a_section_entry_its_own_fragment` — `status` is `1`.
- `test_two_entries_naming_one_substitute_derive_one_name` — `stand-in.bundles/stand-in.bundle.md` is absent.
- `test_an_explicit_folder_leaves_the_derived_name_following_the_substitute` — the same bundle is absent under `out`.

The last two assert the folder rather than the bytes for the reason T1 gives, and the first two differ by the section each names: a fragment key replaces the section, and a document key leaves the entry's own fragment in place. Those are separate branches of `Substitution.substitute`, so a case naming only one of them would leave the other unstated.

## T4 — The unmocked runs derive what they derived before

**Ran:** `pf -d json entry.md` and `pf -d json -f guide.md '#run'` in copies of each fixture's `source/` tree, with no `-m`.

**Observed:** exit `0` in both, publishing `entry.bundles/entry.bundle.md` carrying `# Entry … # Rules`, and `guide__run.bundles/guide__run.bundle.md` carrying the guide's own `Run` section. Neither publishes a `stand-in` folder, and neither emits a diagnostic — the unmocked behaviour the mapping must leave alone is the behaviour the trees state, which is why the fixtures' expectations differ from these in both name and bytes.

## T5 — A URL-style check of the derived name under `-o`

**Ran:** `pf -m entry.md=stand-in.md -o hold entry.md` in a probe tree.

**Observed:** exit `0`, writing `hold/stand-in.bundles/stand-in.bundle.md`. `-o` names the folder the run's own folder stands in and says nothing about the name, so the derived name follows the substitute with or without it. This is the half the epic record said a fixture could not state; T1 shows the fixture states it, and the unit case states the `-o` independence a single-invocation fixture cannot.

## T6 — Two entries naming one substitute

**Ran:** `pf -d json -m entry.md=stand-in.md -m other.md=stand-in.md entry.md other.md`.

**Observed:** exit `0`, one `W_MOCK_SUBSTITUTED` per key, and one bundle at `stand-in.bundles/stand-in.bundle.md`. `selections` de-duplicates by `(path, fragment)`, so both entries give one target. The epic record predicted a multi-selection refusal requiring `-o`; the record is corrected in `change-list.md` and the unit case states what the build does.

## T7 — `make conformance` maps the clause

**Ran:** `make conformance` at the branch head, with `README.md` pinned to `827b66fc`.

**Observed:** exit `0`.

```text
Link classification and resource handling — The substitution mapping: 12 fixture(s)
conformance report: 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; 37 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes
```

The mapping clause's fixture count rose from 10 to 12. The clause count and the uncovered count are unchanged, which is what two fixtures taking an existing clause must show. Both manifests declare `W_MOCK_SUBSTITUTED`, which the schema's warning catalogue carries since W04, so no manifest declares a code the corpus cannot state.

## T8 — `make check`

**Ran:** every target of `make check`, in the Makefile's order, at three revisions: `7a662612`, the head before the base moved; the head after W06's merge `846f8f5a` was brought in; and the final head.

**Observed at `7a662612`:** exit `0` throughout.

- `lock-check` — the locked environment resolves; `lint` — `All checks passed`; `format-check` — every file formatted; `typecheck` — no issues.
- `test` — 1354 passed; `harness` — 802 passed.
- `authoring` — `0 finding(s)`.
- `corpus` — `360 fixture(s), 360 pass`.
- `smoke` — the installed command is named on the path.
- `layout` — `4 tree(s) present`; `tables` — `21 command(s) and 8 declaration(s)`.
- `links --online` — every reference resolved.
- `vocabulary` — `46 contract term(s) ... on 827b66fc`.
- `invocation` — `30 statement(s)`.
- `conformance` — the counts T7 gives.
- `independence` — every shaped term of every declaration and report entry is one the contract names.
- `steps` — every procedure in 59 documents writes its steps as sub-sections.

**Observed after the base moved, on the head carrying it:** two targets failed, both in the sandbox and both for one cause.

```text
tests/test_linked_bootstrap.py: error: Failed to build ... cause: Failed to fetch: https://pypi.org/simple/hatchling/ ... dns error
smoke check: the installation does not stand
```

`smoke` and the thirteen `test_linked_bootstrap` cases each run `uv build --wheel`, which resolves `hatchling` from the network. Every other source test passed: `1346 passed` with `--ignore=tests/test_linked_bootstrap.py`. Both are the failures the delivery brief names as sandbox-only.

**Observed at the final head `97a6a9b0`:** exit `0` on every target, including `smoke` and `test_linked_bootstrap`, which pass once the sandbox's network restriction is lifted.

- `test` — 1359 passed; `harness` — 802 passed.
- `corpus` — `363 fixture(s), 363 pass`, the two new fixtures among them.
- `smoke` — `the installed command is named on the path, independent of the working directory, independent of this repository`.
- `conformance` — `305 clause(s)`, `55 covered by no fixture`, `0 declaration(s) naming no clause`.
- `independence`, `invocation`, `vocabulary`, `links --online`, `layout`, `tables`, `steps`, `authoring`, `lint`, `format-check`, `typecheck` — each green.

## T9 — Delivery

**Ran:** `gh api` against the pull request, the epic base and the epic issue; and `sync.py` to record the delivery.

**Observed:** [#438](https://github.com/m2ux/prosiform/pull/438) raised against `i05/e09/main`, titled `[I05:E09] Redirect the Entry and Derive the Name It Publishes`, and linked to #414 by `addCloseIssueReferences`. The link was verified through `closedByPullRequestsReferences`, which listed #438 at `OPEN` beside the earlier rows.

The base moved to `846f8f5a` (W06's merge) between the branch being cut and the pull request being raised. The base was brought into the branch with a merge commit, `97a6a9b0`, rather than by rebasing a branch already pushed, so the pull request's history holds both the delivery commit and the merge. The `Checks` run reported `success` on `97a6a9b0`, and the pull request merged to `i05/e09/main` at `737068cf5cc297e74a6c6d8dfec4e60b72201ffd`.

`sync.py` linked row `W03` to #438, ticked `AC2` and `AC13` as ready to verify, and marked the row done. The updated body was published to #414 and read back: the row links #438 with `✓`, and both criteria carry `[x]`. The epic is not closable, which is expected — W05, W07, W08 and W10 are undelivered.

