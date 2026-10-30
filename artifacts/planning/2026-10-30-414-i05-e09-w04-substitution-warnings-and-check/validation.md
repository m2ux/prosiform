# Validation — W04 Substitution Warnings and Check Mode

> Evidence record · Created 2026-10-30

Every check below ran in the worktree `.worktrees/i05/e09/w04-substitution-warnings-and-check` on branch `i05/e09/w04-substitution-warnings-and-check`, at the revision each section names. The build under test was named by `PROSIFORM_BUILD` as `env PYTHONPATH=<worktree>/src <venv>/pf`, the same form the continuous-integration job supplies, because `uv run` cannot build the wheel without network in the sandboxed shell this session ran in.

The design clause every mock fixture declares is `Link classification and resource handling — The substitution mapping`; the revision carrying the two warning sentences is `827b66fc`, which `README.md` now pins.

## T1 — Both codes are rejected by the schema before the change, and accepted after

**Ran:** a probe through `jsonschema.Draft202012Validator` against each revision's `fixtures/manifest.schema.json`, with a manifest declaring the code at warning severity.

**Observed:** before, at `164a5200`, neither code is in the catalogue and a manifest declaring either is refused:

```text
W_MOCK_SUBSTITUTED: in catalogue = False; manifest rejected -> expected.diagnostics.0.code: 'W_MOCK_SUBSTITUTED' is not one of ['W_COINCIDENT_HEADING', 'W_DISPATCH_DEPTH', 'W_DISPATCH_SELF', 'W_EARLIER_SET_RETAINED', 'W_RESOURCE_PORTABILITY']
W_MOCK_UNUSED: in catalogue = False; manifest rejected -> expected.diagnostics.0.code: 'W_MOCK_UNUSED' is not one of [...]
```

After the change:

```text
W_MOCK_SUBSTITUTED: in catalogue = True; manifest accepted
W_MOCK_UNUSED: in catalogue = True; manifest accepted
```

The build's own `-C` before the change listed five warning codes and neither of these; it now lists seven. This is the folded work W00 recorded: the code the design declares is the code the schema's catalogue repeats, and without both a fixture declaring either fails validation before the run starts.

## T2 — The three fixtures fail against the code before the change

**Ran:** `checks/corpus.py` at branch head `12803a9e`, then the same corpus with `b91e45ff`'s `cli.py` and `closure.py` installed into the build.

**Observed:** `358 fixture(s), 358 pass` with the change; `358 fixture(s), 351 pass, 7 fail` without it. The three this row lands each fail on the diagnostic they declare:

```text
mock/a-substitution-warns-with-its-target: fail
  expected.diagnostics: the run emits 0 diagnostics where 1 diagnostic is expected
    position 1: warning W_MOCK_SUBSTITUTED expected, the run emits none
mock/an-unused-key-warns-and-publishes: fail
  expected.diagnostics: the run emits 0 diagnostics where 1 diagnostic is expected
    position 1: warning W_MOCK_UNUSED expected, the run emits none
mock/a-mocked-check-publishes-nothing: fail
  expected.diagnostics: the run emits 0 diagnostics where 1 diagnostic is expected
    position 1: warning W_MOCK_SUBSTITUTED expected, the run emits none
```

The other four failures are W01's manifests, which declare the warning this row emits. Each fixture therefore holds the change rather than the tree.

## T3 — One key serving two references states one substitution

**Ran:** `fixtures/mock/a-substitution-warns-with-its-target` through `-d json`, and `test_one_key_serving_two_references_records_one_substitution`, `test_a_substitution_names_the_first_link_that_redirected_it` and `test_a_stage_that_resolves_a_link_again_records_no_second_substitution`.

**Observed:** `guide.md` links `rules.md` whole and again by section; the run emits exactly one warning, carrying the whole-document link's position:

```text
{"severity": "warning", "message": "the reference 'rules.md' is redirected to the substitute 'stand-in.md', where it would have resolved to 'rules.md'", "code": "W_MOCK_SUBSTITUTED", "resolved": "stand-in.md", "source": "rules.md", "location": {"file": "guide.md", "line": 3, "column": 1}}
```

The record is keyed by the served key, so the second reference adds no second warning. The first cut keyed it by the substitute's identity, which emitted two warnings for this tree — `mock/a-substitution-warns-with-its-target` failed on the count — and the record moved onto the key. Emission and candidate validation re-resolve the same link and record the same key with no origin, so the discovery record keeps its position; a record re-reached with no position does not overwrite one that has a position.

## T4 — Both warnings' fields, and an empty mapping raises neither

**Ran:** `src/tests/test_mock.py`, and the fixtures through `-d json`.

**Observed:** `W_MOCK_SUBSTITUTED` carries `location`, `source` and `resolved`; `W_MOCK_UNUSED` carries `source` and no `location`, with the key's authored spelling — `./docs/rules.md`, not the `docs/rules.md` it normalizes to, which `test_a_key_no_reference_named_is_unserved_and_keeps_its_authored_spelling` holds. `test_a_run_given_no_mapping_states_neither_warning` and `test_an_empty_mapping_records_neither_a_substitution_nor_an_unused_key` hold that a run given no `-m` emits nothing.

`test_a_substitution_warning_states_the_identity_the_reference_would_have_named` holds the message: two keys naming one stand-in are told apart only by the identity each replaces, so a message stating the substitute alone would leave a reader unable to tell which link moved.

## T5 — `-c` reports the substitution and publishes nothing

