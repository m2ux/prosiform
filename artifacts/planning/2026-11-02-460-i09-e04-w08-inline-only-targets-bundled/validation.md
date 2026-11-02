# Validation

The checks [W08](w08.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design | README pin `99bec9f7`, *Section composition — Inline-only targets* |
| Branch head | `5c99a472` on `i09/e04/w08-inline-only-targets-bundled`, with `i09/e04/main` merged at `64f85304` (W03) |

## T1 Unit Tests

`src/tests/test_cli.py`:

- **A directive inside a contribution includes its target.** Composition does not yet place such a directive (W05), so the section it names stands in its document's file group, and the section only the outer directive reaches takes none.
- **A placed document widens.** When such a directive names a section of a document already read, the section joins that document's selection and its links are read: the far document it links is bundled.

`src/tests/test_candidate.py` passes the diagnostic chains to assembly.

Result: pass.

## T2 Composition Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-target-only-directives-reach-takes-no-group` | The read and write documents, reached only by directives, take no file group. The write document's `group` pair places no merged group. The read document's unreached Outputs is carried nowhere. | AC17 |
| `an-inclusion-of-another-section-keeps-only-that-section` | An ordinary link to Outputs gives the read document a group carrying Outputs alone, while Inputs stands only in its contribution. | AC17 |
| `an-inclusion-of-the-composed-section-keeps-its-group` | An ordinary link to the composed section, and one to a composed document whole, each keep that document's group beside the contributions. | AC17 |
| `a-link-inside-a-contribution-includes-its-target` | Links a contribution carries include their targets, placed where the contribution stands. | AC17 |
| `a-dispatch-in-an-inline-only-contribution-takes-its-own-sub-section` | A dispatch inside an inline-only contribution takes a sub-section one level below the contribution. The scope's own dispatch sub-section still follows the destination sections. | AC17 |

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `5c99a472`:

- Unit tests: 1655 passed. The harness ran 1193.
- Corpus: 463 fixtures, all pass.
- Conformance: 356 clauses read, and no declaration names a missing clause.

Result: pass.
