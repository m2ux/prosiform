# Decisions

The planning decisions taken with the user, each with the reasoning that produced it.

## D1 — The Python Build Is the Tool in Use

Python implements the full behavioural contract — closure, consolidation, destination identity, validation, diagnostics and CLI — produces a language-neutral fixture corpus of exact expected composites, and ships as the tool agents in this workspace invoke. It is used for an extended period before a production build is committed to. Source-span edit fidelity is proven in Rust, where the production parser lives.

The design's hardest unproven element is the source-range adapter, which is parser-specific and would not transfer from a Python CommonMark parser to `pulldown-cmark`. Its hardest semantic elements — dependency closure to a fixed point, overlap consolidation, destination identity over the whole composite and the post-compilation invariants — are parser-independent and provable cheaply.

A specification written before use is a hypothesis, and the cheapest place to discover what it got wrong is a build that already works. Using Python for that period means the design's errors are found and corrected at Python's cost rather than at Rust's, and it makes the corpus the durable artifact: what survives the period is a contract that real sources have exercised. The prototype is therefore a retained component, not a stopgap, and it stays in use as the differential oracle after the production build exists. See D7 for what ends that period.

## D2 — Gate Evaluation Precedes the Rust Build; Upstream Is a Separate Proposal

The Rust initiative opens with an epic that empirically proves or disproves both mandatory parser viability gates against a pinned `pulldown-cmark`, producing a written verdict. The upstream contribution is a non-goal of this proposal. A failed gate triggers a new proposal for the upstream route, raised only then.

The gates are mandatory before any composite is published, so an unsatisfiable gate blocks the Rust initiative. The assessment concludes the current public API probably satisfies neither. Carrying the risk as a gate epic makes the blockage visible and dated without authorizing outbound action, which the design forbids. An upstream contribution depends on maintainer agreement, so it does not belong inside an initiative whose completion is otherwise controlled here.

## D3 — One Repository, Prototype Retained

`m2ux/md-composer` holds `fixtures/` (the language-neutral corpus and the contract it encodes), `prototype/` (the Python oracle, retained and maintained) and `rust/` (production md-compose). Both implementations run the same corpus in continuous integration. Each tree is created by the stage that writes into it: the corpus, prototype and documentation trees by the prototype initiative, the production tree by the production initiative.

The no-stopgap principle rules out a draft that a later version replaces. It does not rule out a second implementation that keeps proving the first. Retaining the oracle gives differential testing: a divergence between two independent implementations on the same input is a defect in one of them, which catches classes of error the fixtures did not anticipate.

## D4 — One Theme Board

A single md-compose theme board, copied from the Initiative template, holds both initiatives and their epics.

Two boards would split one product's queue and hide the dependency between the stages. One board shows the Rust initiative's readiness as gated on the prototype's corpus.

## D5 — Goal Clauses

Eight clauses, stated as outcomes someone could observe. G1 to G7 were confirmed when the proposal was raised; G8 follows from the decision to use the Python build for an extended period before committing to a production build, and is added to the proposal rather than left implicit.

- **G1.** Given a source root and one or more local document or section references, an agent receives one continuous Markdown document containing the selected content and every local Markdown dependency reachable from it.
- **G2.** Every internal reference in that document resolves to exactly one destination within it, and each included source region appears exactly once however many paths reach it.
- **G3.** Selected instruction wording and code examples are byte-identical to their sources apart from the transformations the declared profile names.
- **G4.** The original outline of each selected section survives: its ancestor headings are present, its relative depth is preserved, and each contributing file's content sits beneath one heading naming that file.
- **G5.** A composition that cannot be fully validated emits no composite and exits nonzero, with a diagnostic naming the defect, its source location, the offending reference and the inclusion chain that reached it.
- **G6.** Authors keep their existing modular files; nothing beyond ordinary Markdown links and headings makes a document composable.
- **G7.** The contract is demonstrated by two independent implementations passing one shared fixture corpus.

- **G8.** The behavioural contract the production build implements has been exercised by real use and recorded as settled before that build begins.

The user declined two offered amendments: dropping G7 as a planning rather than product outcome, and adding the agent delivery contract as an eighth clause.

