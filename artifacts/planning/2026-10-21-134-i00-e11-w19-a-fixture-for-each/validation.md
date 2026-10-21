## Overview

What the corpus was measured to state on `i00/e11/w19-a-fixture-for-each` at `1e0e8dd`, cut from the epic base `i00/e11/main` at `ce4483c`.

## The Gap

`E_INVALID_USAGE` gathers six faults, which the design states in one sentence of the CLI contract: a missing `--root`, no entry reference, an option the contract does not declare, an option value outside the set its row names, a fragment-only reference with no `--from`, and an output path naming an input source.

On the base, three were stated by the corpus — `cli/diagnostics-format-unknown`, `cli/fragment-only-reference-without-from` and `cli/output-naming-an-input-source`, each declaring the run's own data its message carries. The other three were stated by the build's own tests alone, and one of them by nothing a manifest could write: the runner prepended `--root` and the fixture's resolved source tree to every invocation, so no manifest could describe a run supplied no allowed source root.

## The Decision

The runner supplies the allowed source root a manifest names, and supplies none where the manifest names none. The fault is therefore stated by a fixture rather than recorded as one no fixture can declare, which is the stronger of the two arms AC20 admits.

The alternative — recording the fault as outside what a fixture can reach — leaves a clause of the CLI contract held by one build's tests, which bind that build and not the contract. The corpus exists to bind any implementation, so the expressive gap sat in the instrument rather than in the fault.

`invocation.root` is therefore optional in the schema. Every other rule about it is unchanged: a fixture declaring `E_ROOT_NOT_FOUND` names a root it does not hold, and every other fixture naming one holds it as a directory.

## The Faults, as the Build Reports Them

Measured against the build under test at `1e0e8dd`, with the fixture's own source tree where the manifest names one:

```text
$ prosiform --root source --diagnostics json --no-such-option guide.md
{"severity": "error", "message": "unrecognized arguments: --no-such-option", "code": "E_INVALID_USAGE", ...}
status 2

$ prosiform --root source --diagnostics json --check
{"severity": "error", "message": "at least one entry reference is required", "code": "E_INVALID_USAGE", ...}
status 2

$ prosiform --diagnostics json guide.md
{"severity": "error", "message": "--root is required and names the allowed source root", "code": "E_INVALID_USAGE", ...}
status 2
```

## The Fixtures

| Fixture | Declares | Carried text |
| --- | --- | --- |
| `cli/an-option-the-contract-does-not-declare` | Exit 2, one error `E_INVALID_USAGE` | `--no-such-option` |
| `cli/a-command-line-naming-no-entry-reference` | Exit 2, one error `E_INVALID_USAGE` | `entry reference` |
| `cli/a-command-line-naming-no-allowed-source-root` | Exit 2, one error `E_INVALID_USAGE`, no source tree | `--root` |

Each passes against the build under test, and the corpus run reports 220 fixtures, 220 passing, none awaited.

## Each Fixture Against Another Fault

A fixture that passes whatever fault the build reports states nothing about which fault it is. Each new fixture was run against a build replaying a different fault under the same code, exit status and severity — the whole of the result identical but the message:

```text
cli/a-command-line-naming-no-allowed-source-root: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    '--root' is absent
    produced 'at least one entry reference is required'
cli/a-command-line-naming-no-entry-reference: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    'entry reference' is absent
    produced '--root is required and names the allowed source root'
cli/an-option-the-contract-does-not-declare: fail
  expected.diagnostics: diagnostic 1's message does not carry 1 declared text
    '--no-such-option' is absent
    produced 'at least one entry reference is required'
```

## The Harness

| Case | Measured |
| --- | --- |
| A manifest naming a root | The run receives `--root`, the resolved tree, and the diagnostic format |
| A manifest naming no root | The run receives the diagnostic format and the arguments alone |
| A manifest naming no root | Validates against the schema |
| A manifest naming no arguments | Refused as malformed, as each other declaration is |
| A fixture declaring `E_ROOT_NOT_FOUND` | Still held to a root it does not hold |

## The Guide

The corpus guide carries the six faults the code names and the fixture stating each, so coverage under one code is read from the corpus. It also carries the invocation a manifest naming no root declares, beside the one that names a root the run cannot find.

## The Gate

Measured in the delivery worktree at `1e0e8dd`.

| Target | Result |
| --- | --- |
| `make lock-check` | Resolved 22 packages |
| `make lint` | All checks passed |
| `make format-check` | 50 files already formatted |
| `make typecheck` | Success: no issues found in 49 source files |
| `make test` | 670 passed |
| `make harness` | 491 passed |
| `make corpus` | 220 fixture(s), 220 pass, 0 fail, 0 awaited, 0 unexpected pass |
| `make smoke` | Installed, bundled and glossary shipped |
| `make layout` | 3 tree(s) present |
| `make tables` | 14 command(s) and 7 declaration(s) |
| `make links` | Every reference in 12 document(s) resolved |
| `make vocabulary` | 35 contract term(s) across 23 source(s) |
| `make invocation` | 27 statement(s) held to the build |

## Limitations

The fixture for a command line naming no entry reference declares the carried text `entry reference`, which is the contract's own term for what the command line supplies none of rather than an option spelling. The other five faults name an option or a path the run was given, which no phrasing can avoid carrying. A build reporting this fault in another language carries the term only where it carries the contract's vocabulary, so this one fixture binds a build's wording further than the other five do. The alternative — declaring nothing — would pass any `E_INVALID_USAGE` the build cared to emit, which is the gap this row closes.

The runner supplies the diagnostic format on every invocation, so a command line naming an unreadable `--diagnostics` value is stated and a command line naming none is not. The contract declares a default for that option, so a run supplied none is a well-formed run rather than a fault, and nothing is left unstated by it.
