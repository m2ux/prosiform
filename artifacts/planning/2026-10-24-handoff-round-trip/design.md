# Handoff Round-Trip: Design

An end-to-end suite compiles a bundle of the work-tracker example, reads the destinations that bundle publishes, and compiles each of them, so the claim that a withhold hands material to a later run is held by a test rather than by a reading of the code.

## The Gap

- **The design declares a handoff and nothing exercises it.**
  `make conformance` reports `File-owned invocation conformance cases — Deferred handoff: 0 fixture(s)`. Every existing deferral and dispatch fixture asserts the *emitted* form; none compiles what was emitted.

- **A fixture declares one invocation.**
  `manifest.invocation.arguments` is a single argument list run once, so a round-trip has no place to live in the corpus as it stands.

- **The claim is the whole point of both operators.**
  A `¬` link is material "reached in a run of its own"; a `»` link is material a sub-agent compiles. If the published destination cannot be compiled, both statements are false and the corpus says nothing.

## The Tree

`example/work-tracker/` is the corpus's own example material and the only tree in this repository that is compliant with the current contract:

| File | Declaration |
| --- | --- |
| `SKILL.md` | `root: "."` |
| `modes/plan-mode.md` | `root: ".."`, `group: "modes"`, `group-depth: 2` |
| `artifacts/epic.md` | `root: ".."`, `group: "artifacts"`, `group-depth: 2` |
| `artifacts/epic-issue-body.md` | `root: ".."`, `group: "artifacts"`, `group-depth: 2` |

- **It bundles clean.** `pf -o - modes/plan-mode.md` from `example/work-tracker` resolves every link, contributes the two artifact groups, and emits no authored `../` link.
- **The suite builds on it**, rather than on `skills/work-planner/`, which declares no root: every `../` link there escapes the working-directory root and is emitted as authored, so its bundles carry no artifact content at all.

## Probes

Measured with `pf 0.9.0 (skill-markdown-v1)` over a copy of the example tree, with `dispatch` declared on `SKILL.md` and a `## Dispatch` section linked from the mode's prerequisites:

| Probe | Result |
| --- | --- |
| `pf -o - modes/plan-mode.md` | the declared text is emitted after the entry sentence |
| a `»` link added to the mode | published as `artifacts/epic.md#delivery-findings` |
| a `¬` link added to the mode | published as `artifacts/epic-issue-body.md#fields` |
| `pf -o - 'artifacts/epic.md#delivery-findings'` | exit 0, heading `Delivery Findings` selected |
| `pf -o - 'artifacts/epic-issue-body.md#fields'` | exit 0, heading `Fields` selected |

## Decisions

- **A pytest module, not a corpus extension.**
  The round-trip needs two invocations and a parse of the first's output between them. Extending `manifest.schema.json` with a `handoff` step would put that machinery into the corpus for one family; a module in `src/tests/` runs the installed command twice and binds this build, which is the right scope for a delivery test.

- **The destination is read from the first bundle, never from the manifest.**
  Restating the authoring string in the test would assert that one string compiles twice. Parsing the published link is what makes the test a round-trip: it fails when emission writes a destination the build cannot resolve.

- **The tree is the example, copied to a temporary directory.**
  Each scenario starts from `example/work-tracker` copied into `tmp_path` and writes its own links into the copy, so the checked-in example is never mutated and the corpus's one-invocation rule is untouched. Fixture discovery takes any directory holding a manifest, so the copy adds no fixture.

- **Two operators, one mechanism.**
  `»` and `¬` publish the same destination rule, so one helper compiles either destination. The rows differ only in which operator wrote the link.

- **The guard is its own row.**
  `E_GENERATED_INPUT` is a different claim from a handoff: it states that a published bundle is refused as input. It gets its own test naming the line the declaration occupies.

## The Stacks

- **The dispatch stack** writes `[» the epic](../artifacts/epic.md#delivery-findings)` into the mode, so the published destination is `artifacts/epic.md#delivery-findings`.
- **The deferral stack** writes `[¬ the issue body](../artifacts/epic-issue-body.md#fields)`, so the published destination is `artifacts/epic-issue-body.md#fields`.
- **The both-operators stack** writes one link of each into one mode, so a single bundle publishes two destinations and each compiles.
- **The escaped stack** names a target whose path carries a character the destination escapes, and compiles what the bundle published.
- **The dialog stack** declares `dispatch` on `SKILL.md` and links that section from the mode's prerequisites, so the opening line carries the text — the emission AC1 of the dispatch epic depends on.

## Checks

- **The second run's bundle is compared whole**, not by substring, so a wrong heading level or a dropped preamble fails.
- **The second run's exit status is zero**, and its diagnostics carry no error.
- **The guard test asserts the code and the line**, so a change that moves the entry line fails the fixture rather than passing silently.
- **The rows are named for the situation**, not the mechanism: a dispatched link's destination compiles, a deferred link's destination compiles, an escaped destination compiles, both destinations compile from one bundle, and a published bundle is refused as input.
