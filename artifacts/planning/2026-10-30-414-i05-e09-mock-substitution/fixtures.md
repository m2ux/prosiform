# Fixture Inventory

Every corpus fixture this epic lands, the row that lands it, and the criterion it proves. A fixture lands in the pull request that makes it pass, so no fixture is written against a prediction.

## The family

All nineteen sit under a new `fixtures/mock/` family. Each declares a `source/` tree, an `expected/stdout.md`, and a `manifest.toml` naming the design clause W00 lands.

Two family-wide obligations:

- **Every fixture names the clause W00 lands,** or `make conformance` refuses the declaration.
- **Both warning codes need a fixture declaring them,** because `make conformance` reads `pf -C` and reports a code the contract declares and no manifest names as a failure.

## How a fixture carries a mapping

Four facts about the corpus decide the shape of every manifest here, and each was read from the checks rather than assumed.

- **`arguments` is a list, one element per argv entry,** so `-m` and its `ORIGINAL=ALTERNATIVE` are two elements. The value needs no shell quoting because no shell sees it, which is why a fragment key is written `rules.md#escalation=stand-in.md` and not as a quoted word.
- **The value's sides resolve from `invocation.cwd`,** which `runner.py` passes as the process's working directory. A substitute therefore sits inside the fixture's source tree, or above it by a parent segment.
- **`expected.absent` resolves against the fixture directory, not `cwd`.** `compare_absent(fixture, …)` takes the fixture root, so a run publishing under `cwd` writes to `source/<name>` and the declaration reads `source/<name>`. Every `absent` declaration in this family names the `source/`-prefixed path for that reason.
- **A fixture naming `-o -` writes nothing at all,** which is what the two example-skill fixtures do, because their source is a symbolic link to the repository's own example tree and a published file would land inside it.

A fixture whose `source` is a symbolic link follows the `usage-example` family's pattern: the tree is reached rather than copied, so no fixture can drift from the material it tests.

**A linked `source` cannot carry a substitute.** `execute` takes `Path.cwd().resolve()`, so a working directory reached through a symbolic link resolves to the link's target, and a `../stubs` value lands beside the target rather than beside the fixture. The two example-skill fixtures therefore hold a real copy of `example/work-planner` under `source/`, and are held to the original by `cmp` outside the corpus, as the `real-source` family already is. Every other fixture here owns a small tree and is unaffected.

## W01 — Mapping, option and identity

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-mocked-dependency-is-compiled` | AC1 | A compiled link resolves to the substitute, which is bundled under its own file heading, with `W_MOCK_SUBSTITUTED` naming the link. |
| `a-substitute-outside-the-writing-root-is-reachable` | AC11 | A source declaring `root: .` reaches a substitute beside its tree, which the same run without `-m` refuses as `E_TARGET_NOT_FOUND`. This is the feature's justification, and no unit test can show it. |
| `a-key-naming-an-absent-document-is-substituted` | AC18 | A key naming a document that does not exist compiles its substitute, where the same run without `-m` fails `E_TARGET_NOT_FOUND`. This is what makes an artifact under authoring testable before it lands. |
| `a-substitute-above-the-working-directory-is-reachable` | AC20 | A mapping value carrying `..` reads a stub above the working directory, and the warning names it by that path. |

AC15 is the option's row in `invocation.md`, held to the help output by `make invocation` rather than by a corpus fixture.

## W02 — Key and self-mock refusals

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-duplicate-key-is-refused` | AC9 | Two spellings of one identity on the command line: `E_INVALID_USAGE`, exit `2`, nothing published. |
| `a-self-mock-is-refused` | AC10 | A key and value normalizing to one identity: `E_INVALID_USAGE`, exit `2`, nothing published. |

## W03 — Entry redirect and derived name

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-redirected-entry-derives-its-name-from-the-substitute` | AC2 | The run publishes `stand-in.bundle.md`, and `absent` names `entry.bundle.md`. |
| `a-redirected-referrer-carries-its-entry` | AC13 | A fragment-only entry resolves its section against the substituted referrer. |

## W04 — Substitution warnings and check mode

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-substitution-warns-with-its-target` | AC7 | One `W_MOCK_SUBSTITUTED` per target however many references the key served, with `location`, `source` and `resolved`. |
| `an-unused-key-warns-and-publishes` | AC8 | `W_MOCK_UNUSED` with exit `0` and a published bundle. |
| `a-mocked-check-publishes-nothing` | AC19 | `-c` with a mapping resolves and warns exactly as a publishing run does, and `absent` names the output path. |

## W05 — Withheld and dispatched targets

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-deferred-target-is-redirected` | AC4 | The published destination is the substitute's working-directory-relative path, and the original is never opened. |

## W06 — Section keys and the end of chaining

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-fragment-key-redirects-one-section` | AC3 | One section compiles the substitute while the rest of its document compiles as it ships. |
| `a-document-key-and-a-section-key-together` | AC14 | Both keys of one document serve their references, and the narrower takes the section it names. |
| `a-substitute-that-is-a-key-is-not-redirected-again` | AC12 | The substitute is read from disk, and the key naming it is reported unused rather than followed. |

## W07 — The substitute as a source

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `a-substitute-declaring-a-group-joins-it` | AC5 | The substitute's own `group` and `group-depth` decide its membership, and its section appears under its own member heading. |
| `a-substitute-root-bounds-its-own-links` | AC6 | The substitute's declared root bounds its outgoing links, so a link above it stays a citation. |

## W08 — The example skill over the mechanism

| Fixture | Criterion | Declares |
| --- | --- | --- |
| `an-example-mode-bundled-against-a-stub` | AC21 | `plan-mode.md` bundles against a stubbed `artifacts/epic.md`, and the example tree is byte-identical afterwards. |
| `an-example-skill-told-to-use-a-fake-gh` | AC22 | A redirected `conventions.md` names `./fake-gh`, so an agent following the bundle runs the fake while every other instruction stays real. |

## Why the last two families carry no fixture

- **A dispatched target and a run-set target** are redirected by the same `withholding_target` resolution W05 covers, and their effect is a second run rather than a bundle this run publishes. `src/tests/test_mock.py` holds both, as E00 held its candidate fault.
- **A candidate comparison against a mocked bundle** is unreachable from a source tree: it is the fault path for an emission that disagreed with its source. A unit test carries it, as it carries every internal fault.
