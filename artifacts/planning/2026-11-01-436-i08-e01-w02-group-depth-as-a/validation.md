# Validation

The checks [W02](w02.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Branch head | `0d8319fd` on `i08/e01/w02-group-depth-as-a` |
| Epic base | `5a31a7c4` on `i08/e01/main` |
| Design pin | `425037d6` on `engineering` |

## T1 Unit Tests

`uv run --project src --frozen pytest src/tests/test_metadata.py` at `0d8319fd`: every test passes, among them `test_a_declared_group_is_refused_at_its_key` (three spellings, each at the `group` key, naming `prosiform.default.group-depth: [{<group>: <depth>}]`), `test_a_malformed_group_entry_is_refused_at_the_entry` (eight entries, each named `prosiform.default.group-depth[<n>]` at the entry), `test_a_document_joins_several_groups_at_different_depths`, `test_group_and_marks`, `test_group_grammar`, `test_depth_grammar` and `test_integer_depth_schema`.

Result: pass.

## T2 Run Tests

`uv run --project src --frozen pytest src/tests/test_cli.py` at `0d8319fd`: `test_a_document_joining_two_groups_is_emitted_under_each` (the bundle carries the member under `# Modes` at depth one and again under `# Targets` at depth two), `test_a_depth_disagreement_in_one_of_a_documents_groups_refuses` (`E_GROUP_DEPTH_CONFLICT` naming `targets`, the group the members disagree about) and `test_a_group_its_preset_names_twice_holds_the_document_once` pass.

Result: pass.

## T3 Corpus Fixtures

`make corpus` at `0d8319fd` reports `inclusion/a-declared-group-is-refused`, `inclusion/a-document-joins-two-divisions`, `inclusion/a-malformed-group-entry-is-refused` and `inclusion/a-group-entry-keyed-by-a-number-is-refused` as `pass`. Every grouping fixture's expected bundle holds unchanged, so a document in one group emits as it did under the two fields.

Result: pass.

## T4 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `0d8319fd`, exit 0. The unit suite reported 1520 passed and the harness 1129 passed. The corpus reported 404 fixtures, 404 pass, 0 fail, 0 awaited. `make conformance` read 323 clauses with 0 declarations naming no clause; *Conversion metadata — `group` is refused* is cited by 1 fixture, *Conversion metadata — An entry is one string key with an integer value* by 2 and *Presets — A document in several groups* by 1.

Result: pass.

## Findings

- **Candidate coverage counted a region across the whole bundle.** A document in two groups failed as an internal fault; coverage is now held within each group, the rule the design states.
- **The design's usage example declared the retired flat fields.** It is restated as a `default` preset holding a `group-depth` pair, and the README pins that revision.
- **The glossary's *grouping rule* named two paired fields.** It names one `group-depth` entry.
