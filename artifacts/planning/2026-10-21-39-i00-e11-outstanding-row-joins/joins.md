# Joins Across the Outstanding Rows

The rows W24 through W29, the pair that shares a pull request, and the reason each other pair does not.

## No Row Depends on Another

None of the six consumes another's output. Each names an already-delivered row as its origin — W24 from W17, W25 from W23, W26 from W22, W27 from W19, W28 from W16, W29 from W18 — and nothing it produces is read by a sibling. All fifteen pairs therefore pass the dependency test, and each is settled on grain alone.

## The Pair That Shares a Pull Request

**W25 and W28.** Both are the standalone link check, both are exercised by `make links`, and neither is a pull request's worth on its own.

- W25 teaches the shared reading a list item's content column, so a code block indented inside a bullet is passed over while the item's own content, a nested bullet included, is read.
- W28 puts one resolvable tracker reference in a document the check finds, so the `gh api` route makes a real call when the repository checks itself.
- W28 is the row that cannot stand alone: its implementation is one reference in a Markdown document and an assertion over the check's output.

Together they read as one change — the check reads what a reader reads, over both of its routes — and the pull request holds their order.

## The Rows That Keep Their Own

Each of these carries a decision of its own, which is what makes it a unit.

| Row | What makes it a pull request |
| --- | --- |
| W24 | A manifest field naming the fault a run meets, a runner that performs it, and a build path that can be made to fail in itself, before either marker is lifted |
| W26 | A check over every definition `src/prosiform` makes, its `make check` target, its rows in both README command tables, its own tests, and the standing of the delivery wrapper |
| W27 | The text each group-rule fixture carries, and the decision on where a rule spelled with no colon is reported |
| W29 | A change in the arrangement, the decision between emitting the subsection and keeping the member's own heading, and the invariant that every selected document reaches the bundle |

## Why Each Remaining Pair Does Not Share

| Pair | Why |
| --- | --- |
| W24–W25, W24–W26, W24–W28, W24–W29 | W24's instrument is the work; pairing it with a reading, a check, a reference or an arrangement puts a runner capability behind another row's review |
| W24–W27 | Both touch the corpus, but one adds an instrument to the runner and the other decides which code a fault takes; the pull request would answer two questions |
| W25–W26, W26–W28 | All three sit in `checks/`, but W26 is a new check with its own design question, which a link-check pull request would bury |
| W25–W27, W25–W29, W27–W28, W28–W29 | Different surfaces entirely — the shared reading, the corpus catalogue and the arrangement have no file and no decision in common |
| W26–W27, W26–W29 | Each row carries its own contract decision; one pull request would carry two |
| W27–W29 | Both state something in the corpus, but one is a catalogue's coverage and the other an arrangement's invariant |

## A Consequence W27 Carries

Should the evidence put a rule spelled with no colon under `E_INVALID_USAGE`, that code's fixture set gains a seventh fault, each already declaring the text its message carries. That work belongs to W27 and is one reason it is not joined to a row that does not own the code.
