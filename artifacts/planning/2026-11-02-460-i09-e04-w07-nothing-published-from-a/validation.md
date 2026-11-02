# Validation

The checks [W07](w07.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `aa97db93`. It carries `3ed0bf02` and adds the dispatch-mark refusal to *Operators that combine* and *Operator marks*, and the named-output failure to the Composition fixture list. |
| Branch head | `1fda6796` on `i09/e04/w07-nothing-published-from-a` |

## T1 to T3 Failure Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-composition-failing-in-a-dispatched-bundle-publishes-nothing` | The entry composes cleanly; the dispatched `log.md` collides with its authored `Inputs`. `E_HEADING_COLLISION` at `log.md:8`, exit 1, empty standard output, no `guide.bundles` folder. | AC14 |
| `a-composition-failing-under-a-named-output-folder-publishes-nothing` | `-o out guide.md`: the dispatched `fetch.md` composes past H6. `E_HEADING_DEPTH_OVERFLOW` at `fetch.md:16`, exit 1, `out` never made. | AC14 |
| `a-composition-failing-in-a-check-run-publishes-nothing` | `-c guide.md` over T1's sources fails alike and writes nothing. | AC14 |

Result: pass.

## T4 Dispatch Mark Against a Glyph (Folded)

| Fixture or test | Shows |
| --- | --- |
| `a-dispatch-mark-written-against-a-glyph-is-refused` (new) | `[⇉→](step.md#output)`: `E_UNSUPPORTED_CONSTRUCT` naming `⇉→` at `guide.md:8`. |
| `operator-marks-are-no-directive-label` | The `[⇉→]` case is now `[⇉step]`, a mark written against text, carried as written. |
| `test_composition.py` | `[⇉→]`, `[⫽→]`, `[⇉&rarr;]`, `[¬⇉→]` and `[⇉𝔸]` contradict; `[ ¬→]`, `[ ⇉→]`, `[⇉step]` and `[¬→]` do not. |

Result: pass.

## T5 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `1fda6796`. Results:

- Unit tests: 1643 passed. The harness ran 1148.
- Corpus: 487 fixtures, all pass.
- Conformance: 354 clauses. *Section composition — Failure* has 3 fixtures, *Operators that combine* 11 and *Operator marks* 6.
- Independence: every term is one the contract names.

Result: pass.
