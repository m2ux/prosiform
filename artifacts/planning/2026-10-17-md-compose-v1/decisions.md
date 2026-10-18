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
