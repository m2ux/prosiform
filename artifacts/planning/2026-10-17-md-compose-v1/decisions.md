# Decisions

The planning decisions taken with the user, each with the reasoning that produced it.

## D1 — The Python Prototype Is a Semantic Oracle

Python implements the full behavioural contract — closure, consolidation, anchor identity, validation, diagnostics and CLI — and produces a language-neutral fixture corpus of exact expected composites. Source-span edit fidelity is proven in Rust, where the production parser lives.

The design's hardest unproven element is the source-range adapter, which is parser-specific and would not transfer from a Python CommonMark parser to `pulldown-cmark`. Its hardest semantic elements — dependency closure to a fixed point, overlap consolidation, qualified destination identity and the post-compilation invariants — are parser-independent and provable cheaply. Splitting the work this way makes the corpus the durable artifact and keeps the prototype a retained component rather than a stopgap.

## D2 — Gate Evaluation Precedes the Rust Build; Upstream Is a Separate Proposal

The Rust initiative opens with an epic that empirically proves or disproves both mandatory parser viability gates against a pinned `pulldown-cmark`, producing a written verdict. The upstream contribution is a non-goal of this proposal. A failed gate triggers a new proposal for the upstream route, raised only then.

The gates are mandatory before any composite is published, so an unsatisfiable gate blocks the Rust initiative. The assessment concludes the current public API probably satisfies neither. Carrying the risk as a gate epic makes the blockage visible and dated without authorizing outbound action, which the design forbids. An upstream contribution depends on maintainer agreement, so it does not belong inside an initiative whose completion is otherwise controlled here.

## D3 — One Repository, Prototype Retained

`m2ux/md-composer` holds `fixtures/` (the language-neutral corpus and the contract it encodes), `prototype/` (the Python oracle, retained and maintained) and `rust/` (production md-compose). Both implementations run the same corpus in continuous integration.

The no-stopgap principle rules out a draft that a later version replaces. It does not rule out a second implementation that keeps proving the first. Retaining the oracle gives differential testing: a divergence between two independent implementations on the same input is a defect in one of them, which catches classes of error the fixtures did not anticipate.

## D4 — One Theme Board

A single md-compose theme board, copied from the Initiative template, holds both initiatives and their epics.

Two boards would split one product's queue and hide the dependency between the stages. One board shows the Rust initiative's readiness as gated on the prototype's corpus.

## D5 — Goal Clauses

Seven clauses, confirmed by the user, stated as outcomes someone could observe:

- **G1.** Given a source root and one or more local document or section references, an agent receives one continuous Markdown document containing the selected content and every local Markdown dependency reachable from it.
- **G2.** Every internal reference in that document resolves to exactly one destination within it, and each included source region appears exactly once however many paths reach it.
- **G3.** Selected instruction wording and code examples are byte-identical to their sources apart from the transformations the declared profile names.
- **G4.** The original outline of each selected section survives: its ancestor headings are present, its relative depth is preserved, and each contributing file's content sits beneath one heading naming that file.
- **G5.** A composition that cannot be fully validated emits no composite and exits nonzero, with a diagnostic naming the defect, its source location, the offending reference and the inclusion chain that reached it.
- **G6.** Authors keep their existing modular files; nothing beyond ordinary Markdown links and optional heading anchors makes a document composable.
- **G7.** The contract is demonstrated by two independent implementations passing one shared fixture corpus.

The user declined two offered amendments: dropping G7 as a planning rather than product outcome, and adding the agent delivery contract as an eighth clause.

## D6 — The Prototype Parses With markdown-it-py

The Python build parses with `markdown-it-py`. `I00:E01:W02` configures it to the declared profile rather than selecting a parser.

The profile needs pipe tables, double-tilde strikethrough, source task-list markers preserved without checkbox generation, and typographic substitution disabled. `markdown-it-py` is CommonMark-compliant, supplies the first three through option-controlled plugins and the fourth by leaving its typographer off, and exposes a token stream whose structure is the closest Python analogue to `pulldown-cmark`'s event model. That similarity matters beyond convenience: profile reasoning that holds for one build reads across to the other, so a divergence between them is more likely a defect than a difference in how each parser frames the same document.

Block tokens carry line ranges and inline tokens do not, which bounds how precisely the prototype can locate an edit. That bound is acceptable here because byte-exact span editing is D1's explicit non-goal for this build; the prototype may reconstruct its output provided the corpus's preservation fixtures hold. A candidate parser is not excluded later: a fixture the prototype cannot satisfy for parser reasons is a reason to revisit this decision, recorded as one.

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
