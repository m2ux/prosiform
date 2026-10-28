# I05:E03:W08 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w08-prosiform-section-and-its`, cut from `i05/e03/main` at `f2d558a37f6999853b3e8335dd22bcd1a1e015c0`.
- **Tested revision.** `40de3544` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `429eaf810c6c985c3efde016cf0dcea8bd3eeb2f` on `engineering`, whose profile clause names `skill-markdown-v4`, whose The Prosiform section clause states the section and both protocols, and whose Dispatch sub-sections and Parallel dispatch sub-sections clauses state the protocol links.

## T1 Prosiform section (unit)

| Test | Observes |
| --- | --- |
| `test_bundle.py::test_a_bundle_using_the_dispatch_operator_opens_with_its_protocol` | AC16: `# Prosiform` and `## Dispatch` only, then `# Guide`; the sub-section line ends "as [Dispatch](#dispatch) states."; the dispatched `plan.bundle.md` carries no Prosiform section. |
| `test_bundle.py::test_a_bundle_using_the_parallel_mark_states_both_protocols` | AC16: a `⫽`-only bundle carries `## Dispatch` and `## Parallel dispatch`; the set's instruction links `#parallel-dispatch`. |
| `test_bundle.py::test_a_bundle_using_both_operators_states_each_protocol_once` | AC16: one Prosiform section, each protocol once, though the operators sit in two sections. |
| `test_bundle.py::test_a_bundle_using_neither_operator_carries_no_prosiform_section` | AC16: the bundle opens on `# Guide`, byte for byte the bundle it was. |
| `test_bundle.py::test_the_prosiform_section_precedes_a_file_heading` | Placement: a section entry's bundle opens `# Prosiform` ahead of the `# Guide` file heading. |
| `test_bundle.py::test_the_prosiform_section_follows_a_preamble_and_precedes_its_dispatch` | Placement: preamble, Prosiform section, the preamble's `# Dispatch plan`, then `# Guide`. |
| `test_bundle.py::test_the_prosiform_section_precedes_a_titled_entry_members_title` | Placement: a titled entry member of a merged group opens with its preamble, the section, then its `# Guide` title. |
| `test_bundle.py::test_an_authored_heading_equal_to_a_protocol_pf_emits_is_refused` (3 cases) | `## Dispatch` beside `⇉` or `⫽`, and `## Parallel dispatch` beside `⫽`, exit 1 with `E_HEADING_COLLISION` and no bundle. |
| `test_bundle.py::test_an_authored_protocol_heading_pf_does_not_emit_publishes` (2 cases) | `## Dispatch` in a bundle that dispatches nothing, and `## Parallel dispatch` beside `⇉` only, publish. |
| `test_candidate.py::test_an_instruction_linking_its_protocol_holds`, `test_an_instruction_linking_no_protocol_of_the_prosiform_section_is_invalid` (2 cases) | Candidate validation holds an instruction's link to a Prosiform protocol heading: `#dispatch` holds; `#guide` and `#nowhere` are `target integrity` failures. |
| `test_cli.py` dispatch and parallel sub-section tests | Each expected bundle opens with the Prosiform section and each sub-section line links its protocol. |

## T2 Byte-identical protocols (two corpora)

AC17: `test_bundle.py::test_each_protocol_is_the_same_bytes_in_two_corpora` compiles a nested `skill/` corpus (dispatch and set in one section, a dispatched bundle carrying a set) and a second corpus whose entry dispatches in parallel from its preamble and dispatches from an H3. The `## Dispatch` and `## Parallel dispatch` sub-sections of `skill_guide.bundle.md`, `skill_plan.bundle.md` and `mode.bundle.md` are the same bytes.

## T3 Operator combinations (end to end)

AC16: the `fixtures/prosiform` family.

| Fixture | Observes |
| --- | --- |
| `a-bundle-using-the-dispatch-operator-states-its-protocol` | `# Prosiform`, `## Dispatch`, then `# Guide`; `plan.bundle.md` carries none. |
| `a-bundle-using-the-parallel-mark-states-both-protocols` | `## Dispatch` and `## Parallel dispatch`; the set's line links `#parallel-dispatch`. |
| `a-bundle-using-both-operators-states-each-protocol-once` | One section, each protocol once. |
| `a-bundle-using-neither-operator-carries-no-prosiform-section` | The bundle opens on `# Guide`. |
| `the-section-follows-a-preamble`, `the-section-precedes-a-file-heading` | Placement after a preamble and ahead of a file heading. |
| `a-heading-equal-to-the-dispatch-protocol-is-refused`, `a-heading-equal-to-the-parallel-dispatch-protocol-is-refused` | Exit 1, `E_HEADING_COLLISION`. |

The 21 existing dispatching fixtures (`dispatch`, `run-set`, one `frontmatter` and three `usage-example`) take the section and the protocol link; their diff removes only the instruction lines the link rewrites.

## T4 Informational version

AC18: `cli/informational-version-response` and `cli/informational-long-version-response` expect `(skill-markdown-v4)` and pass; `checks/smoke.py` reports `pf 0.15.0 (skill-markdown-v4)` from the installed wheel.

## T5 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1275 unit tests, 713 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary, invocation, conformance and independence.

## T6 make corpus

`corpus check: 330 fixture(s), 330 pass, 0 fail, 0 awaited, 0 unexpected pass`. Every bundle using no operator reproduces unchanged.

## T7 make conformance and make invocation

- `make conformance`: 302 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere; The Prosiform section is covered by 6 fixtures, the Prosiform section adversarial family by 8.
- `make invocation`: 28 statements of `invocation.md`, each held to the build's help.
- `make vocabulary`: 43 contract terms, `Prosiform section` among them, each defined in the glossary.
