# Decisions

The planning decisions taken with the user, each with the reasoning that produced it.

## D1 — The Python Build Is the Tool in Use

Python implements the full behavioural contract — closure, consolidation, destination identity, validation, diagnostics and CLI — produces a language-neutral fixture corpus of exact expected bundles, and ships as the tool agents in this workspace invoke. It is used for an extended period before a production build is committed to. Source-span edit fidelity is proven in Rust, where the production parser lives.

The design's hardest unproven element is the source-range adapter, which is parser-specific and would not transfer from a Python CommonMark parser to `pulldown-cmark`. Its hardest semantic elements — dependency closure to a fixed point, overlap consolidation, destination identity over the whole bundle and the post-compilation invariants — are parser-independent and provable cheaply.

A specification written before use is a hypothesis, and the cheapest place to discover what it got wrong is a build that already works. Using Python for that period means the design's errors are found and corrected at Python's cost rather than at Rust's, and it makes the corpus the durable artifact: what survives the period is a contract that real sources have exercised. The prototype is therefore a retained component, not a stopgap, and it stays in use as the differential oracle after the production build exists. See D7 for what ends that period.

## D2 — Gate Evaluation Precedes the Rust Build; Upstream Is a Separate Proposal

The Rust initiative opens with an epic that empirically proves or disproves both mandatory parser viability gates against a pinned `pulldown-cmark`, producing a written verdict. The upstream contribution is a non-goal of this proposal. A failed gate triggers a new proposal for the upstream route, raised only then.

The gates are mandatory before any bundle is published, so an unsatisfiable gate blocks the Rust initiative. The assessment concludes the current public API probably satisfies neither. Carrying the risk as a gate epic makes the blockage visible and dated without authorizing outbound action, which the design forbids. An upstream contribution depends on maintainer agreement, so it does not belong inside an initiative whose completion is otherwise controlled here.

## D3 — One Repository, Prototype Retained

`m2ux/prosiform` holds `fixtures/` (the language-neutral corpus and the contract it encodes), `prototype/` (the Python oracle, retained and maintained) and `rust/` (production prosiform). Both implementations run the same corpus in continuous integration. Each tree is created by the stage that writes into it: the corpus, prototype and documentation trees by the prototype initiative, the production tree by the production initiative.

The no-stopgap principle rules out a draft that a later version replaces. It does not rule out a second implementation that keeps proving the first. Retaining the oracle gives differential testing: a divergence between two independent implementations on the same input is a defect in one of them, which catches classes of error the fixtures did not anticipate.

## D4 — One Theme Board

A single prosiform theme board, copied from the Initiative template, holds both initiatives and their epics.

Two boards would split one product's queue and hide the dependency between the stages. One board shows the Rust initiative's readiness as gated on the prototype's corpus.

## D5 — Goal Clauses

Eight clauses, stated as outcomes someone could observe. G1 to G7 were confirmed when the proposal was raised; G8 follows from the decision to use the Python build for an extended period before committing to a production build, and is added to the proposal rather than left implicit.

- **G1.** Given a source root and one or more local document or section references, an agent receives one continuous Markdown document containing the selected content and every local Markdown dependency reachable from it.
- **G2.** Every internal reference in that document resolves to exactly one destination within it, and each included source region appears exactly once however many paths reach it.
- **G3.** Selected instruction wording and code examples are byte-identical to their sources apart from the transformations the declared profile names.
- **G4.** The original outline of each selected section survives: its ancestor headings are present, its relative depth is preserved, and each contributing file's content sits beneath one heading naming that file.
- **G5.** A run that cannot be fully validated emits no bundle and exits nonzero, with a diagnostic naming the defect, its source location, the offending reference and the inclusion chain that reached it.
- **G6.** Authors keep their existing modular files; nothing beyond ordinary Markdown links and headings is needed to bundle a document.
- **G7.** The contract is demonstrated by two independent implementations passing one shared fixture corpus.

- **G8.** The behavioural contract the production build implements has been exercised by real use and recorded as settled before that build begins.

The user declined two offered amendments: dropping G7 as a planning rather than product outcome, and adding the agent delivery contract as an eighth clause.

## D6 — The Prototype Parses With markdown-it-py

The Python build parses with `markdown-it-py`. `I00:E02:W02` configures it to the declared profile rather than selecting a parser.

The profile needs pipe tables, double-tilde strikethrough, source task-list markers preserved without checkbox generation, and typographic substitution disabled. `markdown-it-py` is CommonMark-compliant, supplies pipe tables and strikethrough as core rules enabled by name, preserves source task-list markers by leaving the task-list plugin out, holds typographic substitution off by default, and exposes a token stream whose structure is the closest Python analogue to `pulldown-cmark`'s event model. That similarity matters beyond convenience: profile reasoning that holds for one build reads across to the other, so a divergence between them is more likely a defect than a difference in how each parser frames the same document.

Block tokens carry line ranges and inline tokens do not, which bounds how precisely the prototype can locate an edit. That bound is acceptable here because byte-exact span editing is D1's explicit non-goal for this build; the prototype may reconstruct its output provided the corpus's preservation fixtures hold. A candidate parser is not excluded later: a fixture the prototype cannot satisfy for parser reasons is a reason to revisit this decision, recorded as one.

## D7 — The Specification Is Settled by Use Before Rust Is Committed To

The Python build is used for an extended period as the tool agents invoke, and what that use reveals refines the specification. That period is its own initiative between the prototype and the production build. It ends when every entry in a findings ledger is resolved or explicitly deferred with a reason, and the design and corpus carry one tagged revision; the production build names that revision as its target.

Two weaker end conditions were considered. A declared quiet span of active use measures stability directly, but a quiet span can mean the tool went unused rather than that the contract settled. Corpus coverage of every construct in this workspace's real sources ties the freeze to breadth of exposure, but says nothing about findings still open. The ledger condition is checkable by inspecting the ledger and the tag, and its deferral path stops one awkward finding holding the stage open indefinitely while still recording what was set aside.

The ordering within the stage is design, then corpus, then build. A fix applied to the build alone leaves the design asserting the original behaviour, and the next implementation reads the design; a fixture edited first turns an observed accident into the contract.

## D8 — The Production Initiative Is I02

The Rust initiative renumbers from I01 to I02, and the refinement stage takes I01, so the initiative numbers follow the order the stages run in. No pull request named any of those numbers, so the renumbering changed only issue titles and body references.

## D9 — The Repository Is Laid Out Before the First Task

The default branch holds a README whose body is `tbd` and no other file. A foundation epic opens the prototype initiative: the corpus, prototype and documentation trees D3 names, a Python environment whose dependencies resolve through a lockfile, documented commands for tests, lint, format and type checks, continuous integration running those same commands, and a README that states what the tool is and links to the design and the plan.

It is an epic rather than preparatory rows on the corpus harness because its subject is the repository, not the corpus, and because four of its five criteria bind every later epic rather than one.

No production infrastructure is created before the production initiative starts. Its tree, workspace, toolchain and dependencies are a first row of the adapter epic, so the Rust build neither inherits the prototype's environment by accident nor leaves an empty tree standing through the prototype and refinement stages. The prototype initiative carries a Non-Goal excluding that work.

The prototype's epics renumbered up by one to make room at E00, and the production adapter epic gained a W00 row. No pull request named any of those identifiers, so the renumbering changed only issue titles and body references.

