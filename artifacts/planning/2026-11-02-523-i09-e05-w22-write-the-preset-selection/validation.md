# W22-W24 Validation

The three feature workflows and the harness that reads their bundles, at branch `i09/e05/w22-write-the-preset-selection`.

## How the bundle states the path

`make harness` compiles each workflow's `diagram/` form with the `pf` the locked environment installs and walks the entry bundle as a session given it does. The bundle's own diagram names each edge; each state is entered at the heading the previous section's link names, or else the one the bundle's diagram clicks; its action and transition are read from that heading's text. `test_each_scenario_path_is_the_walk_its_bundle_states` holds every scenario of every diagram-drawing workflow to that walk, the three earlier ones among them, beside the source walk `test_each_scenario_path_is_the_walk_its_inputs_determine` already held. A bundled action differing from the source's is a fault, since the scorer reads the source's.

Two broken copies show the bundle, not the source, is what is held: `test_a_substitute_stating_another_branch_is_a_fault` swaps the branch the handbook's `Inspect` section takes, which leaves the source walk whole and fails the bundle walk; `test_a_substitute_stating_another_action_is_a_fault` changes the selected `Gate` substitute's action.

`subst` warns wherever a pair is used, so a `scenarios.toml` declares `warnings`, and a bundle is held to raising those and no other diagnostic (`test_a_warning_the_workflow_does_not_declare_is_a_fault`, `test_a_declared_warning_the_bundle_does_not_raise_is_a_fault`). The runner refuses a bundle reporting any other diagnostic.

## AC23

`preset-selection`: `Receive` and `Assess` decide the branch; each branch's state links an unclicked state document under a title selecting its presets.

| Scenario | Path | Permutation | Bundle |
| --- | --- | --- | --- |
| `default-alone` | Receive, Edit, Proof, Merge | `Edit` selects nothing of `proof.md`; its `default` pair places Proof. | `# Edit` > `## Proofs` > `### Proof` |
| `title-selected` | Receive, Assess, Patch, Verify, Merge | The title `Patch` selects `verify.md`'s `patch` preset, whose pair places Verify. | `# Patch` > `## Checks` > `### Verify` |
| `two-presets-one-title` | Receive, Assess, Harden, Audit, Merge | `Security Review` selects `audit.md`'s `security` and `review` presets; their settings union. | `# Harden` > `## Audits` > `### Audit`, its policy link redirected to `Strict Policy` |

`test_the_title_linking_a_document_selects_the_presets_placing_it` asserts each arrangement.

## AC24

`group-placement`: `Scope` and `Stage` decide the branch.

| Scenario | Path | Permutation | Bundle |
| --- | --- | --- | --- |
| `leaf-group` | Scope, Lint, Unit, Release | `lint.md` and `unit.md` link nothing and declare one pair. | `# Delivery` > `## Checks` > `### Lint`, `### Unit` |
| `nested-intermediate` | Scope, Stage, Compile, Package, Sign, Release | `package.md`, which `Compile` links, links `sign.md`; each places its own section. | `# Compile` > `## Packaging` > `### Package`, then `### Signing` > `#### Sign` inside it |
| `two-presets-one-document` | Scope, Stage, Announce, Notify, Release | `notify.md` is reached from the diagram under `default` and from `Announce` under `announce`. | Notify under `## Messages` and again under `## Announcements` |

`test_group_pairs_place_each_file_from_the_leaves_up` asserts each arrangement. Where the second group stands is the build's departure recorded under [Arising](#arising): it asserts only that Notify stands in both groups.

## AC25

`subst-redirect`: `Outline` and `Inspect` decide the branch. The entry is titled `Release`.

| Scenario | Path | Permutation | Bundle |
| --- | --- | --- | --- |
| `document-redirect` | Outline, Approve | The entry's `default` maps `states/approve.md` to `alternates/approve.md`, redirecting the diagram's click. | `# Approve` carries the substitute's text |
| `section-redirect` | Outline, Amend, Inspect, Approve | `amend.md`'s `default` maps `inspect.md#inspect` to `../alternates/handbook.md#inspect`. | `# Handbook` > `### Inspect`; the handbook's unselected `Archive` is absent |
| `preset-over-default` | Outline, Amend, Inspect, Stage, Gate, Approve | The entry's title selects `stage.md`'s `release` preset, whose `gate.md` pair holds over `default`'s. | `# Gate` carries `alternates/release-gate.md`'s text |

`test_subst_pairs_redirect_the_links_a_document_writes` asserts each, and that no original's text reaches the bundle.

## What each default cell proves

The workflows are written in the diagram form alone, so the default matrix gives each scenario a `bundle` and a `tree` cell, on each model, and on each harness. No scenario carries a `↳` line or asks for a `pf` run, so a harness with no shell follows every cell.

- **`bundle`.** The session follows the bundle `pf` compiled with the feature: states nested in groups, a section placed twice, links redirected to substitutes. A pass shows the agent follows the arrangement the feature produced.
- **`tree`.** The session reads the sources, which no run compiled, so the feature changes nothing it reads. Each substitute states the action and transition of the state it stands in for, so the path is the same, and the cell is the comparison: what bundling adds. It proves nothing about the feature.

## Default matrix

Eighteen scenarios of ten workflows, 46 cells, 460 sessions at five repetitions; at the 60 000-token session cap they need 27 600 000 tokens, and `EVAL_BUDGET_TOKENS` is 28 000 000. `baseline.json` is unchanged.

## make check

`PROSIFORM_BUILD='uv run --project …/w22-write-the-preset-selection/src --frozen pf' make check` exits 0 at a6c37a40: 1663 build tests and 1217 harness tests pass, every corpus fixture passes, and `conformance` reports 0 declarations naming no clause, 0 declared codes the build reports nowhere and 0 reported codes the contract declares nowhere.

## Arising

A document reached under two presets stands in each group, as the design states, but the second group stands in the division of the document whose reference placed the document first, not of the one whose reference placed that group's first member, as *Grouping — Nested groups* states. Recorded as [#592](https://github.com/m2ux/prosiform/issues/592), since the build is outside this unit's change.
