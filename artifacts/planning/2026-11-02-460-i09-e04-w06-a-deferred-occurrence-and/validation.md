# Validation

The checks [W06](w06.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (README pin) | `3ed0bf02`. It carries `cf382468`, the pin W09 set, and adds the operator-syntax amendment to *The deferral mark*, *Operators that combine*, *Recognition* and *Operator marks*. |
| Branch head | `e5ec64a9` on `i09/e04/w06-a-deferred-occurrence-and`, with `i09/e04/main` merged in at `cb72fee2` |

## T1 Eligible Target Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-directive-naming-a-document-that-declares-nothing-is-refused` | `[→](notes.md#output)`: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, "declares no prosiform" | AC11 |
| `a-deferred-directive-naming-a-document-that-declares-nothing-is-refused` | `[¬→](notes.md#output)`: the operator refusal, at `guide.md:8` | AC11 |
| `a-directive-naming-a-remote-address-is-refused` | `[→](https://example.com/step.md#output)`: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8` | AC11 |
| `a-directive-naming-a-resource-is-refused` | `[→](step.txt)`: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8` | AC11 |
| `a-directive-naming-a-whole-document-is-refused` | `[→](step.md)`: `E_UNSUPPORTED_CONSTRUCT` at `guide.md:8`, no bundle | AC11 |

Result: pass.

## T2 Composed Contract Fixture

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-composed-contract-leaves-its-deferred-implementation-absent` | A step composes `fetch.md#contract` and defers `fetch.md#implementation`. Contract's body is composed under `### Contract` / `#### Fetch`. `### Implementation` / `#### Fetch` carries only `[↳ Implementation](fetch.md#implementation)`. Neither the implementation's body nor `net.md`, which it composes, reaches the bundle. The links read `[→](#fetch)` and `[→](#fetch-1)`. | AC12 |

Result: pass.

## T3 Activation Fixtures

| Fixture | Shows | Criterion |
| --- | --- | --- |
| `a-deferred-directive-is-activated-by-the-run-its-line-names` | `pf fetch.md#implementation`, over T2's sources, publishes the implementation. `net.md#open` is composed beneath it, and `net.md#retry`, deferred again, keeps `#### Retry` / `##### Net` with `[↳ Retry](net.md#retry)`. | AC13 |
| `a-deferred-body-that-fails-is-deferred-without-failing` | An implementation carrying raw HTML is deferred by the step composing its contract, which publishes with no diagnostic. | AC13 |
| `a-deferred-body-that-fails-fails-when-activated` | The run its line names fails with `E_RAW_HTML` at `fetch.md:12` and publishes nothing. | AC13 |

Result: pass.

## T4 Symbol Syntax

| Fixture or test | Shows |
| --- | --- |
| `a-glyph-written-against-the-deferral-mark-is-a-deferred-directive` (was `a-deferred-glyph-label-is-a-deferred-directive`) | `[¬→]` in a preamble is a deferred directive, refused for want of a scope. |
| `a-blank-between-the-deferral-mark-and-a-glyph-is-refused` (new) | `[¬ →]`: `E_UNSUPPORTED_CONSTRUCT` naming `¬ →` at `guide.md:8`, "written together". |
| `a-blank-between-the-dispatch-mark-and-a-glyph-is-refused` (was `a-dispatched-glyph-is-a-dispatch`) | `[⇉ →]`, a dispatch whose text was `→`, is refused, naming `⇉ →`. |
| `operator-marks-are-no-directive-label` | `[¬→]` became a deferred directive, so the fixture's text-mark case is now `[⇉→]`. |
| `test_composition.py`, `test_closure.py` | `[¬→]`, `[¬&rarr;]` and `[¬𝔸]` are deferred directives. The blank forms `[¬ →]`, `[¬  →]`, `[¬ &rarr;]`, `[⇉ →]`, `[⫽ →]`, `[¬⇉ →]`, `¬ ⇉`, `¬ ⫽`, `⇉ ⫽` and `⇉ ¬` are refused. `[¬¬]`, `[¬↳]`, `[¬ ↳]` and `[¬→ ]` are no directive, and `[⇉→]`, `[⫽→]` and `[ ¬→]` are text. |

Result: pass.

## T5 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exited 0 at `e5ec64a9`. Results:

- Unit tests: 1635 passed. The harness ran 1144.
- Corpus: 483 fixtures, all pass.
- Conformance: 354 clauses. *The eligible target* has 8 fixtures, *Deferred composition* 3, *Activation* 3, *Operators that combine* 10 and *Operator marks* 5.
- Independence: every term is one the contract names.

Result: pass.
