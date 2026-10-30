# Dispatch Operator: Design

A second link operator states that a link's material belongs to a sub-agent, and the entry document's metadata states what the operator means. The deferral mark stops being published.

## The Operator

- **`»` opens a link whose material a sub-agent compiles.**
  It keeps everything `¬` already does: the target contributes no content, no dependency is added through the link, and no group membership follows. The target must exist and name the heading it names, because a dispatch an agent performs is one that can succeed.

- **The destination is the deferred destination.**
  [`rebased`](https://github.com/m2ux/prosiform/blob/15c78052c2d8779fce45893df08e3670763b3150/src/prosiform/closure.py#L400-L405) already produces the target's URI-escaped working-directory-relative path with its fragment. A dispatched run compiles that path from the root the bundle names, so the operator adds no destination rule of its own.

- **The link publishes its mark.**
  `»` is the only thing in the bundle saying the material belongs to another agent. A `¬` link's destination already differs from a compiled link's, so the two marks are not redundant with each other and only the deferral mark is removed.

- **One operator per link.**
  Text opening with both marks is refused. One compilation cannot wait for a later run and be dispatched by this one, so the link states two contradictory things and the run says so rather than choosing.

## The Metadata

- **`prosiform.dispatch` is a nonblank single-line string.**
  It states what a `»` link means for that skill, in the skill's own words. The compiler assigns the string no structure and validates it as it validates `group`.

- **The bundle emits it after the entry sentence.**
  A reader meets the rule and the entries as one instruction. Absent, no instruction is emitted and the entry line is the one the corpus already records.

- **Every contributing source agrees on the value.**
  A second value fails with `E_INVALID_CONVERSION_METADATA` naming both locations. A bundle whose opening line depended on which source was read first would make the instruction a property of traversal order.

- **The key joins the admitted set.**
  `root`, `group`, `group-depth`, `group-heading` and `dispatch` are the keys [`metadata.py`](https://github.com/m2ux/prosiform/blob/15c78052c2d8779fce45893df08e3670763b3150/src/prosiform/metadata.py#L338) admits, and an unknown key still fails.

## The Published Form

- **A deferred link publishes its text without the mark.**
  The mark and the spaces following it go, and the text and destination stay. `[¬ Codex](rules/codex.md)` publishes as `[Codex](rules/codex.md)`.

- **Classification does not move.**
  `¬` still withholds a compilation and its target is still required. What changes is one emission rule, so discovery, validation and the corpus's failures are untouched.

- **Nine expected stdout files are regenerated and eight test modules revised.**
  The mark is asserted as published content in nine fixtures and sixty-seven occurrences across nine test modules, so the change is measured from the side that states the output rather than from the side that states the input.

## Decisions

- **Two marks, two statements.**
  `¬` says when, `»` says who. Collapsing them into one operator with a value would make either statement unreadable wherever the other is absent.

- **A metadata key rather than a top-level field.**
  `invocation.md` states that `metadata` has no conversion meaning. Teaching the compiler to read the field skills already carry for harnesses would attach conversion behaviour to a name another consumer owns.

- **Three rows and two pull requests.**
  Rows W01 and W02 change different stages of one emission path and neither depends on the other, so they are separate pull requests. W03 consumes W01's key, so it follows it.

- **No order between the marks' delivery.**
  A bundle may carry `»` links while `¬` links still publish their mark, so the two changes land independently.

## Open Questions

None. The operator, the key name and the published form are settled, and the plan changes the delivery surfaces.