**Ran:** `fixtures/mock/a-mocked-check-publishes-nothing`, and `test_a_check_run_reports_the_substitution_and_publishes_nothing`.

**Observed:** exit `0`, the same `W_MOCK_SUBSTITUTED` a publishing run emits, and no run folder written. `publication` emits the run's notices after the bundle checks and beside each bundle's warnings, and publication is the only stage `-c` skips, so the mapping is reported in both modes by construction rather than by a second branch.

## T6 — A fixture can now declare a diagnostic's `location`

**Ran:** `checks/tests/test_manifest_schema.py`, 5 new cases.

**Observed:** pass. The corpus compared a diagnostic on four fields — `reference`, `resolved`, `source`, `chain` — and no manifest could state where a link stands, so AC7's "naming the link's location" was unstatementable. The schema gains a `coordinate` shape (`file`, `line`, `column`) and `checks/runner.py` compares it. A coordinate missing a field, carrying a zero, naming a parent segment or adding a field is refused, which the parametrized case holds.

## T7 — The corpus, with W02 merged alongside

**Ran:** `make corpus` at branch head `12803a9e`, rebased onto `b91e45ff` — the merge of #431, W02.

**Observed:** exit `0`, `358 fixture(s), 358 pass, 0 fail, 0 awaited, 0 unexpected pass`. Ten mock fixtures: this row's three, W01's four and W02's three. The base had moved before this row merged, so the branch was rebased onto `origin/i05/e09/main` first; `src/prosiform/cli.py` conflicted in `substitution` and the resolution keeps both changes — W02's three refusals as the shape check, and this row's `spelled` map feeding `Substitution(keys, spelled)`.

## T8 — `make conformance` holds the design and the schema to one set of codes

**Ran:** `make conformance` at `12803a9e`, with `README.md` pinned to `827b66fc`.

**Observed:** exit `0`:

```text
warning W_MOCK_SUBSTITUTED: 6 fixture(s), the build reports it
warning W_MOCK_UNUSED: 1 fixture(s), the build reports it
CLI contract — -m ORIGINAL=ALTERNATIVE: 7 fixture(s)
Link classification and resource handling — The substitution mapping: 10 fixture(s)
Exit status and JSON diagnostics — 0: 19 fixture(s)
conformance report: 305 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause; ... 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere
```

Both directions are green. The clause count is unchanged at 305, which is what a sentence added to an existing section must show: the design's exit-status section states these as paragraphs, and `checks/conformance.py` makes a clause of bullets, numbered steps and table rows only, so a paragraph adds a code and no clause. The first fixture drafts named `Exit status and JSON diagnostics — W_MOCK_SUBSTITUTED` as a clause and conformance refused both, naming each as a declaration naming no clause; the fixtures now declare `Exit status and JSON diagnostics — 0`, as the existing `W_EARLIER_SET_RETAINED` fixture does.

## T9 — `make invocation`, `make independence`, `make vocabulary`

**Ran:** each target at `12803a9e`.

**Observed:** exit `0` throughout.

- `invocation` — `30 statement(s)`, unchanged: this row adds warnings rather than grammar.
- `independence` — `every shaped term of every fixture declaration and every report entry is one the contract names`.
- `vocabulary` — `46 contract term(s) ... on 827b66fc`, every one defined in `docs/glossary.md`. No new contract term is marked, so no glossary row is needed.

## T10 — `make check`

**Ran:** every target of `make check` on branch head `12803a9e`.

**Observed:** exit `0` throughout.

- `lock-check` — `Resolved 24 packages`.
- `lint` — `All checks passed`; `format-check` — `71 files already formatted`; `typecheck` — `Success: no issues found in 70 source files`.
- `test` — 1337 passed, and the 13 in `test_linked_bootstrap.py` pass when `uv` resolves from its cache.
- `harness` — 799 passed, 1 skipped.
- `authoring` — `0 finding(s)`; `corpus` — `358 fixture(s), 358 pass`.
- `layout` — `4 tree(s) present`; `tables` — `21 command(s) and 8 declaration(s)`; `steps` — every procedure in 59 documents writes its steps as sub-sections.
- `links --online` — `every reference in 212 document(s) resolved`, except 18 whose host did not answer.
- `vocabulary`, `invocation`, `conformance`, `independence` — the counts above.

**Two local limitations, neither a change.** `tests/test_linked_bootstrap.py` runs `uv build --wheel` and `evals/diagram-following` writes a temporary directory beside its output path; both need the network and an unrestricted `/tmp`, which this session's sandboxed shell denies. Both fail identically on the predecessor worktree at `7806ec28` with the same base, so neither is this row's change; `test_linked_bootstrap.py` passes its 13 tests once `uv` resolves from cache (`UV_OFFLINE=1`), and the diagram eval's 62 failures reproduce unchanged there. Continuous integration runs `make check` unsandboxed, so the branch head's `Checks` run is the authority for both.

## T11 — Delivery

**Ran:** `gh api` against the pull request, the epic base and the epic issue.

**Observed:** [#433](https://github.com/m2ux/prosiform/pull/433) merged to `i05/e09/main` at `8734a799beb24544efb91dbe72b0e652afcd48ea`, its `Checks` run reported `success` on `12803a9e` before the merge. It holds a Development link to #414, verified through `closingIssuesReferences`. Row `W04` on #414 links #433 and is ticked done; `AC7`, `AC8` and `AC19` are ticked.

The base had moved while this row was built — W02 merged at `b91e45ff` — so the branch was rebased onto `origin/i05/e09/main` before merging, and the two units' changes to `cli.substitution` were resolved as described in T7.
