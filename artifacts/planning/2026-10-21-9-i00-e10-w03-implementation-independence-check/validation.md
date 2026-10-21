# Validation — I00:E10:W03

Every run below was made unsandboxed from the worktree `.worktrees/i00-e10-w03`, with the build under test named by

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
```

## The base measured first

`make check` at the epic base `17f6e42` returns 0, so a result on the branch is attributable to the branch. Its build suite is 682 tests, its harness suite 541, and its corpus run reports 231 fixtures, 229 passing and 2 awaited.

## The repository check set

`make check` on `i00/e10/w03-implementation-independence-check` returns 0. Each of its fifteen targets passes: the lock check, lint, format check, type check, the build's own suite of 682 tests, the harness suite of 553, the corpus, the smoke run, and the layout, table, link, vocabulary, invocation, conformance and independence checks.

```text
corpus check: 231 fixture(s), 229 pass, 0 fail, 2 awaited, 0 unexpected pass
conformance report: 253 clause(s) the design states, 66 covered by no fixture,
0 declaration(s) naming no clause; 27 declared name(s) reached, 3 unfixturable
```

This row adds a check and the documentation naming it, and changes no fixture, so the corpus figures and the conformance report are the base's. `make tables` is what holds the new target to its documentation in both directions, in `README.md` and in `checks/README.md`.

## The independence suite

`make harness` grows by the twelve cases of `checks/tests/test_independence.py`, which supply the scan a corpus, a design and a documented invocation of their own rather than the repository's, so each case states what the check reads rather than what this repository happens to hold.

- **A declaration carrying an implementation module name fails.** A fixture whose `description` reads `The boundary is inserted by prosiform/emit.py.` yields one reference: the fixture's identity, the text `prosiform/emit.py`, and what it names, a source file of an implementation. This is the Test row's first half.
- **A corpus stating behaviour alone passes.** The same fixture whose description states the behaviour yields none.
- **A fixture identity naming an implementation fails.** `family/a-boundary-the-rust-build-inserts` yields `rust`, so the name a directory carries is held to the rule its manifest is.
- **A report entry naming an implementation fails.** A design whose clause reads `Block boundaries in the Rust build` yields `Rust` against the report lines carrying it, and the same corpus under the clean design yields none.
- **Each kind of term is named by what it is.** `Python`, `module`, `traceback`, `bundle.rs`, `__main__` and `ValueError` each return the kind of reference they are rather than the string that matched.
- **A term is a whole word.** `a node in the bundle, and a crated object` yields nothing, while `Node.js` and `node.js` each yield the term they are.
- **A span two patterns describe is read as the term it is.** `Node.js` is both the named term and the shape of a source file, and it returns the named term, because the inventory states its named terms before its shapes.
- **The interface terms pass.** The error codes, the warning codes, the exit statuses and the documented options return no reference, and a documented option spelled `--python-path DIR` returns one, so the disjointness is a verdict the check reaches rather than a claim made beside it.

## The check over this repository

`make independence` returns 0:

```text
ok   corpus      231 fixture(s) and their identities
ok   report      the conformance report as it renders
ok   interface   47 declared name(s)

independence check: 60 term(s), named by no fixture declaration, no report
entry and no name the contract declares
```

This is the Test row's second half: the check passes on the corpus as it stands. The 47 declared names are the 5 exit statuses, the 22 error codes and the 3 warning codes the manifest schema enumerates, and the 17 options the documented invocation's table names.

## The exclusions reviewed

The Review part of the work item is the confirmation that the exclusions admit no implementation term, and the check performs it: `declared_references` scans the contract's own declared names against the inventory and returns nothing, so the inventory and the contract's interface are disjoint. A contract that came to declare one — the case the suite shows with `--python-path DIR` — fails the run rather than being admitted.

Reviewing the inventory the other way, against the text the report draws its entries from, found two terms that name the contract rather than a build and were removed:

- **`import`.** The design's `Generic bundling` clause reads `Do not automatically import all of SKILL.md`, and its structural-ancestor rule `Do not traverse references from an ancestor-only heading or import its body`. The word is the contract's own for pulling content into a bundle.
- **`namespace`.** The design's validation scope reads `ancestor-only headings undergo structural, depth, and namespace checks`. A heading's namespace is a design concept, not a language's.

Neither sits in a clause name today, so neither was a current failure; both were removed because a clause name that used them would be refused for using the contract's vocabulary.

## What the validation found

- **The design's prose names both implementations, and the report's entries do not.** Scanning the design whole returns `Python`, `Rust`, `crate` and a `docs.rs` address: the design states which builds implement the contract and which parser candidate the production build starts from, which is the design's business rather than the corpus's. The report prints clause names, fixture identities and declared names, and none of those carries such a term, which is why the scan reads the report's entries rather than the document behind them. Nothing to fix.

- **The inventory is a list, and a list is reached by naming a term it does not hold.** A fixture could name an implementation in words the check does not carry — a build's own function name, a library the design never mentions. The disjointness check bounds the other direction and nothing bounds this one, so the check establishes that no *named* implementation term is bound rather than that no implementation is. Non-trivial and blocking nothing here, so it is deferred.

- **A fixture's source tree and expected bytes are out of scope by design.** They are the document a run consumes and the bytes it reproduces, and `fixtures/real-source/` deliberately bundles real documents naming real source files. Holding them to the rule would refuse the corpus its realism while saying nothing about what the corpus binds. The reading is correct and there is nothing to fix.

## What could not be ticked

**AC4 is ticked.** No fixture declaration, no fixture identity and no entry of the conformance report names an implementation language, the machinery of modules and packaging, a source file of an implementation, an identifier a language reserves, a fault class of an implementation or the wording a build gives its own fault, as `make independence` shows; and a declaration carrying an implementation module name fails the check, as the suite shows.

**AC1, AC7 and AC8 stay unticked**, which is the epic's reading unchanged. AC1 waits on the two adversarial families W01 left held by nothing, and AC7 and AC8 are W04 and W05, a unit this row does not carry.
