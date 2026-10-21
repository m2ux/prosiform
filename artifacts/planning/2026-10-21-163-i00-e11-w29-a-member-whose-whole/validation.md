# Validation

The checks this unit is held to, the procedure each was run by, and what each observed. Each result is attributable to the branch: the whole set was run on the base `i00/e11/main` at `313e1f2` before any change and on `i00/e11/w29-a-member-whose-whole` after all three were delivered.

Every run supplied the build under test by configuration, as the corpus, invocation, conformance and independence targets require, and ran unsandboxed:

```bash
export PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
make check
```

Each criterion this unit covers names the corpus or the grouping fixtures as its instrument, so each is observed by a fixture the corpus run reaches. A unit test accompanies each, and observes the component rather than the criterion.

## The three reproductions, before and after

Each fault was reproduced against the base before anything was changed, and the same invocation was run against the branch after.

### An autolink ends the run

**Base `313e1f2`.** A source whose selected content carries `<https://example.com/profile>`:

```text
E_UNEXPECTED_INTERNAL_ERROR: unexpected internal error: Unrewritable('the parser read 1 use(s) against the 0 the emission can edit in place')
status 4
```

**Branch.** Exit 0, and the autolink reaches the bundle as the source wrote it:

```text
See <https://example.com/profile> for more.
```

The email spelling behaves the same way, and the fixture carrying the constructs the profile supports declares both.

### A member is emitted nowhere

**Base `313e1f2`.** `index.md` references `docs/alpha.md`, whose whole content is `# Alpha`, and `docs/beta.md`. Under `--group docs:2` the run exits 0 and publishes:

```text
# Docs

## Overview

### Beta

Beta has a paragraph of its own.

# index

See [Alpha](#docs) and [Beta](#beta).
```

**Branch.** Same invocation, exit 0:

```text
# Docs

## Overview

### Alpha

### Beta

Beta has a paragraph of its own.

# index

See [Alpha](#alpha) and [Beta](#beta).
```

Under `--group docs:1` and under no rule at all the bundle is what it was, so the arrangement decides where the member's content sits and no longer whether it is carried.

### A newline spelling is rewritten

**Base `313e1f2`.** A source whose every line ends CRLF bundles to one where the line ending each region arrives LF:

```text
A paragraph nothing rewrites\r\nand its second line here.\n\n- one\r\n- two\n
```

**Branch.** The same source, exit 0:

```text
A paragraph nothing rewrites\r\nand its second line here.\r\n\n- one\r\n- two\r\n
```

The blank line between the two emitted parts is LF, which is the newline the bundle generates, and the generated entry line and file heading are LF with it.

## T1 — the grouping fixtures

`make corpus` over the `grouping/` family, which carries the member whose whole content is the heading its overview subsection absorbs, in three readings of one tree:

| Fixture | Declares |
| --- | --- |
| `grouping/an-entry-naming-a-member-carrying-one-heading` | An entry reference naming such a member resolves to the subsection the group's overview carries for it, under `--group notes:2`. |
| `grouping/a-member-carrying-one-heading-bundled-by-document` | The same two documents with no grouping rule in force, so the content carried is read against the grouped arrangement and the position is what differs. |
| `grouping/a-reference-to-a-member-carrying-one-heading` | A compiled reference naming such a member is rewritten to that subsection rather than to the group's own heading. |

The first two are the pair AC30 turns on: the same tree, the same entries, one bundled under a grouping rule and one without, each compared with its expected bundle byte for byte.

**Observed on the branch:** the family passes within `corpus check: 239 fixture(s), 239 pass, 0 fail, 0 awaited, 0 unexpected pass`. The two fixtures that stated the ended behaviour were rewritten to state what the arrangement does, and renamed, because a fixture's identity is read as a claim like its description.

**Coverage:** AC30.

## T2 — the CRLF fixtures

`make corpus` over the two fixtures that state the newline spelling in bytes:

| Fixture | Declares |
| --- | --- |
| `candidate-validation/every-line-terminated-with-crlf` | A source whose every line is terminated with CRLF carries those terminators on each line the bundle emits from it, the paragraph holding the rewritten link included, beside a source terminated with LF that keeps its own. |
| `candidate-validation/crlf-lines-beside-a-rewritten-link` | A code example the source terminated with CRLF keeps those terminators, the link in the paragraph above it is rewritten, and the generated boundary below the example is written with the newline the bundle generates. |

The second fixture's expected bundle stated the defect: the fence closing the code example arrived LF where its source wrote CRLF. Its bytes are corrected.

A bundle is compared byte for byte and the runner locates a difference by the offset of the first differing byte with the control bytes spelled out, so a CRLF against an LF is what the comparison reports rather than something it passes over.

**Observed on the branch:** both pass within the same corpus run. The whole corpus was run once with the source change in place and every expected bundle still at its pre-change bytes: one fixture failed, by exactly one byte, which is the measure of what the change touched and what it left alone.

**Coverage:** AC32.

## T3 — the autolink fixtures

`make corpus` over `profile/the-constructs-the-profile-supports`, the one document carrying every construct the profile supports. Its source carries both autolink spellings — `<https://example.com/profile>` and `<someone@example.com>` — in the paragraph that also carries an inline link, a reference-style link, an image and a code span, so the reading and the parser are held to the same count and the same order.

The fixture carried `awaiting = "I00:E11:W37"`. A fixture carrying that marker and meeting its manifest fails the run, so the change that delivers the work is the change that turns it red: the marker is removed by this delivery, and the corpus run reports `0 awaited`.

**Observed on the branch:** the fixture passes, and the run reports `0 awaited, 0 unexpected pass`.

**Coverage:** AC42.

## T4 — the build's own suite

`make test` and `make harness` run the build's unit coverage and the corpus harness.

The unit coverage added with this unit reads the three components: the scan reading an autolink in both spellings and leaving a bracketed run that is no autolink the text it is; a region carrying the terminator its source wrote and a generated part carrying the bundle's; and the overview subsection a member the arrangement emits nothing else from takes.

**Observed on the branch:** `723 passed` for the build's own suite and `596 passed` for the harness. On the base `313e1f2` the same targets reported `696 passed` and `594 passed`.

## T5 — the whole check, before and after

`make check` runs `lock-check`, `lint`, `format-check`, `typecheck`, `test`, `harness`, `corpus`, `smoke`, `layout`, `tables`, `links`, `vocabulary`, `invocation`, `conformance` and `independence` in order and stops at the first failure.

`make conformance` and `make independence` read the design from the `engineering` branch, so the design clause this unit restates was pushed before the run that observes it.

**Observed:**

| Revision | Result |
| --- | --- |
| Base `i00/e11/main` at `313e1f2`, before any change | exit `0`; `237 fixture(s), 236 pass, 0 fail, 1 awaited`; `242 clause(s) the design states, 0 covered by no fixture` |
| Branch `i00/e11/w29-a-member-whose-whole` at `a8d0f1f`, after all three | exit `0`; `239 fixture(s), 239 pass, 0 fail, 0 awaited, 0 unexpected pass`; `242 clause(s) the design states, 0 covered by no fixture, 0 declaration(s) naming no clause` |

The clause inventory is the same figure on both, because the design change restates one bullet's prose and names no new clause.
