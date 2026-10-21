# Validation

The checks this work is held to, the procedure each was run by, and what each observed. Each result is attributable to the branch: the whole set was run on the base `i00/e11/main` at `8cd9534` before the change and on `i00/e11/w34-an-implementation-reference-the` after it.

Every run supplied the build under test by configuration, as the corpus target requires:

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform" make check
```

## T1 — the check's own suite

`make harness` runs the suite in `checks/tests`, which carries the rewritten `test_independence.py`: 20 cases over the positive rule.

The cases read both directions of it. A declaration stating a word no source holds is reported, as are a fixture identity naming a build, a design clause naming one, and a word the register does not admit. A word the glossary defines, a word the register admits, an interface term the contract declares and an inflection of a stated word each pass. The rest hold the reading: a word is resolved to the form the contract states rather than to the form a sentence inflects, a hyphenated compound is its parts, case is folded on the reading side so a capitalised `Python` is reported, a letter carrying a sign is a word and a single letter is not, a code span in a claim names the fixture's tree, and the paths, reference texts and arguments a manifest declares are not read as words.

**Observed:** `594 passed`, the whole harness suite, on the branch at its merged head. The same target passed on the base before the change.

## T2 — the rule over the corpus as it stands

`make independence` reads the corpus's 237 fixture declarations and the conformance report as it renders against the vocabulary the contract states.

**Observed on the branch:**

```text
ok   vocabulary  2309 word(s) from artifacts/planning/2026-10-17-prosiform-v1/design.md,
                 docs/glossary.md, 51 declared name(s) and docs/corpus-vocabulary.md
ok   corpus      237 fixture(s) and their identities
ok   report      the conformance report as it renders

independence check: every word of every fixture declaration and every report entry is
one the contract states
```

The run is clean, which is the observation AC37 asks for. Every word the rule reported before the register was written was given a verdict; the verdicts and their dispositions are in [analysis](analysis.md). No fixture declaration was changed to reach the clean run.

## T3 — the glossary and the contract still agree

`make vocabulary` holds the shipped glossary to the terms the design marks, in both directions. The register is a separate file and does not enter it, so admitting a word to the corpus's vocabulary cannot quietly become a contract term.

**Observed:** `35 contract term(s) marked … every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)` — the same result on the base and on the branch.

## T4 — the whole check, before and after

`make check` runs the set in order and stops at the first failure.

**Observed:** exit `0` on the base `i00/e11/main` at `8cd9534` before the change, and exit `0` on the branch after it and again after each merge of the epic base into it. `696 passed` for the build's own suite and `594 passed` for the harness, with `lint`, `format-check`, `typecheck`, `lock-check`, `corpus`, `smoke`, `layout`, `tables`, `links`, `vocabulary`, `invocation`, `conformance` and `independence` each reporting their own result.

## T5 — the retired inventory, term by term

The 60 terms the inventory held were each put into a claim — `The run reports it through <term> in the bundle.` — and read against the repository's own vocabulary, before the inventory was removed. The rule reports 59 of them.

### An implementation language or runtime

| Term | Reported | Words the rule reads |
| --- | --- | --- |
| `python` | yes | python |
| `cpython` | yes | cpython |
| `pypy` | yes | pypy |
| `rust` | yes | rust |
| `golang` | yes | golang |
| `java` | yes | java |
| `jvm` | yes | jvm |
| `kotlin` | yes | kotlin |
| `scala` | yes | scala |
| `clojure` | yes | clojure |
| `javascript` | yes | javascript |
| `typescript` | yes | typescript |
| `nodejs` | yes | nodejs |
| `node.js` | yes | js |
| `deno` | yes | deno |
| `ruby` | yes | ruby |
| `perl` | yes | perl |
| `php` | yes | php |
| `haskell` | yes | haskell |
| `erlang` | yes | erlang |
| `elixir` | yes | elixir |
| `swift` | yes | swift |
| `dotnet` | yes | dotnet |
| `csharp` | yes | csharp |
| `ocaml` | yes | ocaml |

### The machinery of modules and packaging

| Term | Reported | Words the rule reads |
| --- | --- | --- |
| `module` | yes | module |
| `submodule` | yes | submodule |
| `package` | yes | package |
| `classpath` | yes | classpath |
| `venv` | yes | venv |
| `virtualenv` | yes | virtualenv |
| `pip` | yes | pip |
| `pypi` | yes | pypi |
| `setuptools` | yes | setuptools |
| `pyproject` | yes | pyproject |
| `sdist` | yes | sdist |
| `wheel` | yes | wheel |
| `npm` | yes | npm |
| `cargo` | yes | cargo |
| `crate` | **no** | none |
| `maven` | yes | maven |
| `gradle` | yes | gradle |
| `gemspec` | yes | gemspec |
| `stdlib` | yes | stdlib |
| `dunder` | yes | dunder |

### The wording a build gives its own fault

| Term | Reported | Words the rule reads |
| --- | --- | --- |
| `traceback` | yes | traceback |
| `stacktrace` | yes | stacktrace |
| `stack trace` | yes | stack, trace |
| `panic` | yes | panic |
| `unwrap` | yes | unwrap |
| `errno` | yes | errno |
| `segfault` | yes | segfault |
| `segmentation fault` | yes | segmentation |
| `core dump` | yes | dump |
| `assertion failed` | yes | assertion |

### The shapes the inventory matched

| Term | Reported | Words the rule reads |
| --- | --- | --- |
| `prosiform/emit.py` | yes | py |
| `bundle.rs` | yes | rs |
| `__main__` | yes | main |
| `ValueError` | yes | ValueError |
| `c++` | yes | c++ |
| `c#` | yes | c# |

**The one term the rule does not report** is `crate`, which the design states where it leaves the production build's slugging component unchosen. The vocabulary admits it because the design states it, which is what AC36 asks of the rule. The disposition is in [analysis](analysis.md) and the design's naming of a build's packaging is raised as its own work.

## Revisions the validation forced

- **The resolution of a plural was over-eager.** `clauses` resolved to `claus` and `loses` to `los`, so a word the design states was reported. The candidate forms are now a set rather than a single key, and every applicable rule contributes to it.
- **A doubled consonant lost the word it was formed from.** `filled` resolved only to `fil`, so the register's `fill` did not admit it. Both the stem and its de-doubled form are now candidates.
- **The design's code spans and link destinations admitted a library's name.** Reading them as prose would have admitted the parser candidate the design names in a code span. They are read no further than a path is.
- **Reading the design case-blind admitted two languages.** `Python` and `Rust` entered the vocabulary from the design's status and parser sections. The stating side is no longer case-folded.
- **Merging the epic base twice brought new report prose.** The conformance report came to state the codes a build reports for itself and the sections of the design stating no behaviour. Each word those entries add was given a verdict and registered, and the whole check was run again on each merged head.
