# Validation — W07 Substitute as a Full Source

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i05/e09/w07-substitute-as-a-full` on branch `i05/e09/w07-substitute-as-a-full`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as the worktree's own `src/.venv/bin/pf`, the same form the continuous-integration job supplies, because `uv run` cannot build the wheel without network in the sandboxed shell this session ran in.

The design clause every mock fixture declares is `Link classification and resource handling — The substitution mapping`; `README.md` pins `827b66fc`, which this session did not move.

The branch head is `4c641293`, rebased onto `846f8f5a` — the merge of #437, W06 — before it was pushed. The 363-fixture counts below are that head's.

    10|
## T1 — Both fixtures pass against the build

**Ran:** `checks/corpus.py` at branch head `4c641293`, 363 fixtures.

**Observed:** exit `0`.

```text
mock/a-substitute-declaring-a-group-joins-it: pass
mock/a-substitute-root-bounds-its-own-links: pass
corpus check: 363 fixture(s), 363 pass, 0 fail, 0 awaited, 0 unexpected pass
```

AC5 and AC6 each have the fixture the epic names. The count rose from 361 to 363, which is the two this row lands. The base carried 361 rather than the 360 this worktree showed before the rebase, because W06's three fixtures and W03's two merged while this row was built.

## T2 — Each fixture is a statement about the substitution, not about its tree

**Ran:** `pf guide.md` in `a-substitute-declaring-a-group-joins-it/source` with no mapping, and `pf -m rules.md=stand-in/entry.md guide.md` over a copy of `a-substitute-root-bounds-its-own-links/source` with the substitute's `prosiform.root` declaration deleted.

**Observed:** exit `0` in both, and each produced the opposite of what the fixture declares.
    20|
Without `-m`, the AC5 tree does not merge at all — `rules.md` keeps its own file group, so the bundle is `# Rules … # Rules / Every rule the tree under test holds.` and no `### Stand In` exists. The merged group therefore exists only because the substitute declares one.

With the substitute's root removed, the AC6 tree compiles the link above it:

```text
# Entry

Detail [beside it](#detail) and [above the stand-in root](#outside).

# Outside

Material above the stand-in's declared root.
```

The fixture expects `[above the stand-in root](../outside.md)` — the citation its author wrote — so the citation is the substitute's own root at work and not the shape of the tree. A manifest declares one invocation and cannot state either counterfactual, so both are recorded here and in the pull request body rather than in the fixtures.

## T3 — The substitute's membership, its own failures and one capture

**Ran:** `pytest tests/test_mock.py` at `4c641293`.

**Observed:** 56 passed. The cases that decide this row:

- `test_a_substitute_declaring_a_group_joins_it_under_its_own_member_heading` — the bundle opens on `# Rules`, carries `### Stand In`, and the authored `rules.md` contributes nothing.
- `test_a_substitute_declaring_no_group_joins_no_group` — a substitute carrying no declaration keeps its own file heading, so no setting travels from the key's target.
    30|- `test_the_group_a_substitute_declares_is_the_one_the_bundle_merges` — an authored target declaring group `authored` contributes no `# Authored` heading to the bundle.
- `test_a_group_depth_conflict_names_the_substitutes_own_declaration` — `E_GROUP_DEPTH_CONFLICT`, exit `1`, with `stand-in.md` named as the related declaration at its own line and column.
- `test_a_substitutes_metadata_failure_names_the_substitute` — `E_INVALID_CONVERSION_METADATA` located on `stand-in.md`, on the chain `["guide.md", "stand-in.md"]`.
- `test_a_substitute_reached_by_two_routes_joins_the_group_once` — one overview subsection and one variant heading name the one member, and its preamble and scope each appear once however many links reach it.

The first version of the two-route case asserted one `### Stand In` and failed at two: a group with a pooled section names a member in the overview **and** in each variant the member contributes to. That is the arrangement's behaviour rather than a second membership, so the assertion now counts the naming and holds the content to one occurrence, which is what a second capture would duplicate.

## T4 — The substitute's root bounds its own links

**Ran:** `test_a_substitutes_root_bounds_its_own_outgoing_links` and `test_the_substitutes_root_is_read_from_its_own_bytes` at `4c641293`.

**Observed:** both pass. The first holds that `detail.md` beside the substitute compiles and `../outside.md` does not. The second gives the authored target `root: ..` — a root that *would* reach the same link — and the substitute's own `.` still emits it as a citation, which is the direction that fails if a setting ever travels from the original.

## T5 — A parent-segment substitute reads its own settings

**Ran:** `test_a_substitute_above_the_working_directory_reads_its_own_settings` at `4c641293`.

    40|**Observed:** pass. With the working directory at `tree/`, `-m rules.md=../above/entry.md` reads a substitute one directory above it. The substitute's `group: rules` merges it into the group the guide declares, its `root: .` resolves from `above/` rather than from `tree/`, so `detail.md` beside it compiles, and `../tree/guide.md` above that root stays the link its author wrote.

