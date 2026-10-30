# I05:E09 Mock Substitution — October 2026

> Epic planning · Created 2026-10-30

## Executive Summary

This record holds the plan for I05:E09: a `-m ORIGINAL=ALTERNATIVE` invocation parameter that redirects the document a reference resolves to, so a bundle can be built and exercised against stand-in material without editing the tree under test. It is the ninth epic of I05, the standing initiative for ad hoc feature enhancements.

The epic is seven tasks. W01 puts the mapping at the resolution seam and threads it through every helper; W02 adds the option and its refusals; W03 makes a redirected entry derive its own output name, W04 emits the two warnings and W05 redirects withheld and dispatched targets, which run in parallel from W02; W06 scopes a key to one section; and W07 states the behaviour in the bundling rules and the design. Every behaviour a source tree can produce is proven by an end-to-end corpus fixture.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Epic body](epic.md) | The reviewed epic body, its criteria and its work-breakdown rows |
| [W01 work item](w01.md) | The mapping at the resolution seam |
| [W02 work item](w02.md) | The option's grammar and refusals |
| [W03 work item](w03.md) | The derived name of a redirected entry |
| [W04 work item](w04.md) | The substitution warnings |
| [W05 work item](w05.md) | Withheld and dispatched targets |
| [W06 work item](w06.md) | Keys scoped to one section |
| [W07 work item](w07.md) | The bundling rules and the design clause |
| [Joins](joins.md) | The independent row pairs that take separate pull requests, and why |

## Design

### Resolution

Substitution sits inside `closure.inside`, the one function every stage reaches resolution through. The mapping is a parameter beside the `root` each call site already passes, so dependency discovery, emission's destination rewrite, candidate validation, the withheld-target check and entry normalization cannot disagree about what a reference names. Five modules reach resolution: `closure.py` owns the seam, and `cli.py`, `bundle.py` and `candidate.py` call it.

### Semantics

The substitute becomes the target outright. Its title, its `group` and `group-depth`, its `root` and its own links are the ones the run uses, and the bundle reads as if the author had written the substitute's path in the link. An overlay — keeping the original's identity and swapping only its bytes — was refused because it produces a document whose name and content come from different files and leaves `group` with two claimants.

### Confinement

A mapping entry is an invocation parameter rather than authored content, so both sides resolve from the invocation working directory and neither is bounded by the writing source's declared root. A fixture tree outside the root of the skill it exercises is the case the feature exists for. The reference grammar is unchanged: percent decoding, control-character refusal, `..` normalization, drive-path refusal, no-follow access and the Markdown-suffix test all still apply.

### The mapping

| Element | Rule |
| --- | --- |
| Form | `-m ORIGINAL=ALTERNATIVE`, repeatable |
| Matching | The identity a reference normalized to; an exact `(path, fragment)` key before `(path, None)` |
| Reach | Positional entries, `-f`, and compiled, deferred, dispatched and run-set references alike |
| Refused | Two keys normalizing to one identity; a key and value normalizing to one identity; a fragment-only key; a value naming no Markdown document |
| Chaining | None; a substitute's own links are matched against the mapping, and a substitute that is also a key is not followed again |

### Observability

A mocked bundle is otherwise the same kind of output as a real one, so the run states each substitution. `W_MOCK_SUBSTITUTED` names one redirected target's location, the identity it would have resolved to and the substitute; `W_MOCK_UNUSED` names a key that matched nothing. Both accompany a published bundle and exit `0`.

## Decisions

- **Redirect, not overlay.** The substitute becomes the target, identity and all. (User, 2026-10-30.)
- **A repeatable command-line option, not a mapping file and not frontmatter.** The mapping is an invocation parameter; frontmatter would put test scaffolding in the material under test. (User, 2026-10-30.)
- **`-m`, `--mock`.** (User, 2026-10-30.)
- **Entries are mockable as well as links.** (User, 2026-10-30.)
- **A redirected entry derives its output filename from the substitute.** The redirect is total. (User, 2026-10-30.)
- **Matching is on normalized identity.** (User, 2026-10-30.)
- **An unmatched key warns and does not fail.** (User, 2026-10-30.)
- **No chaining.** (User, 2026-10-30.)
- **A warning per redirected target, not a note in the bundle.** A note would need a heading, which is a destination in the bundle. (User, 2026-10-30.)
- **Every reference is redirected, withheld ones included.** (User, 2026-10-30.)
- **A key redirecting a document to itself is refused as invalid usage.** (User, 2026-10-30.)
- **An epic under I05, not a new initiative.** I05 exists to hold ad hoc enhancements, and this is one self-contained addition to link resolution. (User, 2026-10-30.)
- **Priority 5.** The epic has no prerequisite epic and no component contention, so it can start at any time; 5 places it behind the epics already in flight. (User, 2026-10-30.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