## D6 — The Prototype Parses With markdown-it-py

The Python build parses with `markdown-it-py`. `I00:E01:W02` configures it to the declared profile rather than selecting a parser.

The profile needs pipe tables, double-tilde strikethrough, source task-list markers preserved without checkbox generation, and typographic substitution disabled. `markdown-it-py` is CommonMark-compliant, supplies the first three through option-controlled plugins and the fourth by leaving its typographer off, and exposes a token stream whose structure is the closest Python analogue to `pulldown-cmark`'s event model. That similarity matters beyond convenience: profile reasoning that holds for one build reads across to the other, so a divergence between them is more likely a defect than a difference in how each parser frames the same document.

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

**The freeze could pass on an unused tool.** Both conditions ending the refinement stage counted entries in the findings ledger, and an unused tool records none, so the stage held on its first day with the specification unexamined. The ledger now records every composition run, not only surprises, and an exposure set names the real sources that must be composed before a freeze. The freeze check refuses a tag until each of them carries a recorded run.

**Twelve error codes had no owner.** Every epic said the tool fails "with its declared error code" and nothing declared the catalogue, while the first failure fixture arrives four epics before diagnostics are built. The catalogue is now part of the fixture manifest schema in the corpus-harness epic, so a fixture naming a code outside it is rejected as malformed.

**The evidence behind the proposal is of the same order as the output budget.** The closure measured for the Problem is 318,018 bytes read whole against a default budget of 262,144. A fixture now composes that closure and records its output size against the configured budget, so the default rests on a measurement, which is what the design asks for.

A fourth finding was withdrawn. It claimed the prototype could not keep its byte-preservation promise, because rewriting a link destination inside a selected section needs a character position its parser does not report. Computing a destination needs the target's identity, not the original's position, and the position matters only for splicing text into a copy of the original bytes. Of the four edits inside a selected section, three sit at line granularity the parser does report; for the fourth the parser supplies the destination, the count and the order of the links in the containing structure, so the occurrence is located by walking them rather than by pattern matching. The promise stands unchanged.

## D11 — Prerequisite Sections Go as Composition Replaces Them

A skill's prerequisite section names whole documents, coarsely but completely. Composition supplies the same context precisely, so those sections are removed rather than refactored, and no refactor is planned as work inside these initiatives.

Removal happens during the refinement stage, one skill at a time, and is gated: a section comes out only once a recorded composition run supplies the sources it named. A source the section named and the composition did not supply is a ledger entry, usually resolving to a missing inline link in the procedure that needed it.

The timing is what makes the gap catchable. Removing the lists before the stage would take away the coarse safety net before the tool had been shown to replace it; removing them after the freeze would refine and measure the tool against a structure that is going away.

This also reframes the measured evidence. The 318,018 bytes reached from one mode is largely the prerequisite sections pulling whole documents. It is the before-figure that composition replaces, not a limit to design around.

The [worked example](worked-example.md) measures the split. Composing Plan Mode without the prerequisite lists reaches 27 files rather than 39, which is 239,331 bytes read whole against 318,018; selecting sections within those 27 then composes 187,488. So removal accounts for 78,687 bytes and composition for 51,843. At this skill's granularity the retrieval argument rests on the completeness signal and the single resolved document, not on size.

## D12 — Each Run Is Measured Against Reading the Sources Whole

A run record carries the composed output size and the total size of the same sources read whole. The refinement stage is not settled until each source in the exposure set has that pair recorded.

The proposal justified this work with a retrieval cost. Every criterion since has been about correctness, so without this the plan would never answer the question it was raised to answer. The measurement rides on a record that already exists for other reasons, so it costs one field and one criterion.

## D13 — Deployment Stays Behind the Validation Gate

Field deployment waits on the validation gate and runs in parallel with the conformance report. It is last in numbering, not in dependency.

Deploying five levels earlier, once destinations resolve, would start the refinement stage sooner. It would also put an unvalidated tool into use: no reparse of the finished composite against what was selected, no boundary safety, no detection of a source that changed mid-run, and no diagnostics explaining a failure. Findings recorded then would mix genuine specification problems with defects the gate would have caught, which is the evidence the stage exists to produce.