The design and the planning record stay on the engineering branch. The repository's documentation tree links to them rather than copying them, so there is one copy of each.

## D10 — Three Corrections Taken From the Pre-Delivery Review

A review of the plan before any work started produced three corrections, each closing a hole rather than changing a decision.

**The freeze could pass on an unused tool.** Both conditions ending the refinement stage counted entries in the findings ledger, and an unused tool records none, so the stage held on its first day with the specification unexamined. The ledger now records every bundling run, not only surprises, and an exposure set names the real sources that must be bundled before a freeze. The freeze check refuses a tag until each of them carries a recorded run.

**Twelve error codes had no owner.** Every epic said the tool fails "with its declared error code" and nothing declared the catalogue, while the first failure fixture arrives four epics before diagnostics are built. The catalogue is now part of the fixture manifest schema in the corpus-harness epic, so a fixture naming a code outside it is rejected as malformed.

**The evidence behind the proposal is of the same order as the output budget.** The closure measured for the Problem is 318,018 bytes read whole against a default budget of 262,144. A fixture now bundles that closure and records its output size against the configured budget, so the default rests on a measurement, which is what the design asks for.

A fourth finding was withdrawn. It claimed the prototype could not keep its byte-preservation promise, because rewriting a link destination inside a selected section needs a character position its parser does not report. Computing a destination needs the target's identity, not the original's position, and the position matters only for splicing text into a copy of the original bytes. Of the four edits inside a selected section, three sit at line granularity the parser does report; for the fourth the parser supplies the destination, the count and the order of the links in the containing structure, so the occurrence is located by walking them rather than by pattern matching. The promise stands unchanged.

## D11 — Prerequisite Sections Go as Bundling Replaces Them

A skill's prerequisite section names whole documents, coarsely but completely. Bundling supplies the same context precisely, so those sections are removed rather than refactored, and no refactor is planned as work inside these initiatives.

Removal happens during the refinement stage, one skill at a time, and is gated: a section comes out only once a recorded bundling run supplies the sources it named. A source the section named and the bundling did not supply is a ledger entry, usually resolving to a missing inline link in the procedure that needed it.

The timing is what makes the gap catchable. Removing the lists before the stage would take away the coarse safety net before the tool had been shown to replace it; removing them after the freeze would refine and measure the tool against a structure that is going away.

This also reframes the measured evidence. The 318,018 bytes reached from one mode is largely the prerequisite sections pulling whole documents. It is the before-figure that bundling replaces, not a limit to design around.

The [worked example](worked-example.md) measures the split. Bundling Plan Mode without the prerequisite lists reaches 27 files rather than 39, which is 239,331 bytes read whole against 318,018; selecting sections within those 27 then bundles 187,488. So removal accounts for 78,687 bytes and bundling for 51,843. At this skill's granularity the retrieval argument rests on the completeness signal and the single resolved document, not on size.

## D12 — Each Run Is Measured Against Reading the Sources Whole

A run record carries the bundled output size and the total size of the same sources read whole. The refinement stage is not settled until each source in the exposure set has that pair recorded.

The proposal justified this work with a retrieval cost. Every criterion since has been about correctness, so without this the plan would never answer the question it was raised to answer. The measurement rides on a record that already exists for other reasons, so it costs one field and one criterion.

## D13 — Deployment Stays Behind the Validation Gate

Field deployment waits on the validation gate and runs in parallel with the conformance report. It is last in numbering, not in dependency.

Deploying five levels earlier, once destinations resolve, would start the refinement stage sooner. It would also put an unvalidated tool into use: no reparse of the finished bundle against what was selected, no boundary safety, no detection of a source that changed mid-run, and no diagnostics explaining a failure. Findings recorded then would mix genuine specification problems with defects the gate would have caught, which is the evidence the stage exists to produce.

## D14 — The Entry Point Says Bundle; Later the Harness Does It

An agent decides between reading a document and bundling it exactly once, on entry. Inside a bundle the question cannot arise: every supported local Markdown link has been rewritten to an internal destination, and a link that could not be rewritten failed the bundling.

That rules out marking individual links. It would also contradict the goal clause stating that nothing beyond ordinary Markdown links and headings is needed to bundle a document, and it would have to be maintained across every link in every skill. Inferring the choice from file names or paths is excluded for the same reason the design excludes inferring prerequisites from them.

So the mark belongs at the entry, and the question is who acts on it. In the first stage the skill's own text names the invocation, which needs nothing built and is the natural replacement for the prose that told the agent to read. In the second the skill declares itself ready to bundle and the harness bundles on load, so the choice stops being the agent's at all. Frontmatter suits that declaration: prosiform strips frontmatter, so the marker never reaches the output, and the generated-input rule already stops a bundle being bundled again.

The first stage runs during refinement, as each prerequisite section is removed. How reliably agents follow a written instruction is itself evidence, so the second stage is raised as its own proposal once there is use to draw on, rather than planned from an assumption about how well prose works.

## D15 — A Failed Bundling Stops the Work

A caller meeting a failed run halts and surfaces the diagnostic. Reading the sources instead is unsupported, and the documented invocation says so.

A fallback would restore the behaviour bundling replaces, and would restore it silently: the work would continue, nobody would notice, and the failure would produce no ledger entry. The refinement stage depends on failures being visible, so an invisible one costs more than a halt.

## D16 — Four Clauses the Plan Had Not Claimed

A second review mapped the design's sections against what the epics claim, and found three clauses with no owner and one the plan contradicted.

**An unsupported construct fails rather than becoming prose.** The profile work item planned a fixture asserting that an unsupported extension construct is left as ordinary text. The design says a recognized unsupported dependency or section-naming construct in selected content is rejected. Leaving a wiki link as text drops a dependency and reports nothing, which the completeness criterion forbids, so the build would have satisfied its epic while violating its initiative. The design is followed: a construct recognized as a dependency or section-naming extension fails, while prose that merely resembles one is left alone.

**Validation follows the selection, not the file.** A whole design section had no criterion. Indexing a source means parsing all of it, so the natural implementation validates all of it, and bundling one section of a large skill would fail on a broken link elsewhere in the same file. Two criteria now hold the boundary, and a file-wide parsing-safety failure is diagnosed as an inability to index that source rather than as a dependency on the construct that exceeded the limit.

**Encoding and suffix classification are stated.** A source is required to be valid UTF-8, and Markdown classification recognizes the two declared suffixes case-insensitively while failing an explicit entry carrying another.

**Determinism is promised, not merely tested.** A work item tested that differing argument orders produce one bundle; no criterion said so. Both the corpus comparison and the differential run between the two builds rest on it, so it is now a criterion and group order derives from source identity rather than from discovery order.

The conformance report would have caught all four, since it maps every design clause to its fixtures and lists the uncovered ones. It runs at the end of the prototype initiative, so the first of these would have surfaced after the profile had been built against the opposite rule.

## D17 — Destinations Are Hierarchy Paths, and the Output Is Markdown Only

