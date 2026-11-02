# Validation

The checks [W02](w02.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`ee8df501`](https://github.com/m2ux/prosiform/blob/ee8df5019eae28c538ba327c78fdfd10d5ad08e0/artifacts/planning/2026-10-17-prosiform-v1/design.md#section-composition), which adds the visible-scalar rule to *Recognition* |
| README pin | `99bec9f7`, unchanged: see the [change list](change-list.md#held) |
| Branch head | `243793e5` on `i09/e04/w02-sections-composed-into-their`, cut from `i09/e04/main` at `4f13b24d` |

## T1 Unit Tests

- **Recognition.** `src/tests/test_composition.py` reads a no-break space (written and as `&nbsp;`), an ideographic space, a next-line control, a zero-width space, a soft hyphen and a byte order mark as no directive. The no-break space case moved here from the directive cases.
- **Candidate validation.** `src/tests/test_candidate.py` builds a candidate in which two sibling steps compose one section. It validates, and carries the section's body three times: twice composed and once in its own group. Pointing the directives at another heading fails *target integrity*. Changing a composed body fails *preservation*.

Result: pass.

## T2 Composition Fixtures

Each success fixture also links its target documents whole, so each target keeps its own file group as *Inline-only targets* says.

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `titles-from-several-sources-share-one-destination-section` | `read.md#inputs` and `write.md#inputs` share one `Inputs` destination, with `Read` and `Write` contributions. `Outputs` gets its own destination after it. | AC3 |
| `sibling-steps-each-carry-their-own-destination-section` | Two sibling steps each carry their own `Inputs` destination section. | AC3 |
| `a-multi-paragraph-body-is-carried-whole` | Three paragraphs are carried byte for byte, including a soft line break and a hard break. | AC4 |
| `nested-headings-keep-their-relative-depth` | The target's H3 and H4 are emitted at H5 and H6, under an H4 contribution. | AC4 |
| `a-list-is-carried-as-written` | Nested items, a continuation paragraph and an ordered list are carried as written. | AC4 |
| `a-table-is-carried-as-written` | The alignment row and the cell padding are carried as written. | AC4 |
| `a-target-with-no-parent-heading-is-refused` | The run is refused with `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`. | (W04's AC8, folded) |
| `invisible-scalar-labels-are-ordinary-links` | `[ ]`, `[&nbsp;]`, a zero-width space and `[&#xAD;]` are bundled as ordinary links. | AC1 (debt) |

Every directive's link points at its contribution heading. All pass.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0. Results:

- Unit tests: 1653 passed. The harness ran 1183.
- Corpus: 453 fixtures, all pass.
- Conformance: 356 clauses read, and no declaration names a missing clause.

Result: pass.
