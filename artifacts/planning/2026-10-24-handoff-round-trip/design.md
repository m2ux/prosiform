# Handoff Round-Trip: Design

An end-to-end suite compiles a bundle, reads the destinations that bundle publishes, and compiles each of them, so the claim that a withhold hands material to a later run is held by a test rather than by a reading of the code.

## The Gap

- **The design declares a handoff and nothing exercises it.**
  `make conformance` reports `File-owned invocation conformance cases — Deferred handoff: 0 fixture(s)`. Every existing deferral and dispatch fixture asserts the *emitted* form; none compiles what was emitted.

- **A fixture declares one invocation.**
  `manifest.invocation.arguments` is a single argument list run once, so a round-trip has no place to live in the corpus as it stands.

- **The claim is the whole point of both operators.**
  A `¬` link is material "reached in a run of its own"; a `»` link is material a sub-agent compiles. If the published destination cannot be compiled, both statements are false and the corpus says nothing.

## Probes

Measured on `i01/e09/main` at `5749da28` with `pf 0.9.0 (skill-markdown-v1)`, over a synthetic tree holding `entry.md` and `lib/steps.md`:

| Probe | Result |
| --- | --- |
| `pf -o - entry.md` | both links published with resolved destinations: `lib/steps.md#run`, `lib/steps.md#every-rule` |
| `pf -o - 'lib/steps.md#run'` | exit 0, fragment resolves to `#run` |
| `pf -o - 'lib/steps.md#every-rule'` | exit 0, fragment resolves to `#every-rule` |
| `pf -o - 'shared/my%20rules.md#run'` on the dispatch fixture tree | exit 0 — the percent escape is read back |
| `pf -o - entry.bundle.md` | `E_GENERATED_INPUT` at `entry.bundle.md:6` |

- **The guard fires after the content.**
  The entry line is emitted at the end of the bundle, so `entry.bundle.md:6` is where the declaration sits. A test must not assume line 1.

## Decisions

- **A pytest module, not a corpus extension.**
  The round-trip needs two invocations and a parse of the first's output between them. Extending `manifest.schema.json` with a `handoff` step would put that machinery into the corpus for one family; a module in `src/tests/` runs the installed command twice and binds this build, which is the right scope for a delivery test.

- **The destination is read from the first bundle, never from the manifest.**
  Restating the authoring string in the test would assert that the same string compiles twice. Parsing the published link is what makes the test a round-trip: it fails when emission writes a destination the build cannot resolve.

- **Synthetic trees, not corpus fixtures.**
  Each stack is written to `tmp_path` by the test, so no fixture directory is needed and the corpus's one-invocation rule is untouched. A directory holding no manifest is invisible to fixture discovery, which is why a corpus directory would add nothing.

- **Two operators, one mechanism.**
  `»` and `¬` publish the same destination rule, so one helper compiles either destination. The rows differ only in which operator wrote the link.

- **The guard is its own row.**
  `E_GENERATED_INPUT` is a different claim from a handoff: it states that a published bundle is refused as input. It gets its own test naming the line the declaration occupies.

## The Stacks

- **One synthetic tree per scenario**, each with `entry.md` and its targets under a working directory.
- **The dispatch stack** writes `[» the draft](lib/my%20steps.md#run)` — a path carrying an escape, so the test proves the escape is read back and not merely echoed.
- **The deferral stack** writes `[¬ the rules](lib/steps.md#every-rule)` and expects the destination's run to resolve the fragment.
- **The both-operators stack** writes one link of each, so a single bundle publishes two destinations and each compiles.
- **The fragment-only stack** defers a fragment of its own document, whose published destination names the document from the working directory.

## Checks

- **The second run's bundle is compared whole**, not by substring, so a wrong heading level or a dropped preamble fails.
- **The second run's exit status is zero**, and its diagnostics carry no error.
- **The guard test asserts the code and the line**, so a change that moves the entry line fails the fixture rather than passing silently.
- **The rows are named for the situation**, not the mechanism: a dispatched link's destination compiles, a deferred link's destination compiles, an escaped destination compiles, both destinations compile from one bundle, a fragment-only deferral compiles, and a published bundle is refused as input.
