# SOLID Compliance: What the Syntax Space Lets a Skill Designer Achieve

> Plan · Created 2026-10-25 · Build `pf 0.9.0 (skill-markdown-v1)` at `bd3b0665`

## Executive Summary

prosiform is a compiler for instruction sets written as linked Markdown. Its authoring surface is small: YAML frontmatter under a `prosiform` key, CommonMark links, two link operators (`¬` and `»`), and section fragments. That surface carries no module system, no interface declarations, no dependency direction rules and no type system. The question this report answers is which parts of SOLID a designer can actually reach through it, which parts they must reach around it, and which parts the syntax space cannot express at all.

The answer is uneven, and it is uneven in a specific pattern. **Everything SOLID asks for that reduces to "one stated thing in one place" is well served.** Section selection gives single responsibility an addressable unit; declared groups give open–closed an extension point; heading sets give Liskov substitution a checkable interface; the two link operators give interface segregation a real choice of what to carry; per-file `root` gives dependency inversion a source-owned policy. Each of those is demonstrated below with a run, and each runs clean.

**Everything SOLID asks for that needs a declared contract is absent.** There is no way to state that a consumer requires a heading set, no way to declare that a provider implements a role, and no way to forbid one document from reaching another. The tool validates what it compiles, not what an author promised. So the boundary is: prosiform checks *link integrity*, not *design intent*. A design that holds together does so because the author kept it together, and the compiler will bundle a design that does not.

Three findings carry more than the rest.