This is AC20 stated against the capability `fixtures/mock/a-substitute-outside-the-writing-root-is-reachable` already shows, as the brief directs: no third fixture was added. The unit case is where the row can say it, because the epics' `fixtures.md` records AC20 as that fixture's claim.

## T6 — Conformance maps every declared clause

**Ran:** `checks/conformance.py` at `4c641293`, with `README.md` pinned to `827b66fc`.

**Observed:** exit `0`.

```text
Grouping — Group membership: 5 fixture(s)
Conversion metadata — Source ownership: 1 fixture(s)
Link classification and resource handling — The substitution mapping: 15 fixture(s)
Link classification and resource handling — Local Markdown links resolving outside the root: 10 fixture(s)
Exit status and JSON diagnostics — 0: 24 fixture(s)
conformance report: 305 clause(s) the design states, 54 covered by no fixture, 0 declaration(s) naming no clause; 37 declared name(s) reached, 0 unfixturable, 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere, 16 clause(s) no run states, 3 section(s) stating no behaviour, 3 installation claim(s) no run observes
```

The clause count and the uncovered count are unchanged, which is what a row that adds fixtures and states no new clause must show.

The AC6 manifest's first draft declared `Reference normalization and path identity — Bounded bootstrap capture`, and conformance refused it: `Bounded bootstrap capture` is a heading, and the rules beneath it are table rows and bullets, so the heading alone names a clause the design does not state as one. The row now declares `Link classification and resource handling — Local Markdown links resolving outside the root`, which is the rule the fixture takes — a reference outside its author's root is emitted as authored and never opened — beside `Conversion metadata — Source ownership` for whose settings decide the root.

## T7 — `make check` on the branch head

**Ran:** every target of `make check` at `4c641293`, in the Makefile's order.

**Observed:** green throughout.
    60|
- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `177 files already formatted`; `typecheck` — `Success: no issues found in 79 source files`.
- `test` — 1351 passed; `harness` — 987 passed.
- `authoring` — `0 finding(s)`.
- `corpus` — `363 fixture(s), 363 pass`.
- `smoke` — the installed command is named on the path, independent of the working directory and of this repository.
- `layout` — `4 tree(s) present`.
- `tables` — `21 command(s) and 8 declaration(s)`.
- `links --online` — `every reference in 212 document(s) resolved, except 18 whose host did not answer`.
- `vocabulary` — `46 contract term(s) ... on 827b66fc`, every one defined in `docs/glossary.md`.
- `invocation` — `30 statement(s)`.
- `conformance` — the counts in T6.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `steps` — every procedure in 59 documents under example/work-planner/ writes its steps as sub-sections.

`tests/test_linked_bootstrap.py`'s 13 tests were deselected, because the module runs `uv build --wheel` and needs network the delivery sandbox denies. They pass unchanged in the predecessor worktree at the same base under the same conditions, so they are not this row's change; continuous integration runs them unsandboxed.

## T8 — A formatting defect the first push carried, and its correction

**Ran:** the `Checks` workflow on the first pushed head `9a2c6525`, then the same target locally after the correction.

**Observed:** `failure` at `format-check`:

```text
unformatted: File would be reformatted
   --> src/tests/test_mock.py:590:1
177 files already formatted
1 file would be reformatted
make: *** [Makefile:91: format-check] Error 1
```

The rebase onto `846f8f5a` conflicted in `src/tests/test_mock.py` — W06's section-key cases landed at the same end of the file this row appends to — and the conflict markers were removed with a line filter that left three blank lines where the two regions met. `ruff format` joins them to two. The file was reformatted, both commits were rebuilt on the same base so the branch records two substantive commits rather than three, and the branch was force-updated with `--force-with-lease`; no other contributor holds it.

The local `format-check` this session ran before the first push reported `177 files already formatted` — the count is the same before and after, which is why the defect passed locally and failed in CI. The local run and the CI run used the same `ruff` from the same lockfile, so the difference is the working tree: the local check ran before the rebase's resolution was committed and the CI check ran on the committed bytes. The lesson is that `format-check` must run after the last commit, which T7's re-run does.

    90|
## T9 — Delivery

**Ran:** `gh api` against the pull request, the epic base and the epic issue, and `gh api graphql` for the Development link.

**Observed:** [#439](https://github.com/m2ux/prosiform/pull/439) opened against `i05/e09/main` at `846f8f5a`, titled `[I05:E09] Substitute as a Full Source`, labelled `bot:ai-assisted`, and holding a Development link to #414 verified through `closedByPullRequestsReferences`, which lists `439`.
