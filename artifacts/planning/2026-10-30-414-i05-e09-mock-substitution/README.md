# I05:E09 Mock Substitution — October 2026

> Epic planning · Created 2026-10-30

## Executive Summary

This record holds the plan for I05:E09: a `-m ORIGINAL=ALTERNATIVE` invocation parameter that redirects the document a reference resolves to, so a bundle can be built and exercised against stand-in material without editing the tree under test. It is the ninth epic of I05, the standing initiative for ad hoc feature enhancements.

The epic is ten tasks. W00 states the design clause and moves the pin that lets a fixture name it, because `make conformance` reads the design at the revision `README.md` pins and refuses a declaration naming no clause it carries. W01 carries the mapping and the option together, because neither is observable without the other; W02 adds the three mapping refusals; W03 makes a redirected entry and referrer derive their own output name; W04 emits the two warnings; W05 redirects withheld and dispatched targets; W06 settles section keys and ends chaining; W07 treats the substitute as a source in its own right; W08 applies the mechanism to the example work-planner skill; the option's documented row lands with W01, where `make invocation` first requires it; and W10 refuses the fourth mapping shape the clause states, a value naming no Markdown document.

Each fixture lands in the pull request that makes it pass, so it is written against working behaviour rather than a prediction. Seventeen corpus fixtures under a new `fixtures/mock/` family, every one naming the clause W00 lands, and two example-skill scenarios the corpus cannot express.

Three rows were migrated here from [I05:E12](../2026-10-31-i05-inclusion-profiles-and-folders/epic-c-folder-mocks.md). A folder pairing is a shape of the same `-m` option this epic landed, so it belongs to the epic that owns the option rather than to a later epic that would reopen it. W11 carries the grammar, the precedence and the two refusals; W12 the absent substitute and the unused report; W13 the documented row and the example scenario. Five corpus fixtures and one check join the family, and the option's row is rewritten rather than added.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Epic body](epic.md) | The reviewed epic body, its criteria and its work-breakdown rows |
| [W00 work item](w00.md) | The design clause, the invocation rules and the pin |
| [W01 work item](w01.md) | The mapping at the resolution seam |
| [W02 work item](w02.md) | The option's grammar and refusals |
| [W03 work item](w03.md) | The derived name of a redirected entry and referrer |
| [W04 work item](w04.md) | The substitution warnings |
| [W05 work item](w05.md) | Withheld and dispatched targets |
| [W06 work item](w06.md) | Section keys and the end of chaining |
| [W07 work item](w07.md) | The substitute as a source in its own right |
| [W08 work item](w08.md) | The example skill bundled against stubs and a fake `gh` |
| [W10 work item](w12.md) | The fourth refused shape: a mapping value naming no Markdown document |
| [W11 work item](w09.md) | A folder pairing, its precedence and its refusals |
| [W12 work item](w12.md) | A folder key's absent substitute and its unused report |
| [W13 work item](w09.md) | The folder form documented and demonstrated |
| [Joins](joins.md) | The independent row pairs that take separate pull requests, and why |
| [Fixture inventory](fixtures.md) | Every fixture the epic lands, and the row that lands it |

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
| Reach | Positional entries, `-f`, and compiled, deferred, dispatched and parallel-dispatched targets alike, a reference its author's root admits and one it carries as a citation |
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
- **The mapping is specified on the command line, not in TOML or JSON.** A file format would be a second input language in a tool that reads only Markdown and its own frontmatter, needing its own parser and its own diagnostics. If a checked profile is ever needed, it arrives as a line list read by the existing value parser rather than as a structured document. (User, 2026-10-30.)
- **The mapping and the option are one row.** A mapping nothing can be passed is unobservable and an option with nowhere to put its pairs is unused, so W01 carries both and declares `closure.py` as its component with `cli.py` named in its body. The grain rule bends for a row that must be invocable. (User, 2026-10-30.)
- **The design clause merges to `engineering` before the pin moves.** Conformance reads the design at the pinned commit, so the amendment must exist before the pin can name it. The Open Question is settled. (User, 2026-10-30.)
- **Three capabilities already true by construction are stated and pinned.** A key may name a document that does not exist, a mapping value may carry a parent segment, and a mapping applies under `-c`. Each follows from where the seam sits, and a later refactor could remove it silently. (User, 2026-10-30.)
- **The example skill's scenarios are W08 of this epic.** The mechanism and its first consumer land together, so the mapping is proven against real material rather than only against purpose-built fixtures. (User, 2026-10-30.)

