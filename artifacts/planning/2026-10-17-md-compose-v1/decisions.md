# Decisions

The planning decisions taken with the user, each with the reasoning that produced it.

## D1 — The Python Build Is the Tool in Use

Python implements the full behavioural contract — closure, consolidation, anchor identity, validation, diagnostics and CLI — produces a language-neutral fixture corpus of exact expected composites, and ships as the tool agents in this workspace invoke. It is used for an extended period before a production build is committed to. Source-span edit fidelity is proven in Rust, where the production parser lives.

The design's hardest unproven element is the source-range adapter, which is parser-specific and would not transfer from a Python CommonMark parser to `pulldown-cmark`. Its hardest semantic elements — dependency closure to a fixed point, overlap consolidation, qualified destination identity and the post-compilation invariants — are parser-independent and provable cheaply.

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
- **G6.** Authors keep their existing modular files; nothing beyond ordinary Markdown links and optional heading anchors makes a document composable.
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

## D12 — Each Run Is Measured Against Reading the Sources Whole

A run record carries the composed output size and the total size of the same sources read whole. The refinement stage is not settled until each source in the exposure set has that pair recorded.

The proposal justified this work with a retrieval cost. Every criterion since has been about correctness, so without this the plan would never answer the question it was raised to answer. The measurement rides on a record that already exists for other reasons, so it costs one field and one criterion.

## D13 — Deployment Stays Behind the Validation Gate

Field deployment waits on the validation gate and runs in parallel with the conformance report. It is last in numbering, not in dependency.

Deploying five levels earlier, once destinations resolve, would start the refinement stage sooner. It would also put an unvalidated tool into use: no reparse of the finished composite against what was selected, no boundary safety, no detection of a source that changed mid-run, and no diagnostics explaining a failure. Findings recorded then would mix genuine specification problems with defects the gate would have caught, which is the evidence the stage exists to produce.

## D14 — The Entry Point Says Compose; Later the Harness Does It

An agent decides between reading a document and composing it exactly once, on entry. Inside a composite the question cannot arise: every supported local Markdown link has been rewritten to an internal destination, and a link that could not be rewritten failed the composition.

That rules out marking individual links. It would also contradict the goal clause stating that nothing beyond ordinary Markdown links and heading anchors makes a document composable, and it would have to be maintained across every link in every skill. Inferring the choice from file names or paths is excluded for the same reason the design excludes inferring prerequisites from them.

So the mark belongs at the entry, and the question is who acts on it. In the first stage the skill's own text names the invocation, which needs nothing built and is the natural replacement for the prose that told the agent to read. In the second the skill declares itself composable and the harness composes on load, so the choice stops being the agent's at all. Frontmatter suits that declaration: md-compose strips frontmatter, so the marker never reaches the output, and the reserved-anchor rule already stops a composite being composed again.

The first stage runs during refinement, as each prerequisite section is removed. How reliably agents follow a written instruction is itself evidence, so the second stage is raised as its own proposal once there is use to draw on, rather than planned from an assumption about how well prose works.

## D15 — A Failed Composition Stops the Work

A caller meeting a failed composition halts and surfaces the diagnostic. Reading the sources instead is unsupported, and the documented invocation says so.

A fallback would restore the behaviour composition replaces, and would restore it silently: the work would continue, nobody would notice, and the failure would produce no ledger entry. The refinement stage depends on failures being visible, so an invisible one costs more than a halt.

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