The hierarchy path is superseded by [D23](#d23--a-destination-is-the-fragment-the-renderer-generates); the Markdown-only output stands.

Every outbound local link in a bundled document becomes a reference to content now inside that same document. The bundle is a transient artifact an agent reads whole: it is never published, and no renderer resolves its fragments. A destination therefore only has to name a place in a document the reader already holds.

A destination is the root-relative document path, then the source-heading slug of each eligible ancestor, then the section's own slug. Two destinations coincide only when the file, the ancestor chain and the slug all coincide, which means duplicate sibling headings. Those are refused as ambiguous.

That removes four things the earlier scheme needed. The digest goes, because uniqueness comes from the structure. The collision error goes with it. GitHub's duplicate numbering is not reproduced, because a counter ties a destination to how many similar headings precede it, so unrelated edits would silently repoint links; measured across this workspace, no document has repeated heading slugs and no link uses a numbered fragment. And the reserved prefix goes, because the path form is itself the marker that identifies the tool's own output.

The bundle carries Markdown and nothing else. No anchor elements are emitted, and raw HTML in selected content fails rather than being copied through, so the output holds no element or identifier the tool did not create. Hand-written anchors are no longer a supported way to name a section: a source heading is the only thing that does. Measured across this workspace's skills, no document contains any HTML, so nothing depended on the removed feature.

What this costs is clicking. A fragment of this form resolves in no renderer. That is not a loss for the consumer, which reads the document rather than navigating it.

## D18 — Expansion Depth Is a Budget, and a Structural Ancestor Does Not Satisfy a Reference

Bundling carries a declared expansion-depth budget, defaulting to eight link hops from the nearest entry reference along a target's shortest path. The design previously forbade any depth cap; that prohibition was aimed at a recursive-call limit leaking out as behaviour, which is a different thing from a budget chosen on purpose. Traversal stays iterative and a cyclic graph within the budget bundles normally.

Measured across four real entry points in this workspace, depth today runs from three to six hops. Eight sits above that with headroom and low enough to catch a runaway chain.

What the measurement also showed is what the budget does not do. Every one of those entry points reaches the same forty-three files: SKILL.md in three hops, plan-mode in six. The graph is dense, so depth governs the shape of a traversal and not its size. Size stays bounded by the file, byte and target budgets. The depth budget exists so a document reaches what governs it directly, and a chain that outgrows it is a prompt to restructure the sources rather than to raise the number.

Separately, a link whose target is present only as a heading-only ancestor now expands closure to include that section's selected body. A structural ancestor shows a title to preserve an outline; it is not content, and a reference to it was previously able to resolve to a heading with nothing beneath it while the bundle looked complete.

## D19 — A File Group Keeps Its Source Order

Selected regions and structural ancestors are emitted in the order they appear in their source. A document's preamble therefore sits after its filename heading and before its first retained heading, which needs no rule of its own.

This was raised first as a gap about preamble placement, which was the wrong framing: preamble position follows from source order, and the general rule was the thing no criterion covered. Without it, sections could be emitted in any order within a file group, which would break both outline reconstruction and the determinism the bundle promises.

## D20 — The Record Names Destinations, Not Anchors

A destination names a place in the bundle and the output carries no markup, so the record states both in those terms throughout. Three error codes are renamed to the things they now describe: an ambiguous fragment names a heading rather than an anchor, a reference that resolves to nothing names a target, and a document refused as input is a generated one with no reserved namespace left to name.

| Code | Raised when |
| --- | --- |
| `E_AMBIGUOUS_SOURCE_HEADING` | A fragment requires one of two sibling headings producing the same slug. |
| `E_TARGET_NOT_FOUND` | A supported local Markdown reference resolves to no document or section. |
| `E_GENERATED_INPUT` | A source's links carry bundle destinations. |

Goal clause G6 is restated for the same reason: authors needed nothing beyond ordinary Markdown links and headings before this change, and heading anchors named a feature that no longer exists. The clause is weaker in wording and identical in what it promises, because a hand-written anchor was never required to bundle a document and no document in this workspace carried one.

The design's status paragraph now names both builds. It previously said no implementation was authorized, which three planned initiatives have overtaken.

## D21 — A File Heading Carries a Path Without Its Extension, and Absorbs a Title It Duplicates

The file heading is the visible text of a file group and the first segment of every destination into it, so the two must be the same string: a reader following `artifacts/board/fields/themes` looks for a heading spelled `artifacts/board`. Both now drop the Markdown extension.

Dropping it means two documents whose paths differ only by that extension produce one file heading. They are refused with `E_AMBIGUOUS_FILE_GROUP`, which is the treatment duplicate sibling headings already get. The design previously kept the extension for exactly that case; refusing the ambiguity is the cheaper answer, and no document in this workspace has a twin under another Markdown extension.

The file heading also absorbs the source's first heading where that heading is the document's only H1 and slugifies to the final segment of the path. Measured across the work-planner skill, 37 of its 38 documents open with an H1 restating their own filename, so without absorption almost every file group opens with the same name twice and every destination into it carries the slug twice.

The one exception shows why the rule compares slugs rather than dropping every H1. `SKILL.md` opens with `# Work Planner`, a title the path does not carry, so it is kept and its group shifts as usual.

An absorbed group keeps its source heading levels, because the file heading has taken the level the plus-one shift was making room for. The shift is therefore a property of the group rather than of the bundle: plus one by default, zero where a title was absorbed. The alternative, shifting anyway, leaves each absorbed group opening on an H1 followed by an H3.

## D22 — A Destination Is Written as a Fragment

The hash stands; what follows it is settled by [D23](#d23--a-destination-is-the-fragment-the-renderer-generates).

A destination begins with `#`, so `#artifacts/architecture-overview/fields/template` rather than the bare path. Everything after the hash names a place inside this one document.

Written as a bare path, a destination is indistinguishable from a relative file reference, and an editor offered one tries to open a file that does not exist. The content it names is in the bundle, a few hundred lines away, which is the whole point of having bundled it.

A colon chain was considered for the ancestor segments. It leaves the file path looking like a path, and for a document at the source root it produces `guidelines:prose`, where a colon in the first segment is how a URI scheme is spelled and a renderer may read `guidelines:` as one. The leading hash has no such hazard, needs one character, and leaves the path and the slugs exactly as they were.

The generated-input rule cannot read off the destination, which D23 makes an ordinary fragment. It reads the file heading instead.

## D23 — A Destination Is the Fragment the Renderer Generates

A destination is the bundled heading's slug, carrying the ordinal a GitHub-compatible renderer appends when two bundled headings share one. So `#task-eligibility` where the slug is unique, `#fields-7` where it is the eighth heading to produce `fields`.

Measured against GitHub's own rendering of the worked example: it generates 353 anchors for the bundle's 353 headings, 272 bare and 81 numbered, and strips `/` from every slug it makes. That last fact is decisive. No destination containing a path separator can match an anchor, so the hierarchy path could not resolve anywhere, under any separator, while the path remained inside the fragment. The bundle published with renderer-generated destinations resolves all 774 of its fragment links against those anchors, with none broken.

This reverses the part of [D17](#d17--destinations-are-hierarchy-paths-and-the-output-is-markdown-only) that refused the renderer's counter. That refusal was sound about source documents, where an edit elsewhere changes how many similar headings precede a target and a stored link silently repoints. It does not carry to a bundle, which is generated whole in one pass, validated against the map that produced it, never hand-edited, and refused as input to a later run. No link to a bundle destination outlives the run that wrote it, so there is nothing for a later edit to repoint.

Two things are given up. A destination no longer says which file it points into, so an agent reads the link text rather than the href to know where it is going. And the generated-input policy loses its marker: a bundle's links are ordinary fragments now, so detection rests on the file heading alone, which is weaker and recorded as such.

Two things are gained beyond the links working. Scoping destinations to the bundle rather than to a file group means a section whose slug is unique needs no qualification at all, which is most of them. And the bundle stops carrying a naming scheme of its own: it is an ordinary Markdown document whose links happen to resolve.

## D24 — A Group Merges One Part of the Tree, and a Name Carries Variants Only Where It Collides

`--group SLUG:DEPTH`, repeatable, names a directory slug and a source heading level. Every document under any directory of that slug is merged at that level: `--group artifacts:2` puts every `Operations` section of every artifact document in one place, every `Fields` section in another. A document no group names keeps its own group, so one bundle carries both arrangements and the entry document is still read as itself.

This subsumes the bare grouping level that preceded it. Merging the whole bundle at a level is a group whose slug matches everything, so carrying both would be two parameters for one idea, and the narrower one could not express what the broader one already did.

The slug is what scopes the merge. A group emits one H1 carrying it, so two groups never blend: `artifacts` and `references` each hold their own `Operations`. Without that scope the parameter would only be a depth, and a depth cannot say which part of a tree is worth merging.

A merged heading keeps its source text. Where that text occurs once in its group there is nothing to disambiguate, and most do: bundling Plan Mode with `--group artifacts:2` leaves every one of the twenty-four merged operations bare. Where two or more documents contribute one text, it is emitted once and each document's content hangs beneath it under a variant heading naming that document, so the eight `Template` fields sit together under one `Template` rather than scattered under eight qualified names. Thirteen names carry variants this way, all of them in `Fields`.

A variant heading is the shortest run of that document's path which distinguishes it from the others, in title case, measured after dropping the leading segments they all share. In this group that is one segment, `Architecture Overview` against `Epic Issue Body`; across two libraries carrying one slug it would be the library name. Qualifying the heading text itself was tried first and discarded: it spelled the same distinction but left the variants apart, which is the comparison the merge exists to make.

This supersedes refusing the collision. Refusal was the right answer while every merged name was either unique or a conflict; minimal qualification is better because it distinguishes exactly the names that need it and leaves the rest alone, so the bundle does not acquire a naming scheme that applies to everything in order to handle a minority. What survives of the refusal is the case qualification cannot reach: two headings of one document colliding in one group, which the source heading rules already refuse.

Anything still coinciding takes the renderer's ordinal, as any repeat does. Eleven did, five of them generated group or merged-section headings matching a section name in an unmatched document.

Two things needed a home once a merged document stopped being contiguous. A group is headed by its directory slug in title case and carries an `Overview` section holding each member's preamble, as a subsection named by the document's stem less a trailing word the section already states: `artifacts/epic-issue-body.md` reads `Artifacts` / `Overview` / `Epic Issue Body`. The trimming is the rule the variant headings already follow, drop what the containing heading states, applied to a name rather than a path; under `Overview` nothing in this workspace matches, so names stay whole. Two earlier shapes were discarded: a `Sources` group above the groups, which invented a structural area, and a file heading per member inside one, which mixed paths in among section names. And a reference to a grouping-depth heading resolves to the merged group, losing which document it meant, which is the cost of merging.

Measured on the Plan Mode closure with `--group artifacts:2`: 8 top-level groups against 27, 13 names carrying variants, 302 destinations against 353, 38 ordinals against 81. All 421 references are rewritten under either arrangement, and GitHub's rendering of the three-group bundle resolves every one of its 728 fragment links against the 306 anchors it generates.

Only `work-planner` is broadly representative in this workspace, so the cross-library case the parameter is built for, two directories of one slug under separate libraries, is implemented but not yet exercised against real sources.

## D25 — The Routing Document Is Not Bundled, and Group Order Is Path Order

A skill's entry point is a routing table. The agent reads it, chooses a procedure, and passes that procedure's link to prosiform. The routing document is therefore never bundled, because it is never an entry reference: `SKILL.md` routes, `modes/plan-mode.md` is the argument, and the bundle holds the argument and what it reaches.

Groups are ordered by root-relative path, and nothing else. Neither discovery order nor argument order decides the arrangement, so one selection always bundles to the same bytes.

Emitting an entry reference's group last was tried and removed. The argument for it was salience: the thing the agent carries out sitting closest to the point of acting, with its material laid out above. Nothing rested on it. Order never decides whether a link resolves, only which heading takes the bare slug and which takes an ordinal, so every link resolves whatever the arrangement. No order can do better than that in any case, because the reference graph is cyclic — `epic-issue-body` to `epic` to `initiative-issue-body` and back, among three cycles — so between 31 and 61 of the Plan Mode closure's 194 cross-document references point forward whichever order is chosen. The delivery contract settles the rest: the agent holds the whole validated document before it acts.

So the rule bought two backward references out of 194 and cost a special case, a second special case to stop a group claiming the entry away from it, and a contradiction in the determinism criterion, which had promised that argument order does not change the bytes. Path order throughout restores all three.

## D26 — The Contract Is Stated Over Groups, and a Merged Reference Reaches Its Document

A group is the bundle's unit of arrangement: one source document by default, one merged directory under a grouping rule. Four clauses of the input and output contract and two post-compilation invariants describe that unit as a source file, which holds for a document-headed group and fails for a merged one. They are restated over groups, so one set of invariants holds under every arrangement: one H1 per group, each source belonging to exactly one group, source order kept within a group and within each contribution to a merged one, and the preserved outline beginning at the heading the grouping rules place.

A reference to a heading at the grouping depth resolves to the contributing document's variant heading, and to the merged heading itself where the name occurs once. The variant heading is already emitted and already names its document, so the reference reaches the document it meant. Resolving to the shared heading instead would make a grouped bundle answer a reference less precisely than an ungrouped one, which would make grouping a choice about fidelity rather than about arrangement.

Generated-input detection reads a bundle's opening file heading, which a merged group does not have: its heading is a directory slug in title case. A bundle whose every group is merged is therefore not detected, and the design says so rather than implying a guarantee it cannot keep. Nothing rests on the detection: an ordinal is safe because a bundle is generated whole in one pass and validated against the map that assigned it, not because a later run would refuse the bundle as input.

## D27 — A Grouping Rule Is Validated, and an Overview Holds Everything Above the Depth

Three things a grouping rule does were stated nowhere, and each one decides output.

A merged section can meet both variant tests at once: it carries body text from more than one document, and it also carries a name several documents contribute. The document-keyed test is applied first, and a section it splits is arranged by document throughout. The per-name rule then applies only to the names inside a section the first test leaves alone, so one section is never arranged two ways.

An `Overview` section holds each member's selected content above the grouping depth. The earlier wording said preamble, which the glossary defines as content above a document's first heading — and in this workspace that is almost always empty, because a document opens on its title and its lead text sits under it. Holding the preamble alone would drop that text, and a section shallower than the grouping depth would have nowhere to go at all. The overview subsection is named from the document's stem and absorbs the member's own H1 when their slugs agree, which is the file heading's absorption rule applied where there is no file heading.

A rule's own arguments are checked. A depth outside 1 through 6 names no heading level, a slug naming no directory under the root arranges nothing the user asked for, and one slug given twice states two arrangements for one set of documents; all three are refused with `E_INVALID_GROUP_RULE` and the invalid-usage exit status. A rule whose directories contribute no document to this particular closure is different: the rule is well formed and the closure simply does not reach it, so it warns and arranges nothing.

## D28 — The Bundle Opens by Naming What It Was Built For

A caller passes one reference and receives the whole closure. Path order decides where that reference's content sits, and a grouping rule distributes it across merged sections, so the document says nothing about which part answers the request. In the worked example the entry's group begins 75% of the way in.

The bundle therefore opens with a preamble of its own, naming each entry reference and linking to the destination it resolved to. It supplies three things.

It supplies the mapping, which the caller cannot compute. The caller sent `modes/plan-mode.md`; under `--group modes:2` that became `#plan-mode`, the name of an overview subsection derived from the document stem. The identity was already known; the destination was not.

It puts the reading rule where it is used. The design already says inclusion makes material available without authorizing the execution of every included procedure, but that sentence lives in a specification no agent reads. A bundle holding five modes' procedures leaves the agent to infer which one it was built for. The entry line states it in the document itself, and states nothing more: it carries no execution verb, because the tool does not know whether an entry names a procedure, and execution verbs belong to the authored instructions.

It survives the transport. The delivery contract guarantees the bundle arrives whole; it guarantees nothing about metadata carried beside it, which a transport may summarize or drop. A destination in the artifact is as reliable as the artifact. The run still reports each destination on the diagnostic stream, which is where a script or the corpus runner reads it as data rather than parsing prose.

The clean-Markdown rule is narrowed rather than set aside. It forbade generated commentary in the Markdown; it now admits this one line and forbids the rest, per-section envelopes included. The line is recorded with the group, file and variant headings as generated structure, so it counts toward no source's coverage.

The line is not used as a detection signal. An authored document may legitimately open with links into its own sections, so generated-input detection continues to rest on the file heading alone, with the limitation D26 records.

Whether naming the entry is enough, or whether an agent also needs its content positioned differently, is a question about agent behaviour that no reading of the design settles. It is taken up where it can be answered: each refinement-stage run records whether the entry's content was acted on from the bundle alone.

## D29 — A Scheme Means the Reference Is Not Ours, and a Resource Is Text

Six clauses decided one thing: whether a reference is a local Markdown dependency. They classified schemes, kept an allowlist, handled authorities, refused protocol-relative URLs, and left the exact scheme set as a residual item to be specified later.

One clause decides it. A reference is a dependency when it carries no scheme and no authority and resolves to a Markdown file under the root. Everything else is text the bundle carries unchanged, never opened and never interpreted. No scheme is permitted and none is refused, because which scheme a reference carries decides nothing: carrying one at all is what puts it outside the tool's interest.

That is stronger than the allowlist it replaces. The property the old clauses protected was that an unrecognized scheme must not be read as a filesystem path, and they protected it through a rejection path. Now a scheme is positive evidence that the reference is not local, so no path exists along which one could be opened. A schemeless reference the root cannot contain still fails, because that is a local document reference the run cannot satisfy, and refusing it keeps an intended dependency from being dropped in silence.

Resource rebasing goes with it. A relative image reference is text: emitted byte-identical, never rebased, with a warning that a bundle read elsewhere may not find it. Rebasing one means deciding where the bundle will be read from, which is the caller's question. The `--resource-base` option, its HTTPS directory validation, its conflict with a real output file, the file-output rebasing rules and their fixture family are all removed, and the tool holds no notion of a web address at all. The one rule worth keeping from that section stays on the option that owns it: an output path naming an input source is refused.

The tool bundles linked local Markdown. Nothing about a web address belonged in the contract that says so.

## D30 — Merge Discipline Is Convention Until the Repository Is Public

The repository is private on a plan that offers no branch protection: the API answers a protection request with an upgrade notice. The delivery procedure defines the base order and the merge order, every writer follows it, and that is where the guarantee comes from while the writer count is low. The first sign of a writer who does not follow it will be a surprising merge rather than a blocked push, which is worth knowing in advance.

The repository is to be made public later. Protection is enabled at that point, because it becomes available at no cost and the procedure stops being the only thing holding the shape: required pull requests on `main`, no force-push, no branch deletion. The condition is recorded here and tracked as an issue so it is acted on when the trigger arrives rather than remembered.

## D31 — The Root Is the Caller's Boundary and Must Contain the Closure

The root confines source access. It is the caller's safety boundary and says nothing about how the sources are organized, so it must contain every document the entry references reach.

This was settled by getting it wrong. The worked example bundled `modes/plan-mode.md` with the root at `skills/work-planner` and recorded ten link faults in the skill. Nine were not faults. `skills/guidelines.md` exists, carrying the three headings those links name, and work-planner's own guidelines and its revise mode both reference it deliberately. The links resolve exactly where their authors intended; the root excluded a dependency the skill genuinely has, and the refusals were read as defects.

A collection that shares material with a sibling is therefore rooted above both: `skills`, not `skills/work-planner`. The alternative, treating a cross-collection dependency as a defect to remove, would make the tool's confinement boundary dictate how a skill is authored, which is the wrong way round for a boundary whose purpose is to stop a run reading outside what the caller allowed.

A refused reference says the root is too narrow at least as often as it says the link is wrong. The diagnostic names the resolved path so the caller can tell the two apart, and that is the only thing the tool can say about it.

**D33 supersedes the rooting conclusion above.** The reasoning holds and the measurement holds: the boundary must not dictate how a skill is authored, and nine of those ten faults were the root's fault rather than the links'. What has changed is that a reference's shape is no longer what makes it a dependency. The links to the shared guidelines go unmarked, so they are citations, and a citation puts nothing outside the root. The skill is rooted at its own directory, nothing in it moves, and the boundary still dictates nothing — which is the outcome this decision wanted and could not reach while every mention was a requirement.

## D32 — The Mark Is Authoring Syntax and Does Not Reach the Bundle

A dependency's link text opens with `¬`. A rewritten link carries the text that followed the mark and not the mark itself.

The alternative was to preserve it. Visible link text is preserved everywhere else, and the preservation invariant lists link text among the bytes a bundling does not change, so carrying the mark through would have been the consistent reading of that rule.

It loses to what the mark is. The mark says *this reference is a requirement*, which is a statement to the compiler about the source, not content the author wrote for a reader. A marked link is rewritten in any case — its destination changes from a source path to a bundle destination — so the text is already being transformed at that point, and dropping the mark costs no additional pass. Carrying it would put a symbol in every bundled link that means nothing to the reader holding the bundle, where every reference has already been resolved and the distinction the mark drew no longer applies.

An unmarked link is emitted as authored and is not rewritten, so no mark can appear in one. The invariant therefore reads: a mark appears in a source and never in a bundle.

## D33 — A Skill Is Rooted at Its Own Directory, and a Citation Leaves It

A collection is rooted at its own directory. `skills/work-planner` is the root for bundling work-planner, and the shared material a skill cites from above that directory is not carried into the bundle.

D31 reached the opposite conclusion and was right to, under the rule in force: every local Markdown link was a dependency, so a citation of `skills/guidelines.md` put the closure above the skill, and the only way to keep the links where their authors wrote them was to widen the root. Widening works and costs something — a root at `skills` permits a run to read every sibling collection, which is a larger boundary than any one bundling needs, and it makes the portable unit the whole directory of skills rather than the skill.

The mark removes the choice between them. A citation is unmarked, so it carries no document and crosses no boundary; a requirement is marked, and an author who marks a reference above the root is told the root is too narrow for what they required. The root goes back to being the smallest boundary that contains what the run was asked to carry, which is what a confinement boundary should be.

Nineteen references across five documents in two collections cite the shared guidelines this way, and two further collections cite nothing above themselves. None of them changes: an unmarked link is what they already are.

## D34 — An Epic Is Cut Where Its Dependants Need It, and the Tool Ships Before the Gate Completes

A task row naming another epic's row waits for that epic to close, so where a cross-epic edge points decides how much work it imports. Three edges named an early row of their prerequisite and waited for the whole of it: the closure epic's traversal row named the second of seven outline rows, the destination epic's first row named the same, and its rewriting row named the fourth of eight closure rows. Under the previous rule the whole epic waited regardless and the cost was invisible.

Each prerequisite is therefore cut at the row its dependants name. Outline Hierarchy keeps the slug index, section extraction, the shift and file-group emission; structural ancestors, the depth ceiling and directory grouping leave it. Dependency Closure keeps normalization through budgets; the measured size and the example tree leave it. Candidate Validation keeps the one check that establishes a candidate carries its sources, and boundary safety, source consistency, diagnostics and validation scope become a separate gate. The departed rows form two epics that run after the tool is in use.

The alternative was to leave the epics whole and order them by priority. It was refused because priority orders epics and the gate is epic closure, so a tail row with no dependants would still hold the next epic shut. Merging the three epics into one was refused for the opposite reason: it removes every whole-epic wait but puts thirteen rows behind one integration base and one review.

The cost is two more epics, each carrying an integration base, a review pull request and a closure gate. It is paid once. The measured return is the longest chain falling from fourteen steps to thirteen, and the row that installs the tool moving from the eleventh step of that chain to the first.

## D35 — The Initiative Row Gates Only What Every Row Needs

An initiative row's Depends on cell stops an epic starting at all, while a task row's edge stops only that row. Naming a prerequisite on the initiative row where only some rows need it therefore holds back rows that are free, and the board shows an epic waiting on work none of its startable rows consumes.

A cell is written only where every task or joined unit of the dependent epic requires every task of the epic named. Candidate Validation qualifies, its one row naming the last row of Destination Identity. Outline and Closure Completion qualifies, because its rows are joined into one unit and that unit draws on both prerequisite epics. Field Deployment does not: packaging and a stable entry point need nothing from the validation gate, and the cell that named it held those rows behind seven others.

The alternative was to record the intended order as initiative edges, which reads naturally and is what the table looked like before. It was refused because an edge states a requirement and an order states a preference, and writing one as the other removes the board's ability to tell them apart. Order is carried by the priority label, which was made for it.

The measured return is the installation row becoming startable immediately rather than at the eleventh step, and Field Deployment entering the first priority set.

## D36 — Coverage Depth Follows the Ship, and the Corpus Names Its Own Gaps

The corpus is the contract, so a row that ships without the fixtures its criteria name would leave the contract asserting what nothing measures. The eight rows delivered so far carried forty fixtures, five per row and three and a third per criterion, of which sixteen state a nonzero exit. Carried at that depth, the rows before the tool reaches agents would author about eighty-five.

Each shipping row therefore authors the fixture that proves its behaviour and ticks its criterion, and declares its boundary, failure and adversarial cases as fixtures marked `awaiting` the conformance epic. A marked fixture tolerates failure and fails the job when it unexpectedly passes, so a deferral cannot outlive its reason, and the conformance epic gains a criterion that no marker survives it.

The alternative of writing the proving fixtures alone was refused for about one slot of saving: an undeclared case is one the conformance epic must rediscover from the design, and until it does, nothing distinguishes a clause that is covered from one that is not.

The modelled cost of the shipping slice falls from about fifteen row-equivalents to about eleven. The fixture counts are measured; the conversion to row-equivalents rests on fixture authoring being about half of a row, which the record does not establish.

## D37 — The Epic Order Is Chosen Where the Derivation Cannot See the Reason

The derived priority map ranks by prerequisite depth. It places Deferred Debt in the first set, because the rows deferred so far name only closed work, and it places Destination Identity there too, because no whole-epic edge holds it even though no row of it is free. Depth is not the whole of the reason an epic runs when it does.

The map is therefore set as Outline Hierarchy, Dependency Closure and Field Deployment at 7; Destination Identity at 6; Candidate Validation at 5; the Validation Gate at 4; Outline and Closure Completion at 3; Corpus Conformance at 2; Deferred Debt at 1. [D39](#d39--an-in-progress-epic-holds-the-bar-it-was-ranked-at) revises Field Deployment's place. The separation of the last two is [D38](#d38--a-priority-set-asserts-concurrency-and-the-components-decide-whether-it-holds)'s. Field Deployment joins the first set on the strength of one free row and finishes as the rest of the chain reaches it. Deferred Debt is last because its epic exists to be cleared after delivery, which no edge states.

The alternative was to encode the intended order as dependency edges so the derivation would produce it. It was refused for the reason recorded in [D35](#d35--the-initiative-row-gates-only-what-every-row-needs).

## D38 — A Priority Set Asserts Concurrency, and the Components Decide Whether It Holds

Epics sharing a priority number are Ready together, and since a task row is gated by what it names rather than by its epic, the members of one set run their internal sequences in parallel. That is an assertion about what can proceed at once, and prerequisite depth, which is all the derivation reads, cannot establish it. Two epics that extend one module are as independent as any other pair to a map built from edges.

Each remaining row is therefore read against the component its work item says it implements. Ten of the twenty-eight extend bundle assembly, spread across Outline Hierarchy, Destination Identity, the Validation Gate and Outline and Closure Completion. Six are the closure module, which is one epic's alone. Three are the source model, three the command surface, one the diagnostic stream, three the packaging and documentation.

Two epics of one set may not both hold rows that extend one component. The Validation Gate and Outline and Closure Completion shared a number and each opened on a bundle assembly row, so they are separated and the numbers above them move up by one. The command surface is written by rows of three epics, two of them in the first set; that contention is left standing, because those rows add independent options to a file rather than restructuring one, and the measure is the file while the conflict is the region.

The alternative was to cut epics by component rather than by behaviour. It was refused because the criteria state behaviour, and an epic whose rows share a module but no criterion cannot say what its closure establishes.

This was found by reading every work item by hand after the map had been applied to the tracker. Nothing in the plan, the dependency check or the board reported it, which is [m2ux/workflow-server#1461](https://github.com/m2ux/workflow-server/issues/1461).

## D39 — An In-Progress Epic Holds the Bar It Was Ranked At

An epic is Ready when it carries the highest priority number among the epics that can start **and those already running**: `top = max(rank over candidates + running)`. An epic In Progress therefore holds the bar at its own number for as long as it stays In Progress, and it stays there until its rows deliver.

Field Deployment was ranked into the first set so its packaging row could start immediately, which it did, delivering two rows. Its remaining rows need Destination Identity and Candidate Validation, so it cannot leave In Progress until they land — and while it sits there at the top number, Destination Identity beneath it can never become Ready. The map could not reach its own second step.

The order is therefore spread so that no epic shares a number and each sits where its remaining rows sit: Dependency Closure at 8, Destination Identity at 7, Candidate Validation at 6, Field Deployment at 5, the Validation Gate at 4, Outline and Closure Completion at 3, Corpus Conformance at 2, Deferred Debt at 1. Every handoff resolves: as each epic closes, the highest number among what can start exceeds the number any stalled epic holds.

The alternative was to rank an epic by its first row rather than by its last. That is what put Field Deployment at the top, and it bought a real early delivery. It is refused as a general rule because the number an epic carries is read while it runs, not only when it starts, and an epic whose first row is free and whose last row is deep will hold the bar high for the whole of its life.

This was found by reading `board-queue.py` after the queue offered one unit where two were expected. The board reported nothing: a deadlocked map and a correctly waiting epic look the same from outside.

## D40 — Marking a Resource Is an Authoring Error

A mark means bundle this. A resource — an image, a stylesheet, any reference that is not a local Markdown document — is never bundled, so marking one asks for something the tool will not do.

The contract said two things about it. [D32](#d32--the-mark-is-authoring-syntax-and-does-not-reach-the-bundle) holds that a mark appears in a source and never in a bundle; the design holds that a resource is emitted as authored. Together they publish `[¬ diagram](plan.png)` whole, mark included, and nothing ever removes it, because the mark is dropped by the rewrite and a resource is never rewritten.

A marked resource therefore fails with a code the catalogue declares. D32's invariant holds with no exception, and an author who marks a diagram learns at the run rather than finding authoring syntax in a published bundle.

The alternative was to emit it as authored and narrow D32 to say a mark survives on a reference nothing rewrites. It was refused because it retires the invariant to accommodate one case, and because a bundle carrying a mark offers its reader a signal that means nothing to them.

The cost is a new error code, which moves the design and the schema in one window across two branches. The refusal is therefore delivered by a row rather than written here: the clause and the catalogue entry land together, and the corpus states both the refusal and an unmarked resource bundling beside it. [I00:E04:W05](https://github.com/m2ux/prosiform/issues/6) carries it under AC17.

Until that row lands the corpus asserts neither outcome, which was [I00:E04:W03](https://github.com/m2ux/prosiform/pull/77)'s deliberate choice on finding the collision.

## D41 — One Code Names a Crossed Budget, and the Message Names Which

The contract declares eight resource budgets and holds that crossing one fails the compilation rather than truncating its output. It named no code for the failure, and the catalogue carried none, so the criterion stating the behaviour could not be delivered: a diagnostic reports a code, and there was none to report.

`E_RESOURCE_LIMIT` covers all eight. The diagnostic names the budget crossed and what it counted.

This follows `E_INVALID_USAGE`, which already covers every command line the grammar does not admit on the ground that one remedy serves them all. A crossed budget is the same shape: whichever it is, the sources need restructuring or the number needs raising, and the figure the run reports is what tells an author which.

The alternative of one code per budget was refused for the size it adds — eight catalogue entries and eight clauses — against eight remedies more alike than different. A split between the five size budgets and the two that constrain a graph's shape was refused because it invents a category no criterion names.

The cost is the one [#52](https://github.com/m2ux/prosiform/issues/52) already records: the corpus compares a diagnostic's severity, code, reference and source, never its message, so eight budgets behind one code are eight fixtures the corpus cannot tell apart. This decision widens that gap rather than creating it, and the row that closes #52 closes it for these too.

`E_PARSER_REFERENCE_LIMIT` is not this code and keeps its own meaning: an internal parser limit suppressing a reference lookup, which is a defect in indexing rather than a declared budget an author chose.

## D42 — A Marked Self-Reference Carries a Code of Its Own

The contract holds that a link from a section to that same canonical section is a compile error, and it named no code for the failure. Every failing outcome the contract names carries one, so the criterion stating the behaviour could not be delivered: a diagnostic reports a code, and there was none to report.

`E_SELF_REFERENCE` is that code. It names a marked reference whose target is the node that owns it — a section linking to itself, or a document's preamble linking to that whole document — and it is refused rather than resolved, because the mark asks the bundle to carry what the bundle is already carrying at that point.

It is not folded into `E_RESOURCE_LIMIT`'s one-code-for-eight shape, nor into `E_TARGET_NOT_FOUND`. The target exists and the reference resolves; what fails is the relationship between the reference and the node that wrote it, and the remedy is to drop the mark or name another node rather than to restore anything. A code naming a defect the author can act on is worth its entry, and `E_UNSUPPORTED_CONSTRUCT` would mislead: a self-link is grammatical Markdown the profile reads perfectly well.

The alternative of leaving the criterion undeliverable was refused for the same reason [D41](#d41--one-code-names-a-crossed-budget-and-the-message-names-which) refused it there: the contract states the behaviour, a row is delivering it, and the gap is one entry wide.

This was found by a delivery session measuring the build against the criterion rather than reading the plan, which had the catalogue ending at twenty-three. It ends at twenty-four, and the third clause lands in the same two-branch window as the other two.

## D43 — Conformance Counts an Unmapped Contract, Not a Tracked Defect

`I00:E10:AC6` asked that no fixture carry an `awaiting` marker when Corpus Conformance is measured. `I00:E11` is the deferred-debt epic and runs after every other epic in the initiative, so a fixture awaiting one of its rows still carries its marker at the moment E10 is measured. The criterion could not hold whatever the corpus looked like.

The criterion now excludes a marker naming `I00:E11`. A marker is a claim about what the corpus does not yet prove, and the two kinds differ: a marker naming a row still to come says the contract is mapped and the work is queued, while a marker naming the deferred-debt epic says a defect is known, placed and scheduled. Conformance is the assertion that the contract is mapped to the corpus, and a tracked defect does not contradict it.

The alternative of running `I00:E11` before `I00:E10` was refused: it puts the conformance gate behind every deferred defect, and the ordering exists so that a defect found late does not hold the gate open. Making the figure come out by marking a fixture `I00:E10` instead was also refused — a marker names the work that delivers the behaviour, and a marker pointing at the epic that merely measures it would be false where it matters most.

This was found by the session delivering `I00:E05:W02`, which declared a fixture against a defect it had just placed in `I00:E11` and reported the tension rather than choosing a marker that read better.

## D44 — A Cross-Epic Dependency Gates on the Epic, and the Row Names the Reason

A task row naming another epic's row waits for that epic. The initiative row states the gate, and the rows beside it move independently, so the finest grain the plan gates at is one epic.

Every `Depends on` cell naming another epic therefore links that epic and names the row in parentheses: `[E05](issues/7) (W02)`. The link is what gates and the parenthetical is why, which is the reading the cell already had and did not say.

The cells said `[E05:W02](issues/7)`, whose text promised a precision the link did not carry. A reader scheduling `I00:E07:W02` would have read it as waiting on one merged row and found it waiting on four.

Gating at the row was refused. A merged row is not a settled surface: a later row in the same epic revises what the earlier one delivered, and three contract changes landed in `I00:E05` after `W02` merged. An epic that closed has stopped moving, which is the property a dependant needs. The cost is a wave of wall-clock per dependent row, paid knowingly.

This was found by reading `I00:E07:W02` against the queue, which held it blocked on the epic while its cell named a row that had already merged.

## D45 — An Internal Error on Accepted Input Does Not Wait for the Deferred-Debt Epic

A link-reference definition whose destination or title the author spelled across two lines ends the run in `E_UNEXPECTED_INTERNAL_ERROR`. The input is valid CommonMark, the profile refuses nothing in it, and the contract states that a resolved reference is published inline with its title preserved.

It is delivered by [I00:E08](https://github.com/m2ux/prosiform/issues/59) as `W05` and `AC9`, and `I00:E11` carries neither a row nor a criterion for it.

The defect belongs to the reference conversion `I00:E05` delivered, and that epic is closed. No later epic owns reference handling, so placement was a choice between the validation gate and the deferred-debt epic. The validation gate takes it because its rows close the ways a bundle can be wrong that first use exposed, which is what this is.

Leaving it in the deferred-debt epic was refused on the severity rather than the subject. A wrong bundle is a bundle, and a caller who can see it can work around it; a run that publishes nothing and reports a fault in the tool leaves the caller nothing to act on and tells the author their correct document is not the problem. That class does not wait behind every other epic.

[D43](#d43--conformance-counts-an-unmapped-contract-not-a-tracked-defect) reads the fixture's marker, so the marker moves with the row: `fixtures/reference/a-definition-spelled-across-two-lines` awaits `I00:E08:W05` and states queued work rather than a tracked defect.

`W09` and `AC10` are absent from `I00:E11` rather than reused, and `W10` keeps its number. The two defects beside this one stay where they were placed: both publish a bundle, and both are wrong in it rather than instead of it.

## D46 — The Deferred-Debt Epic Ships in Waves

[I00:E11](https://github.com/m2ux/prosiform/issues/39) merges to `main` through a review pull request per wave of rows, rather than one for the epic. Every other epic keeps one review pull request, opened when its rows are complete.

The epic collects defects found while delivering the others, so its rows arrive over the whole initiative and have no dependency on each other. Holding them all for a single review at the end means a fix sits written and unmerged for as long as the initiative runs, which is the opposite of what a defect epic is for. A row whose absence costs a run on every branch — the link check's verdict was one — cannot wait for the epic it happens to belong to.

A wave is whatever rows are ready together. Each merges to `i00/e11/main` as a task pull request, and the base then opens a review pull request to `main` naming the rows it carries. The base survives the merge and takes the next wave.

Running the rows as standalone tasks against `main` was refused: the epic would stop having a reviewable surface, and a defect's fix would reach `main` without the epic's own gate ever running over the set.

The convention is this epic's rather than a general licence. An epic whose rows build on each other has a reason to review them together, and that reason is why the single review pull request exists.

This was decided after `I00:E11:W07` shipped ahead of its epic and spent the epic's only review pull request on one row.

## D47 — A Criterion Names the Evidence That Can Exist

`I00:E06:AC1` asked that a candidate disagreeing with its recorded source provenance publish nothing and fail, *as the validation fixtures show*. No such fixture can exist.

A corpus fixture declares a source tree, an invocation and the bytes published. A candidate disagreeing with its own provenance is not something a source tree produces against a build that works; only a broken build produces one. Writing the fixture would mean shipping a deliberate defect, or a mutation hook in the product that exists for the corpus to pull — and a hook that can make the compiler lie is a worse thing to carry than the fixture is a good one.

The criterion now names the unit cases for each invariant and the end-to-end run for the published outcome, which is the evidence that can exist. `I00:E10:AC8` already uses that phrasing for the same situation, an outcome no fixture can reach.

The corpus still carries six fixtures for this epic. They exercise each invariant on sources that validate, which is the half a fixture can state: that a correct bundle passes every check.

Leaving the wording and explaining the gap in the validation record was refused. `I00:E10` maps every behavioural clause to the fixtures that exercise it, so a criterion claiming fixture evidence that does not exist becomes an uncovered clause there, and the reasoning would be rediscovered by whoever meets it.

This was found while reviewing the delivery, which showed the criterion by other means and said so rather than reporting the fixtures the wording asked for.

## D48 — An Entry Destination Is a Warning, and the Row That Emits It Is Its Own

`I00:E07:AC6` asks that a successful run report each entry reference and the destination it resolved to on the diagnostic stream, in the declared format. The build computes those pairs already. Emitting them needs a diagnostic, and the catalogue has no entry for one.

The code is `W_ENTRY_DESTINATION`, a warning. A warning is the severity that accompanies a successful run, which is when this is reported, and it lands without touching the schema's severity enum or the test that holds each severity to a catalogue. The two-branch window between `fixtures/manifest.schema.json` and the contract on `engineering` is then one code wide.

A third severity was refused on cost rather than on fit. A notice is the honest name for data that is neither a failure nor a concern, and the existing warnings each flag something imperfect while an entry destination flags nothing. But it would take the schema's enum, a third catalogue, the harness test that pairs the two, and the contract on `engineering`, to carry a distinction no caller has asked for. The severity is read by the corpus and by a calling agent, and neither is misled by a record that says a run succeeded and names what it resolved.

Rewording the criterion to have the wrapper read destinations from the bundle's entry line was refused outright: the contract states that the entry line is what reaches the agent and the diagnostic stream is what a caller acts on as data, and the two are deliberately separate statements of the same thing.

The emission is unconditional on a successful run, so it changes what every successful fixture declares: **103 fixtures declare `exit_status = 0`, and 99 of those declare no diagnostics at all**. That is why it is `W05` rather than part of `W02`. The wrapper and the transport limit are one subject and the catalogue entry with its corpus-wide consequence is another, and a row that merges only when both are done holds the wrapper out of `main` behind a change to a hundred manifests.

`I00:E07:W02` therefore covers `AC2` and `AC3`, and `W05` covers `AC6`.

## D49 — An Image Is a Resource Whatever It Points At

The contract stated a marked resource two ways. One clause groups images with non-Markdown references and makes both text; the next fails a mark on "a reference that is not a local Markdown document", which keys on the target. For a marked image naming a Markdown file the two disagree: the target is a local Markdown document and the syntax is an image.

An image is a resource whatever it points at. Image syntax embeds rather than links, so a document named that way is no more bundleable than a picture is, and a mark asking for it asks for something no reading of the contract can supply. The clause now says so.

Keying the refusal on the target was refused because it leaves the case with no outcome. A marked image naming a Markdown file would be neither a resource to refuse nor a link to bundle, and the only remaining behaviour is to emit it as authored, which publishes the mark that [D32](#d32--the-mark-is-authoring-syntax-and-does-not-reach-the-bundle) forbids in a bundle.

This was found by the session delivering I00:E11:W08, which reported the widening against itself rather than leaving it for a reader to discover in the diff.

## Evidence

Measured on this workspace at commit `acac85867ca963df00251e4cf00a4db11b14bf24`, branch `workspace`:

| Measure | Value |
| --- | --- |
| Markdown files in the work-planner skill | 38 |
| Internal `.md` links among them | 519 |
| Of those, section-level fragment links | 363 |
| Files listed as Plan Mode prerequisites | 15 |
| Files in the transitive link closure of `modes/plan-mode.md` | 39 |
| Distinct section targets in that closure | 139 |
| Bytes if every file in that closure is read whole | 318,018 |
| Files across the workspace's skills carrying a `Read these files first` list | 25 |

The closure figures come from a traversal of `](…​.md[#fragment])` links from `skills/work-planner/modes/plan-mode.md`, following each target transitively.

### A Line Break Inside Heading Text

Measured against the GitHub renderer on branch `engineering`, two headings carrying the same words:

| Heading as written | Anchor generated |
| --- | --- |
| `Run the procedure` over `and then stop`, underlined | `run-the-procedureand-then-stop` |
| `## Run the procedure and then stop` | `run-the-procedure-and-then-stop` |

The renderer discards the line break and inserts nothing in its place, so a multiline Setext heading and the one-line heading of the same words take different anchors. The contract states this under `Source-heading resolution`, and `source.slug` already does it.

The question was raised while delivering I00:E03:W03, as an edge no slug-compatibility fixture carried: AC5 binds the source fragment to the renderer's, and no fixture had measured a multiline heading. The measurement closed it with no change to the build.
