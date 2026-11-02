# Validation

The checks [W03](w03.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `99bec9f7`, whose *Section composition* states *The source of composed content* and *Every occurrence composes* |
| Branch head | `4378945d` on `i09/e04/w03-contributions-keeping-their-source`, cut from `i09/e04/main` at `f74a70d5` |

## T1 Source-Relative Fixtures

Each success fixture also links its target documents whole, so each target keeps its own file group as *Inline-only targets* says.

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-contribution-resolves-links-from-its-source-directory` | The guide and `steps/read.md` each sit beside a `notes.md` and each carry `Outputs`. The contribution's `notes.md` points at the notes beside `steps/read.md`, its `../docs/spec.md` at the spec, and its `#outputs` at `Read`'s `Outputs`, not the guide's. The guide's own `notes.md` points at the guide's notes. | AC5 |
| `colliding-definitions-resolve-against-their-own-source` | The guide and `read.md` each define `spec`, naming different documents. The contribution's full and shortcut uses point at `read.md`'s target and the guide's at its own. A definition inside the composed section is carried by neither copy. | AC5 |
| `a-diagnostic-inside-a-contribution-names-its-source` | The composed section links `notes.md#root-only`, a heading only the guide's notes carry. The run fails with `E_TARGET_NOT_FOUND` at `steps/read.md:8`, resolved to `steps/notes.md`, and publishes nothing. | AC5 |

Result: pass.

## T2 Every-Occurrence Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-repeated-directive-contributes-each-time` | One step writes the same directive inline and by reference: its `Inputs` destination section carries two `Read` contributions. A later step writes it again and carries its own. Each link points at the contribution it placed. | AC6 |
| `ordinary-and-composing-links-to-one-section-each-keep-their-meaning` | One paragraph links `read.md#inputs` ordinarily, composes it, then links it ordinarily again. The directive points at its contribution. Both ordinary links point at the section in `Read`'s own file group. | AC6 |

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `4378945d`. Results:

- Unit tests: 1653 passed. The harness ran 1188.
- Corpus: 458 fixtures, all pass.
- Conformance: 356 clauses read, and no declaration names a missing clause.

Result: pass.