## Review

Six findings from a review against the source, all resolved.

| Finding | Severity | Resolution |
| --- | --- | --- |
| W01 placed the mapping "after normalization and before the Markdown-suffix test", which would have put it before `inside`'s `covers` check and refused every substitute outside the writing source's root — the case the feature exists for. | Critical | The mapping is applied to the reference `inside` returns, after `covers` is held against the authored path. |
| The epic claimed `inside` is "the one function every stage reaches resolution through". `entry` normalizes positional references and `-f` through `resolve` directly, so there are two paths. | High | Both the Problem and the Proposal state the two paths, and W01 owns both. |
| AC15 was cited by W02, a row whose design, implementation and test never mention `invocation.md`. | High | AC15 moved to W01, which lands the option row. |
| W01 and W06 both implemented the two-step lookup, and both claimed AC14. | Medium | W01 owns the lookup and AC14; W06 owns what a section key means and the fixture that makes precedence observable. |
| W01 extended both `closure.py` and `cli.py`, against the one-component rule. | Medium | Merged with W02 at the user's decision; AC14 moved to W06 to stay within the three-criterion grain. |
| The epic carried an Open Question, which planning requires resolved before work starts. | Medium | Settled: design first, then the pin. |
| W08's fixtures reached their stubs by `../stubs` from a `usage-example`-style symbolic link. `execute` takes `Path.cwd().resolve()`, so the value would have resolved to `example/stubs`, outside the fixture. | High | W08 holds a real copy of the example tree under `source/`, held to the original by `cmp` outside the corpus. |
| W08 claimed `cmp` over the tree shows it unchanged, but the run wrote its bundle into `cwd`, inside the skill directory, and `expected.absent` resolves against the fixture root rather than `cwd`. | Medium | Both example fixtures run `-o -`, so the run publishes nothing and no `absent` declaration is needed. |
| W08 named `artifacts/epic.md` as carrying "no criteria", which no part of it holds. | Low | The stub is described by the heading it replaces: `## Epic`, a member of the merged `artifacts` group at depth 1. |

Third pass, against the corpus mechanics and the criterion ownership the checkers cannot see.

| Finding | Severity | Resolution |
| --- | --- | --- |
| W08's corpus fixtures could not exist. A `usage-example` fixture's `source` is a symbolic link to the example tree so the corpus and the published example name one tree; `execute` resolves the working directory, so a parent-segment value lands beside the link's target; and `access.py` refuses a symbolic link in any traversed component. A copying fixture would work and reintroduces the drift the link prevents. | Critical | W08 is a check, not a corpus fixture: it copies `example/work-planner` into a temporary directory at run time, so one tree is maintained and nothing is checked in twice. `make mock-scenarios` runs it. |
| A fixture's `expected.absent` resolves against the fixture directory, and the runner invokes every fixture with `-o -`, so an `absent` declaration in this family asserts nothing. | Medium | Every `absent` claim removed from W02 and W04; the fact is stated once in `fixtures.md`. |
| The fragment-only key refusal was stated in W06's design and covered by no criterion. | Medium | AC23 added and moved to W02, which owns every mapping refusal. |
| W02 reached four criteria after AC23, and `format.py` refuses more than three. | Medium | AC15 split out to its own row, W09, because the documented row must follow the option it reproduces. |
| Renumbering left a duplicate W03 and a stale joins record, which `deps.py` reported only as unmatched pairs. | Medium | Table renumbered, work-item files renumbered, joins regenerated for the final numbering. |
| W01's fixture table lost `a-substitute-outside-the-writing-root-is-reachable` during an edit, leaving AC11 with no fixture. | Medium | Restored, and every fixture name cross-checked between the epic and the rows. |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Board | [Markdown Bundling](https://github.com/users/m2ux/projects/18) |