## D14 — The Entry Point Says Compose; Later the Harness Does It

An agent decides between reading a document and composing it exactly once, on entry. Inside a composite the question cannot arise: every supported local Markdown link has been rewritten to an internal destination, and a link that could not be rewritten failed the composition.

That rules out marking individual links. It would also contradict the goal clause stating that nothing beyond ordinary Markdown links and headings makes a document composable, and it would have to be maintained across every link in every skill. Inferring the choice from file names or paths is excluded for the same reason the design excludes inferring prerequisites from them.

So the mark belongs at the entry, and the question is who acts on it. In the first stage the skill's own text names the invocation, which needs nothing built and is the natural replacement for the prose that told the agent to read. In the second the skill declares itself composable and the harness composes on load, so the choice stops being the agent's at all. Frontmatter suits that declaration: md-compose strips frontmatter, so the marker never reaches the output, and the generated-input rule already stops a composite being composed again.

The first stage runs during refinement, as each prerequisite section is removed. How reliably agents follow a written instruction is itself evidence, so the second stage is raised as its own proposal once there is use to draw on, rather than planned from an assumption about how well prose works.

## D15 — A Failed Composition Stops the Work

A caller meeting a failed composition halts and surfaces the diagnostic. Reading the sources instead is unsupported, and the documented invocation says so.

A fallback would restore the behaviour composition replaces, and would restore it silently: the work would continue, nobody would notice, and the failure would produce no ledger entry. The refinement stage depends on failures being visible, so an invisible one costs more than a halt.

## D16 — Four Clauses the Plan Had Not Claimed

A second review mapped the design's sections against what the epics claim, and found three clauses with no owner and one the plan contradicted.

**An unsupported construct fails rather than becoming prose.** The profile work item planned a fixture asserting that an unsupported extension construct is left as ordinary text. The design says a recognized unsupported dependency or section-naming construct in selected content is rejected. Leaving a wiki link as text drops a dependency and reports nothing, which the completeness criterion forbids, so the build would have satisfied its epic while violating its initiative. The design is followed: a construct recognized as a dependency or section-naming extension fails, while prose that merely resembles one is left alone.

**Validation follows the selection, not the file.** A whole design section had no criterion. Indexing a source means parsing all of it, so the natural implementation validates all of it, and composing one section of a large skill would fail on a broken link elsewhere in the same file. Two criteria now hold the boundary, and a file-wide parsing-safety failure is diagnosed as an inability to index that source rather than as a dependency on the construct that exceeded the limit.

**Encoding and suffix classification are stated.** A source is required to be valid UTF-8, and Markdown classification recognizes the two declared suffixes case-insensitively while failing an explicit entry carrying another.

**Determinism is promised, not merely tested.** A work item tested that differing argument orders produce one composite; no criterion said so. Both the corpus comparison and the differential run between the two builds rest on it, so it is now a criterion and group order derives from source identity rather than from discovery order.

The conformance report would have caught all four, since it maps every design clause to its fixtures and lists the uncovered ones. It runs at the end of the prototype initiative, so the first of these would have surfaced after the profile had been built against the opposite rule.

## D17 — Destinations Are Hierarchy Paths, and the Output Is Markdown Only