**Destination stability is weaker than a modular design expects, and it is weaker by construction.** A whole-document reference to a sole group member resolves to the merged heading; adding an unrelated second member to that group repoints the same reference to a variant heading naming the document ([LSP-6](evidence.log#lsp-6), [LSP-7](evidence.log#lsp-7)). This is not a bug: a bundle is generated in one pass and no link into one outlives that pass. But it means the substitutability a designer gets is *within* a run, never *across* runs, and any address a consumer stores is volatile.

**Two documents' same-named sections reach one destination.** Under a declared group, `plan.md#procedure` and `review.md#procedure` both rewrite to `#procedure`, a heading whose first subsection is the plan's content ([LSP-8](evidence.log#lsp-8)). The design states [the opposite](https://github.com/m2ux/prosiform/blob/bc91bf6dfb0c55f2538cd8bb88dbf81318b67a9e/artifacts/planning/2026-10-17-prosiform-v1/design.md), and the shipped fixture that cites the clause records the merged heading. This is recorded as [issue #269](https://github.com/m2ux/prosiform/issues/269); it is the one place below where observation and contract disagree.

**The substitutability that works is heading-level, and it stops at the heading.** A provider swapped for another with the same headings produces a byte-identical bundle except for its prose ([LSP-1](evidence.log#lsp-1)). A provider that retitles a heading fails at the consumer's line, with the chain ([LSP-2](evidence.log#lsp-2)). But nothing declares which headings a consumer needs, so a retitle fails only where some caller happens to link it, and an added heading can silently enter a shared bucket.

## Method

Every claim in this report is an observation of the build named above. The observations are not narrated; they are produced. `reproduce.sh` beside this file rebuilds a probe tree under `/tmp/solid-probe` and re-runs every command the report cites, recording stdout, stderr and the exit status of each. `evidence.log` is that run's output, and every citation below links to its section — [LSP-7](evidence.log#lsp-7) is the heading `### LSP-7` in that file.

The probe tree is a small skill: a router `SKILL.md`, five modes in group `modes`, two rule documents in group `rules`, one deferred artefact, and a policy file one directory above the source root. Four further trees isolate swapping, destination stability, pooling and direction.

Two baselines are recorded first. The build reports `pf 0.9.0 (skill-markdown-v1)`; `make corpus` over the shipped fixture corpus reports `260 fixture(s), 260 pass, 0 fail` ([/baseline-corpus](evidence.log#baseline-corpus)), so the build under observation is conformant to the contract the corpus encodes. Where this report says a behaviour is intended, that is the ground: the corpus holds it green.

One limitation of the method is stated plainly, because it bears on how far the evidence should be trusted. The probes were written by the same hand that reads the results, and eight of them initially checked something other than what their label claimed. Each was found by comparing the log against the label, corrected, and the whole log regenerated until every label matched its output.

| Probe | What the first version actually did | Correction |
| --- | --- | --- |
| SRP-3 | Named a heading and called it a bullet | Added a document whose bullets can be named, and tested a bullet's text |
| SRP-3b | Emitted a hardcoded sentence as if it were command output | Removed; the run in SRP-3 is the evidence |
| OCP-2 | Declared a group depth the group already had, so no conflict arose | Selected a second member of the other group |
| ISP-4 | Pointed at a file that did not exist, so nothing was tested | Created the source, then linked a missing target from it |
| X-5 | Passed `/dev/null` as the entry, which failed for an unrelated reason | Bundled a mode citing no rule |
| DIP-1a | Diffed a file the script had failed to write | Wrote the bundle from the directory it resolves from |
| LSP-4/5 | Claimed the filename enters the destination, which a fragment does not | Tested a whole-document reference, where it does |
| All | Recorded `$?` from `echo` after a pipe, or from `diff`/`grep` | Each entry records the tool that ran, labelled |

The log now records what ran, and the labels are checked against it. A reader is still right to read the log rather than the labels, and the reproduction script is the arbiter: re-running it either reproduces the log or does not.

## The syntax space

| Surface | What it states |
| --- | --- |
| `prosiform.root` | The dependency base and confinement directory for one source's outgoing links |
| `prosiform.group`, `group-depth` | The group this source joins and the heading level at which its sections merge |
| `prosiform.group-heading` | Whether the group's name is emitted as its H1 |
| `prosiform.dispatch` | One sentence stating what a `»`-marked link means for the skill |
| `[Text](doc.md#section)` | A compiled dependency: resolved, carried, rewritten to a bundle destination |
| `[¬ Text](doc.md)` | A deferral: target must exist, carried nowhere, mark removed |
| `[» Text](doc.md)` | A dispatch: target must exist, carried nowhere, mark published |
| `[Text](../../outside.md)` | A citation: emitted as authored, never opened |
| `pf REF`, `-f`, `-o`, `-c` | Entries, referrer for a bare fragment, destination, validate-only |

That is the whole authoring vocabulary. It has no construct for a required heading, an implemented role, a permitted dependency, a version, or a substitution assertion. Every SOLID verdict below follows from what the nine rows can and cannot say.

## S · Single responsibility

**What it takes to be a responsibility in this system.** One concern is one document, or one document-level heading and its subsections. That unit can be linked from anywhere and selected on its own, which is the property single responsibility needs and prose files normally lack.

- **Problem** a shared rule gets copied into every procedure, so one change needs several edits. **Solution** the rule is one section and every consumer links it.
  Selecting `modes/plan.md#outcomes` emitted the Outcomes list and nothing else from that document ([SRP-1](evidence.log#srp-1), exit 0).

- **Problem** a concern has no way to grow without widening its neighbours' context. **Solution** a sibling joins the group by declaration, and an existing bundle does not change.
  Adding `modes/refactor.md` to group `modes` left the plan-mode bundle byte-identical: `diff` produced no output ([SRP-2](evidence.log#srp-2)).

- **Problem** a rule file accumulates because splitting it means losing addressability. **Solution** a merged group pools same-named sections from several documents into one emitted section, so one concern can be split across files and still compile to one heading.
  Two documents contributing `## Style` produced one `## Style` with a subsection per document ([LSP-8](evidence.log#lsp-8)).

**Limitations.** The unit is a heading, and nothing smaller. A fragment naming a bullet's text resolves to nothing — `rules/bullets.md#prefer-plain-words` fails `E_TARGET_NOT_FOUND` ([SRP-3](evidence.log#srp-3), exit 1) — so a caller wanting one bullet of six takes the section ([SRP-4](evidence.log#srp-4)). A section also drags everything it links: `rules/common.md#wording` pulled in the sibling `agents.md` and its whole closure ([SRP-5](evidence.log#srp-5)). And cohesion is unchecked; a document with twenty unrelated H2s bundles cleanly.

## O · Open–closed

**What counts as extension here.** Adding a file. Group membership is a declaration, not a directory convention, so a new member needs no manifest edit, no router change and no registration step.

- **Problem** adding a mode normally means editing a router and every sibling. **Solution** the new mode declares the group and the existing documents are untouched.
  `modes/refactor.md` joined group `modes` and appeared in a combined bundle with no edit to any existing file ([OCP-1](evidence.log#ocp-1), exit 0).

- **Problem** the extension point is usually the filesystem layout, which then constrains where files live. **Solution** group identity is the declared string, independent of directories, so members merge across unrelated paths.
  The rule members live under `rules/`; the same declaration merges them with no path relationship required.

**Limitations.** Extension is open over content and closed over addresses. Two additions are refused outright rather than accommodated, and both force an edit to an existing file, which is exactly the case open–closed exists to avoid:

- A new member whose natural heading depth differs fails `E_GROUP_DEPTH_CONFLICT` naming both declarations and both locations ([OCP-2](evidence.log#ocp-2), exit 1). The new file must be re-shaped to the group's existing depth.
- A new member introducing its own `dispatch` wording fails `E_INVALID_CONVERSION_METADATA` naming both locations ([OCP-4](evidence.log#ocp-4), exit 1). Where only the newer member declares a text, that member's sentence silently becomes the bundle's rule ([OCP-3](evidence.log#ocp-3), exit 0) — the first source to declare wins, so the declaration is not additive.

A third limit is starker. Adding a second member to a group repoints a whole-document reference that previously resolved to the merged heading: `#rules` became `#a-rules` ([LSP-6](evidence.log#lsp-6) → [LSP-7](evidence.log#lsp-7)). Adding a file therefore changed the address of an existing one. Within one run the bundle is correct; across runs the address moved, so an addition is not address-preserving.

## L · Liskov substitution

**What the substitutability check is.** The heading set. A consumer names a fragment; the compiler resolves it against the provider's headings and fails at the consumer's own line if it is absent. That is a genuine behavioural check — stronger than nothing — and it is the only substitutability guarantee available.

- **Problem** substituting one provider for another silently breaks consumers. **Solution** the consumer's fragment is checked against the provider's headings at compile time.
  Two providers with the same `## Naming` / `## Length` headings and different prose produced bundles differing only in prose — `diff` reported the one content line ([LSP-1](evidence.log#lsp-1)).

- **Problem** a provider's location leaks into its consumers, so moving a file breaks them. **Solution** under a declared group the destination derives from the heading, not the path.
  Relocating `strict/rules.md` to `elsewhere/rules.md` inside group `rules` produced a byte-identical bundle: `diff` produced no output ([LSP-3](evidence.log#lsp-3)).

- **Problem** a provider dropping a heading must be caught rather than silently yielding a dangling link. **Solution** `E_TARGET_NOT_FOUND` names the reference, the provider, the consumer's line, the chain and a remedy.
  Retitling `## Naming` to `## House Naming` failed at `use-strict.md:7` with the full chain ([LSP-2](evidence.log#lsp-2), exit 1).

**Limitations.**

- **The check is one-directional.** Only a *removed or renamed* heading fails, and only where a caller links it. An *added* heading is absorbed silently into a shared bucket, and a provider missing a heading no caller names is never noticed. There is no statement of what a consumer requires, so the interface is inferred from use rather than declared.
- **Outside a group, a whole-document reference is named after the file path.** `/plain/style-guide.md` resolves to `#plainstyle-guide` and `/plain/other-name.md` to `#plainother-name` for identical bytes ([LSP-4](evidence.log#lsp-4), [LSP-5](evidence.log#lsp-5)). A file-named provider is substitutable only at the same path. A *fragment* reference is unaffected, because a source fragment resolves against the provider's own headings — `#naming` reached both ([LSP-5b](evidence.log#lsp-5b)). Substitutability therefore differs by reference shape: heading-level, and path-level for a whole document.
- **Destination stability is per-run only.** The `#rules` → `#a-rules` move above is the concrete case. A consumed address cannot be stored across runs.
- **The contract and the corpus disagree on grouping-depth references.** [LSP-8](evidence.log#lsp-8) observes `plan.md#procedure` and `review.md#procedure` both resolving to `#procedure`. The design clause says a grouping-depth reference resolves to the variant heading naming its document; the fixture citing that clause records the merged heading. Recorded as [issue #269](https://github.com/m2ux/prosiform/issues/269). Until that is settled, the substitutability of a pooled section cannot be stated confidently in either direction.

## I · Interface segregation

**What a consumer can refuse.** Two operators. A link can name material without carrying it, so a consumer's bundle holds the reference and not the payload, and the choice of harness-specific content is made by the source rather than forced on every run.

- **Problem** a consumer of one rule receives the whole rulebook, harness variants included. **Solution** `¬` carries the link's text, strips the mark and opens nothing.
  The Claude and Codex rules appeared as plain links and their content was absent from the bundle: `grep -c "^# Claude Rules"` returned `0` ([ISP-1](evidence.log#isp-1)). This is the example tree's own arrangement ([`rules/agents.md`](https://github.com/m2ux/prosiform/blob/bd3b06656d9d91a27fe1439daff2a189a938f39a/example/my-skill/rules/agents.md)).

- **Problem** a sub-agent's material must be announced without being compiled here. **Solution** `»` withholds identically but publishes its mark, because the mark is the only thing stating who compiles the slot.
  The dispatched link survived as `[» Record Delivery](artifacts/delivery.md)` and its section was absent (`grep -c` returned `0`) ([ISP-2](evidence.log#isp-2)).

- **Problem** the caller cannot see what it received without parsing prose. **Solution** the entry map goes to stderr as data while stdout is the bundle alone, so a wrapper reads destinations without scraping Markdown.
  `pf -o - modes/plan.md 2>/dev/null` emitted five sections and no diagnostic prose ([ISP-3](evidence.log#isp-3)).

- **Problem** a withheld slot becomes a dangling reference nobody notices. **Solution** a withheld target is still required to exist and to name the heading it names.
  A `»` or `¬` link to a missing document fails `E_TARGET_NOT_FOUND` with the chain ([ISP-4](evidence.log#isp-4), exit 1). A dispatch an agent will follow is one that can succeed.

**Limitations.**

- **No required interface can be declared.** Dependencies are the incidental consequence of prose links, so what a consumer depends on is discoverable only by reading it or by reading the bundle. There is no manifest, no `requires`, no capability statement.
- **No mandatory or optional distinction.** Everything linked is compiled unless an operator withholds it; withholding is the author's mark on one link, not a policy the compile enforces.
- **Selection is not minimal.** A section carries its subsections and every document it links, and structural ancestors travel with a partial selection. A consumer needing one rule still receives its section's links.
- **Segregation cannot be enforced from outside.** A consumer carries material it never names, reached through one it does: `modes/full.md` never mentions `agents.md`, yet the bundle carries `agents.md`'s content twice under variant headings ([ISP-5](evidence.log#isp-5)).

## D · Dependency inversion

**What is inverted.** Policy ownership. Structure — roots, groups, depths — comes only from the source's own frontmatter, never from the command line. The caller tunes capacity through budgets and picks entries; it cannot retarget where a document's links resolve or which group it joins.

- **Problem** the caller's working directory decides how a document's links resolve, so the same document behaves differently by invocation. **Solution** `prosiform.root` resolves from the declaring file's own directory.
  Over a closure of compiled links, compiling from the skill directory and from its parent produced byte-identical bundles: `diff` produced no output ([DIP-1a](evidence.log#dip-1a)). Over a closure holding withheld links, only those destinations move, because a withheld destination is deliberately cwd-relative so a later `pf` can be handed it ([DIP-1b](evidence.log#dip-1b)).

- **Problem** an invocation can reassign a document's structure. **Solution** `-r` and `-g` are refused as invalid usage, while operational flags remain the caller's.
  `pf -o - modes/plan.md -r .` and `-g other` each failed `E_INVALID_USAGE` at exit 2 ([DIP-2](evidence.log#dip-2), [DIP-3](evidence.log#dip-3)).

- **Problem** a consumer must name a concrete provider. **Solution** there is no first-class seam, but an indirection document is a working one: a `role.md` that links one provider gives every consumer a single file to repoint.
  Repointing `role.md` from `provider-one.md` to `provider-two.md` swapped the provider with no consumer edit ([DIP-4](evidence.log#dip-4) → [DIP-5](evidence.log#dip-5)).

**Limitations.**

- **Paths are concrete and the inversion is one layer deep.** `root` is a relative directory string, not a logical name. Swapping a provider means editing every consumer or maintaining the indirection document by hand, and the indirection layer is plain links with no declaration of what a role must provide.
- **No direction is enforced.** A provider linking back to its consumer pulled the consumer's entire closure into the bundle ([DIP-6](evidence.log#dip-6), exit 0). A layering rule is a review convention; the compiler has no notion of layers.
- **Structure and policy are the same mechanism.** Because `root` is both the base and the confinement boundary, there is no way to say "this document may read from over there but is not compiled from there" — a link outside the root is a citation and contributes nothing, which is a coarse binary rather than a policy.

## Where the syntax space runs out

These are not weaknesses of the implementation. They are constructs the authoring surface has no spelling for, at any cost.

| Want | Why it cannot be said |
| --- | --- |
| An interface a consumer requires | Nothing declares a heading set; the check is inferred from links |
| A role a provider implements | No type, tag or version on a document or a group |
| A forbidden dependency | No deny rule; any in-root link compiles, and a back-link drags the closure upward ([DIP-6](evidence.log#dip-6)) |
| A substitutability assertion | Swapping is a file edit; nothing records that two files are alternatives |
| A unit below a heading | Fragments resolve against headings only ([SRP-3](evidence.log#srp-3)) |
| Deduplication of identical content | Two paths hold two source identities and both emit ([X-1](evidence.log#x-1)) |
| A stable address across runs | Destinations are assigned and validated per run; the ordinal is safe only because no link outlives it |
| Any non-Markdown interface idiom | Raw HTML is refused ([X-3](evidence.log#x-3)); headings inside containers are not selectable ([X-4](evidence.log#x-4)) |
| Rebundling | A bundle is refused as input ([X-2](evidence.log#x-2)) |

Two further limits are worth separating from that table, because they are about what is *checked* rather than what is *sayable*.

**Completeness follows the links an author wrote.** A mode citing no shared rule at all bundles cleanly and exits 0 ([X-5](evidence.log#x-5)). That is the correct behaviour for a compiler — a missing link is not a missing file — and it is the reason single responsibility and interface segregation remain author discipline here rather than checked properties.

**Identical bytes at two paths are two sources.** `a.md` and `b.md` holding the same text are both emitted, under `# A` and `# B` ([X-1](evidence.log#x-1)). This is consistent with the provenance model, in which repeated prose in two regions is two ranges, and a count of occurrences is not a coverage test. It is not consistent with a reader's expectation of DRY, and there is no construct that expresses "these two are the same rule".

## Verdict

| Principle | Reachable | Checked | Verdict |
| --- | --- | --- | --- |
| Single responsibility | Yes — one heading is an addressable unit | No — cohesion is unenforced | **Well served** |
| Open–closed | Yes — declaration joins a group, no manifest | Partly — depth and dispatch conflicts are refused | **Served, with a fixed additive surface** |
| Liskov substitution | Yes — heading set is the interface | Partly — only removals, only where linked | **Served within a run, not across runs** |
| Interface segregation | Yes — `¬` and `»` withhold content | No — no declared interface | **Served for the author, not for the caller** |
| Dependency inversion | Yes — structure is source-owned | No — no direction, no logical names | **Served at one layer** |

Read across the row of **Checked**, the conclusion is narrow and useful: prosiform is a strong *link integrity* system and a silent *design integrity* one. A designer gets a modular authoring structure whose references are guaranteed to resolve, whose placement is deterministic, and whose dependencies are carried rather than fetched at read time. A designer does not get a compiler that notices a design drifting from its intent, and should not expect one; the guarantee the tool states is complete, validated bundling of the explicitly linked content, not control over how a skill is factored.

The practical consequence for a skill designer is that the structural disciplines need to be carried by review and by convention, and the two conventions that pay most are the ones the syntax space rewards: keep one concern to one document-level heading, and route every shared rule through a group declaration rather than a path. The first buys an addressable unit; the second buys a destination that survives relocation.

## Open Questions

- **Are grouped references supposed to reach the variant heading?** [Issue #269](https://github.com/m2ux/prosiform/issues/269) records the conflict between the clause and the fixture. Until it is settled, [LSP-8](evidence.log#lsp-8) is the behaviour and the clause is not.

- **Is destination volatility across members a defect or a stated limit?** Adding a member repoints an existing reference ([LSP-6](evidence.log#lsp-6) → [LSP-7](evidence.log#lsp-7)). The design's own reasoning — that no link into a bundle outlives the run — makes this correct, and makes any stored address wrong. Whether that deserves a stated limit in the contract's vocabulary, rather than a consequence a reader must derive, is not settled.

- **Should a consumer be able to claim a rule without compiling it?** The two operators let an author withhold. They do not let a caller refuse, so a bundle that carries a rule no caller wanted is indistinguishable from one that needed it.

- **Is the pooled-section bucket the right arrangement for a shared heading?** A section that several documents contribute to emits one heading with a subsection per document, so the shared heading is a container rather than a statement. Whether that reads as a rule or as a table of contents is a question about instruction comprehension that no test here observes.

## References

- **R1.** [Reproduction script](reproduce.sh) — rebuilds the probe trees and re-runs every observation.
- **R2.** [Evidence log](evidence.log) — the run, with each command's output and exit status.
- **R3.** [Grouping destinations](https://github.com/m2ux/prosiform/issues/269) — the clause and fixture that disagree on a pooled reference's destination.
- **R4.** [Invocation](https://github.com/m2ux/prosiform/blob/bd3b06656d9d91a27fe1439daff2a189a938f39a/invocation.md) — the frontmatter keys, the operators and the option set.
- **R5.** [Glossary](https://github.com/m2ux/prosiform/blob/bd3b06656d9d91a27fe1439daff2a189a938f39a/docs/glossary.md) — the definitions of deferral, dispatch, group and destination this report uses.
- **R6.** [Design](https://github.com/m2ux/prosiform/blob/bc91bf6dfb0c55f2538cd8bb88dbf81318b67a9e/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the grouping and destination clauses, and the guarantee the compiler states.
- **R7.** [The example skill](https://github.com/m2ux/prosiform/tree/bd3b06656d9d91a27fe1439daff2a189a938f39a/example/my-skill) — the deferred-harness arrangement cited under interface segregation.

## Anchor map

Each anchor below is a heading in [evidence.log](evidence.log); reading that section shows the run without the summary.

| Anchor | Observation |
| --- | --- |
| [#srp-1](evidence.log#srp-1) | One section selected, carried alone |
| [#srp-2](evidence.log#srp-2) | Unrelated sibling added, bundle unchanged |
| [#srp-3](evidence.log#srp-3) | A bullet's text is not a fragment target |
| [#srp-4](evidence.log#srp-4) | The section is the smallest unit |
| [#srp-5](evidence.log#srp-5) | A selected section drags its links |
| [#ocp-1](evidence.log#ocp-1) | A new mode joins by declaration |
| [#ocp-2](evidence.log#ocp-2) | A differing group depth is refused |
| [#ocp-3](evidence.log#ocp-3) | Sole dispatch declaration becomes the rule |
| [#ocp-4](evidence.log#ocp-4) | Two dispatch texts are refused |
| [#lsp-1](evidence.log#lsp-1) | Same headings, swapped providers, one line differs |
| [#lsp-2](evidence.log#lsp-2) | A retitled heading fails at the consumer |
| [#lsp-3](evidence.log#lsp-3) | Relocation inside a group keeps the destination |
| [#lsp-4](evidence.log#lsp-4) | Outside a group the filename is the heading |
| [#lsp-5](evidence.log#lsp-5) | Same bytes, other filename, other whole-document destination |
| [#lsp-5b](evidence.log#lsp-5b) | A fragment reference ignores the filename |
| [#lsp-6](evidence.log#lsp-6) | Sole member: reference resolves to the merged heading |
| [#lsp-7](evidence.log#lsp-7) | Second member added: same reference repoints |
| [#lsp-8](evidence.log#lsp-8) | Two same-named sections share one destination |
| [#isp-1](evidence.log#isp-1) | A deferral carries text and no content |
| [#isp-2](evidence.log#isp-2) | A dispatch withholds the target and keeps its mark |
| [#isp-3](evidence.log#isp-3) | stdout is the bundle; destinations are stderr data |
| [#isp-4](evidence.log#isp-4) | A withheld target must exist |
| [#isp-5](evidence.log#isp-5) | Content arrives that the consumer never named |
| [#dip-1a](evidence.log#dip-1a) | A compiled closure is cwd-independent |
| [#dip-1b](evidence.log#dip-1b) | Withheld destinations are cwd-relative by design |
| [#dip-2](evidence.log#dip-2) | `-r` is refused |
| [#dip-3](evidence.log#dip-3) | `-g` is refused |
| [#dip-4](evidence.log#dip-4) | An indirection document is the seam |
| [#dip-5](evidence.log#dip-5) | Repointing the seam swaps the provider |
| [#dip-6](evidence.log#dip-6) | A back-link drags the consumer's closure in |
| [#x-1](evidence.log#x-1) | Identical bytes at two paths emit twice |
| [#x-2](evidence.log#x-2) | A bundle is refused as input |
| [#x-3](evidence.log#x-3) | Raw HTML is refused |
| [#x-4](evidence.log#x-4) | A container heading is not selectable |
| [#x-5](evidence.log#x-5) | A mode citing no rule bundles cleanly |
| [#baseline-corpus](evidence.log#baseline-corpus) | The corpus the build is held to |
| [#baseline-build](evidence.log#baseline-build) | The build these observations are of |

Four observations are `diff` runs rather than `pf` runs — [SRP-2](evidence.log#srp-2), [LSP-1](evidence.log#lsp-1), [LSP-3](evidence.log#lsp-3) and [DIP-1a](evidence.log#dip-1a) — and three are `grep` runs — [ISP-1](evidence.log#isp-1), [ISP-2](evidence.log#isp-2) and [ISP-5](evidence.log#isp-5). Each records the exit status of the tool that ran, and the log labels it: for `diff`, `0` means the files agree; for `grep`, `1` means no line matched, which is the observation wherever the point is that a target contributed no headings. Neither is a compile result.
