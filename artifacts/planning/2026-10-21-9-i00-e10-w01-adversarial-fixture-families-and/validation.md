# Validation — I00:E10:W01

Every run below was made unsandboxed from the worktree `.worktrees/i00-e10-w01`, with the build under test named by

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
```

## The base measured first

`make check` at the epic base `68944e8` returns 0, so a result on the branch is attributable to the branch. The corpus run there reports 210 fixtures, 208 passing and 2 awaited.

## The repository check set

`make check` on `i00/e10/w01-adversarial-fixture-families-and` returns 0. Each of its thirteen targets passes: the lock check, lint, format check, type check, the build's own suite of 652 tests, the harness suite of 387, the corpus, the smoke run, and the layout, table, link, vocabulary and invocation checks.

The manifest validation inside `make harness` is what holds the five new fixtures to the schema: each declares the five required declarations, names a code the catalogue its severity selects carries, and names only paths the fixture holds.

## The corpus run

`make corpus` reports:

```text
corpus check: 215 fixture(s), 213 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The five fixtures this row adds pass against the Python build. The two awaited fixtures are the two the corpus already carried.

## The family listing

AC1 is observed by the conformance report's family listing, which is [W02](https://github.com/m2ux/prosiform/issues/9)'s work. Until it exists the criterion is observed by [`family-listing.py`](family-listing.py), which reads the family bullets of the design's `## Adversarial acceptance fixtures` section and the `clauses` of every manifest in the corpus, and prints each family against the fixtures naming it. It is a listing rather than a check: it maintains no mapping of its own, so what it reports is what the design and the corpus say between them.

```bash
python3 family-listing.py <design.md> <fixtures-dir>
```

Its run over this branch reports 25 of the 27 families held, and two held by no fixture:

```text
UNHELD    Consistency
UNHELD    Parser exhaustion
27 family(ies) the design names, 2 held by no fixture
```

**W02 replaces it.** The conformance report reads the same two declarations — the design's family bullets and each manifest's `clauses` — alongside the clause-to-fixture mapping, and emits the family listing as one of its sections. The script goes when the report lands; the declaration it reads is the durable artifact and stays in the manifests.

## The awaiting markers

AC6 is observed by the corpus run, which names each awaited fixture and the work it awaits:

```text
grouping/a-rule-matching-no-document-in-the-closure: awaited, awaiting I00:E11:W14
reference/a-link-inside-image-alternative-content: awaited, awaiting I00:E11:W10
```

Both name [I00:E11](https://github.com/m2ux/prosiform/issues/39), the initiative's deferred-debt epic, which AC6 permits. A search of every manifest in the corpus for `awaiting` returns these two and nothing else, so no fixture awaits work inside this initiative other than that epic.

## What the validation found

- **A paragraph the source terminated with CRLF bundles terminated with LF.** The design requires untouched content to keep its original bytes and its newline spelling. A fenced block keeps its CRLF terminators and the prose around it does not, so one bundle carries two newline spellings after a run that was asked to change neither. Non-trivial and blocking nothing here, so it is deferred as [I00:E11:W31](https://github.com/m2ux/prosiform/issues/165) and the fixture this row adds states the case that holds.
- **`E_PARSER_REFERENCE_LIMIT` is declared by the catalogue and emitted by nothing.** The Parser exhaustion family turns on a parser resource limit rather than on a source tree, so no fixture can declare it ahead of a build that reaches the limit. Deferred as [I00:E11:W30](https://github.com/m2ux/prosiform/issues/164).
- **Consistency is the other family no source tree can state**, and [I00:E11:W24](https://github.com/m2ux/prosiform/issues/150) already holds it: its AC25 ends in the corpus fixture a run reaches unmarked.

## What could not be ticked

**AC1 is left unticked.** Twenty-five of the twenty-seven families the design names are held by fixtures and named by them. The two that are not are the two whose condition no source tree and one invocation can declare, and each is now a tracked row. The criterion is also observed by a report that does not exist yet, so the listing above is the evidence available and W02's report is what ticks it.

**AC6 is ticked.** The corpus run names both awaited fixtures and both name the deferred-debt epic.