The hierarchy path is superseded by [D23](#d23--a-destination-is-the-fragment-the-renderer-generates); the Markdown-only output stands.

Every outbound local link in a composed document becomes a reference to content now inside that same document. The composite is a transient artifact an agent reads whole: it is never published, and no renderer resolves its fragments. A destination therefore only has to name a place in a document the reader already holds.

A destination is the root-relative document path, then the source-heading slug of each eligible ancestor, then the section's own slug. Two destinations coincide only when the file, the ancestor chain and the slug all coincide, which means duplicate sibling headings. Those are refused as ambiguous.

That removes four things the earlier scheme needed. The digest goes, because uniqueness comes from the structure. The collision error goes with it. GitHub's duplicate numbering is not reproduced, because a counter ties a destination to how many similar headings precede it, so unrelated edits would silently repoint links; measured across this workspace, no document has repeated heading slugs and no link uses a numbered fragment. And the reserved prefix goes, because the path form is itself the marker that identifies the tool's own output.

The composite carries Markdown and nothing else. No anchor elements are emitted, and raw HTML in selected content fails rather than being copied through, so the output holds no element or identifier the compositor did not create. Hand-written anchors are no longer a supported way to name a section: a source heading is the only thing that does. Measured across this workspace's skills, no document contains any HTML, so nothing depended on the removed feature.

What this costs is clicking. A fragment of this form resolves in no renderer. That is not a loss for the consumer, which reads the document rather than navigating it.

## D18 — Expansion Depth Is a Budget, and a Scaffold Does Not Satisfy a Reference

Composition carries a declared expansion-depth budget, defaulting to eight link hops from the nearest entry reference along a target's shortest path. The design previously forbade any depth cap; that prohibition was aimed at a recursive-call limit leaking out as behaviour, which is a different thing from a budget chosen on purpose. Traversal stays iterative and a cyclic graph within the budget composes normally.

Measured across four real entry points in this workspace, depth today runs from three to six hops. Eight sits above that with headroom and low enough to catch a runaway chain.

What the measurement also showed is what the budget does not do. Every one of those entry points reaches the same forty-three files: SKILL.md in three hops, plan-mode in six. The graph is dense, so depth governs the shape of a traversal and not its size. Size stays bounded by the file, byte and target budgets. The depth budget exists so a document reaches what governs it directly, and a chain that outgrows it is a prompt to restructure the sources rather than to raise the number.

Separately, a link whose target is present only as a heading-only ancestor now expands closure to include that section's selected body. A scaffold shows a title to preserve an outline; it is not content, and a reference to it was previously able to resolve to a heading with nothing beneath it while the composite looked complete.

## D19 — A File Group Keeps Its Source Order

Selected regions and structural ancestors are emitted in the order they appear in their source. A document's preamble therefore sits after its filename heading and before its first retained heading, which needs no rule of its own.

This was raised first as a gap about preamble placement, which was the wrong framing: preamble position follows from source order, and the general rule was the thing no criterion covered. Without it, sections could be emitted in any order within a file group, which would break both outline reconstruction and the determinism the composite promises.

## D20 — The Record Names Destinations, Not Anchors

A destination names a place in the composite and the output carries no markup, so the record states both in those terms throughout. Three error codes are renamed to the things they now describe: an ambiguous fragment names a heading rather than an anchor, a reference that resolves to nothing names a target, and a document refused as input is a generated one with no reserved namespace left to name.

| Code | Raised when |
| --- | --- |
| `E_AMBIGUOUS_SOURCE_HEADING` | A fragment requires one of two sibling headings producing the same slug. |
| `E_TARGET_NOT_FOUND` | A supported local Markdown reference resolves to no document or section. |
| `E_GENERATED_INPUT` | A source's links carry composite destinations. |

Goal clause G6 is restated for the same reason: authors needed nothing beyond ordinary Markdown links and headings before this change, and heading anchors named a feature that no longer exists. The clause is weaker in wording and identical in what it promises, because a hand-written anchor was never required to make a document composable and no document in this workspace carried one.

The design's status paragraph now names both builds. It previously said no implementation was authorized, which three planned initiatives have overtaken.

## D21 — A File Heading Carries a Path Without Its Extension, and Absorbs a Title It Duplicates

The file heading is the visible text of a file group and the first segment of every destination into it, so the two must be the same string: a reader following `artifacts/board/fields/themes` looks for a heading spelled `artifacts/board`. Both now drop the Markdown extension.

Dropping it means two documents whose paths differ only by that extension produce one file heading. They are refused with `E_AMBIGUOUS_FILE_GROUP`, which is the treatment duplicate sibling headings already get. The design previously kept the extension for exactly that case; refusing the ambiguity is the cheaper answer, and no document in this workspace has a twin under another Markdown extension.

The file heading also absorbs the source's first heading where that heading is the document's only H1 and slugifies to the final segment of the path. Measured across the work-planner skill, 37 of its 38 documents open with an H1 restating their own filename, so without absorption almost every file group opens with the same name twice and every destination into it carries the slug twice.

The one exception shows why the rule compares slugs rather than dropping every H1. `SKILL.md` opens with `# Work Planner`, a title the path does not carry, so it is kept and its group shifts as usual.

An absorbed group keeps its source heading levels, because the file heading has taken the level the plus-one shift was making room for. The shift is therefore a property of the group rather than of the composite: plus one by default, zero where a title was absorbed. The alternative, shifting anyway, leaves each absorbed group opening on an H1 followed by an H3.

## D22 — A Destination Is Written as a Fragment

The hash stands; what follows it is settled by [D23](#d23--a-destination-is-the-fragment-the-renderer-generates).

A destination begins with `#`, so `#artifacts/architecture-overview/fields/template` rather than the bare path. Everything after the hash names a place inside this one document.

Written as a bare path, a destination is indistinguishable from a relative file reference, and an editor offered one tries to open a file that does not exist. The content it names is in the composite, a few hundred lines away, which is the whole point of having composed it.

A colon chain was considered for the ancestor segments. It leaves the file path looking like a path, and for a document at the source root it produces `guidelines:prose`, where a colon in the first segment is how a URI scheme is spelled and a renderer may read `guidelines:` as one. The leading hash has no such hazard, needs one character, and leaves the path and the slugs exactly as they were.

The generated-input rule cannot read off the destination, which D23 makes an ordinary fragment. It reads the file heading instead.

## D23 — A Destination Is the Fragment the Renderer Generates

A destination is the composed heading's slug, carrying the ordinal a GitHub-compatible renderer appends when two composed headings share one. So `#task-eligibility` where the slug is unique, `#fields-7` where it is the eighth heading to produce `fields`.

Measured against GitHub's own rendering of the worked example: it generates 353 anchors for the composite's 353 headings, 272 bare and 81 numbered, and strips `/` from every slug it makes. That last fact is decisive. No destination containing a path separator can match an anchor, so the hierarchy path could not resolve anywhere, under any separator, while the path remained inside the fragment. The composite published with renderer-generated destinations resolves all 774 of its fragment links against those anchors, with none broken.

This reverses the part of [D17](#d17--destinations-are-hierarchy-paths-and-the-output-is-markdown-only) that refused the renderer's counter. That refusal was sound about source documents, where an edit elsewhere changes how many similar headings precede a target and a stored link silently repoints. It does not carry to a composite, which is generated whole in one pass, validated against the map that produced it, never hand-edited, and refused as input to a later run. No link to a composite destination outlives the run that wrote it, so there is nothing for a later edit to repoint.

Two things are given up. A destination no longer says which file it points into, so an agent reads the link text rather than the href to know where it is going. And the generated-input policy loses its marker: a composite's links are ordinary fragments now, so detection rests on the file heading alone, which is weaker and recorded as such.

Two things are gained beyond the links working. Scoping destinations to the composite rather than to a file group means a section whose slug is unique needs no qualification at all, which is most of them. And the composite stops carrying a naming scheme of its own: it is an ordinary Markdown document whose links happen to resolve.

## D24 — A Cohort Merges One Part of the Tree, and a Name Is Qualified Only Where It Collides

`--group SLUG:DEPTH`, repeatable, names a directory slug and a source heading level. Every document under any directory of that slug is merged at that level: `--group artifacts:2` puts every `Operations` section of every artifact document in one place, every `Fields` section in another. A document no cohort names keeps its own group, so one composite carries both arrangements and the entry document is still read as itself.

This subsumes the bare grouping level that preceded it. Merging the whole composite at a level is a cohort whose slug matches everything, so carrying both would be two parameters for one idea, and the narrower one could not express what the broader one already did.

The slug is what scopes the merge. A cohort emits one H1 carrying it, so two cohorts never blend: `artifacts` and `references` each hold their own `Operations`. Without that scope the parameter would only be a depth, and a depth cannot say which part of a tree is worth merging.

A merged heading keeps its source text. Where that text occurs once in its group there is nothing to disambiguate, and most do: composing Plan Mode with `--group artifacts:2` leaves every one of the twenty-four merged operations bare. Where two or more documents contribute one text, it is emitted once and each document's content hangs beneath it under a branch heading naming that document, so the eight `Template` fields sit together under one `Template` rather than scattered under eight qualified names. Thirteen names branched this way, all of them in `Fields`.

A branch heading is the shortest run of that document's path which distinguishes it from the others, in title case, measured after dropping the leading segments they all share. In this cohort that is one segment, `Architecture Overview` against `Epic Issue Body`; across two libraries carrying one slug it would be the library name. Qualifying the heading text itself was tried first and discarded: it spelled the same distinction but left the variants apart, which is the comparison the merge exists to make.

This supersedes refusing the collision. Refusal was the right answer while every merged name was either unique or a conflict; minimal qualification is better because it distinguishes exactly the names that need it and leaves the rest alone, so the composite does not acquire a naming scheme that applies to everything in order to handle a minority. What survives of the refusal is the case qualification cannot reach: two headings of one document colliding in one group, which the source heading rules already refuse.

Anything still coinciding takes the renderer's ordinal, as any repeat does. Eleven did, five of them generated cohort or merged-section headings matching a section name in an unmatched document.

Two things needed a home once a merged document stopped being contiguous. A cohort is headed by its directory slug in title case, and a member's preamble becomes a synthetic section of that cohort named by the document's stem in title case, so `artifacts/epic-issue-body.md` contributes `Epic Issue Body` under `Artifacts` and its path reads `Artifacts/Epic Issue Body`. A preamble is then a section like any other instead of occupying a structure of its own. Three shapes were discarded on the way: a `Sources` group above the cohorts, a file heading per member inside one, and a `Body` group inside one. The first invented a structural area, the second mixed paths in among section names, and the third added a level to hold a name the cohort already carries. And a reference to a cohort-depth heading resolves to the merged group, losing which document it meant, which is the cost of merging.

Measured on the Plan Mode closure with `--group artifacts:2`: 8 top-level groups against 27, 13 branched names, 259 destinations against 353, 20 ordinals against 81. Published and rendered by GitHub, every fragment link resolves against the anchors it generates, with none broken.

Only `work-planner` is broadly representative in this workspace, so the cross-library case the parameter is built for, two directories of one slug under separate libraries, is implemented but not yet exercised against real sources.

## D25 — The Routing Document Is Not Composed, and the Entry Reference Is Emitted Last

A skill's entry point is a routing table. The agent reads it, chooses a procedure, and passes that procedure's link to md-compose. The routing document is therefore never composed, because it is never an entry reference: `SKILL.md` routes, `modes/plan-mode.md` is the argument, and the composite holds the argument and what it reaches.

Groups are ordered by root-relative path, except that a document named as an entry reference is emitted last, entry references in the order given. A cohort keeps a member it claims, so the rule applies to document groups. The agent then reads its routing document, invokes the tool, and finds the procedure it asked for at the end of what that procedure needs.

The question this settles is whether the entry has to come last for the content it references to have been read by the point of use. It does not, and nothing could make it so. The reference graph of the Plan Mode closure is cyclic — `epic-issue-body` to `epic` to `initiative-issue-body` and back, among three cycles — so no ordering makes every reference backward. Between 31 and 61 of its 194 cross-document references point forward whichever order is chosen. The delivery contract settles the practical question anyway: the agent holds the whole validated document before it acts, so a forward reference costs nothing.

That leaves arrangement, decided on what the reader does with it. The entry reference is what the agent carries out and the rest is what it carries out against, so it sits closest to the point of acting with its material already laid out. Nothing in the closure references it, 30 references leave it and none arrive, so moving it costs no document its own context.

It is also the best of the three on the measure: 163 backward references against 161 for path order and 133 for entry-first. That margin is two references and is not the reason.

Composing a routing document instead, as an experiment did, is not the intended use and shows why. `SKILL.md` pulls all 38 documents of the skill into one 301 KB composite, which is the whole library rather than the context for one operation.

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
