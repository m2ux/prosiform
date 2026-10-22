# Prosiform Author Skill

## Goal and Scope

An agent can create Markdown files for an intended Prosiform compilation, preserve the requested meaning and document shape, explicitly connect required context, and report the result of validating the authored sources.

- **Confirmed scope.**  Any Prosiform-compatible Markdown; user decision on 2026-10-22.
- **Delivery.**  One skill at `skills/prosiform-author/` on this repository's workspace branch.
- **Invocation.**  Normal automatic discovery and explicit `$prosiform-author` invocation.
- **Requests.**  “Create Prosiform-compatible Markdown”, “write a document for Prosiform”, and “write linked Markdown that Prosiform can bundle”.
- **Boundary.**  Creating documents and correcting them during authoring; a repository-wide migration or standalone audit is a separate request.
- **Non-goals.**  Compiler changes, a new Markdown dialect, a second validator, installation tooling, publishing generated documents, and imposing agent-skill structure on ordinary documents.
- **This record.**  A creation plan; implementation requires a subsequent request. No issue, initiative or board expansion is needed for this single delivery unit.

## Source Authority

| Concern | Authority | Application |
| --- | --- | --- |
| How the skill is written | User-linked `workflow-server/workspace/skills/guidelines.md` | Entry point, mode structure, prose, links, command ownership, progressive disclosure and verification |
| What Prosiform accepts | Prosiform design and fixture corpus | Markdown profile, source selection, dependency graph and validation guarantees |
| How an installed build is invoked | Its `--version`, `--help`, `--codes`, and matching `invocation.md` | Commands and diagnostic handling verified against the build actually used |
| What the generated documents say | The user's writing request and applicable destination instructions | Content, audience, style, location and intended entry points |

The shared skill guidelines govern this skill's own files. Their prescribed `SKILL.md` and procedure sections are not Prosiform grammar requirements and do not become a required template for every generated document. The profile identifier `skill-markdown-v1` also does not restrict the skill to agent skills.

Freeze the compiler revision used for implementation validation, record its package version and profile, and associate results with that revision. Review newer contract changes before updating the skill's compatibility claim. Conflicts among prose, fixtures and observed behavior remain explicit until resolved; the skill must not invent a rule to hide them.

## Skill Structure

Use one authoring mode. Validation belongs to that mode's completion path.

| Planned file | Responsibility |
| --- | --- |
| `skills/prosiform-author/SKILL.md` | Purpose, objects acted on, Author mode selection, shared constraints and dependencies |
| `skills/prosiform-author/references/author-mode.md` | Authoring sequence, validation, diagnostic handling and local command specifications |
| `skills/prosiform-author/references/markdown.md` | Author-facing compatibility rules and small, fenced examples |

Use only `name` and `description` in frontmatter; the name matches `prosiform-author` and the description stays below 1,024 characters. The opening identifies source documents, selected sections and dependency links. The single mode links to `references/author-mode.md`; its first selector states “Forward-looking, scoped to one Markdown authoring request”.

The mode uses Prerequisites, Procedure, Reference, Rules and Commands in that order, including only sections it needs. Command specifications belong in its Commands section, with their conventions before the procedures that need them. The entry point contains no shell command. The compatibility reference contains no procedure and takes headings appropriate to its subject.

The standard `references/` directory needs no custom directory contract. Add no hook, custom `structure.json`, harness metadata, executable helper or template collection without a concrete implementation need. Use the existing skill checker and the real compiler. Keep maintained behavioral specimens in a skill-local `test/` directory only where they support repeatable acceptance checks; record evaluation transcripts in the engineering record.

## Authoring Behavior

1. **Establish the requested output.**
   Identify the document's purpose, audience, destination, source root, intended entry documents or sections, and any requested grouping. Inspect applicable local instructions and existing conventions. Ask only for missing choices that change the content or its compilation; a simple standalone document does not require a multi-file design interview.
2. **Verify the validation environment.**
   Identify the available Prosiform executable, its version and profile, and the relevant command help. If it is unavailable or cannot be matched to the target contract, author from the documented contract and report compilation as unverified. Installation or environment repair is separate work unless authorized.
3. **Arrange the sources.**
   Use the smallest useful set of documents. Choose unambiguous section headings and put required content inside the intended selection or behind explicit ordinary dependency links. Separate optional branches using deferred links where later compilation is intended. Keep metadata separate from executable instructions.
4. **Write the Markdown.**
   Preserve the user's content and document conventions while applying the compatibility rules below. Use real links for dependencies and fenced blocks for literal examples. Explain any unavoidable content decision to the user; compiler compatibility alone does not decide what the document should mean.
5. **Validate every promised entry.**
   Run the actual compiler with the chosen root and entry reference, using `--check --diagnostics json`. Validate each intended entry separately and any intended combined invocation, including grouping options where requested. Check deferred branches as separate entries when their later compilation is part of the deliverable.
6. **Inspect and correct.**
   Compile representative successful entries into a temporary output outside the source set. Check required context, omission of deferred content, heading hierarchy, rewritten links and preserved examples. Repair in-scope authoring defects and rerun affected entries. Report usage, publication, internal or environment failures by their actual category; do not treat every nonzero status as a prose defect.
7. **Report the result.**
   Name the authored files, tested entries, root, compiler version/profile and results. Distinguish compiler success from content review and untested branches. A failed or unavailable run cannot establish compatibility, and `--check` success for one entry says nothing about every other section in the source tree.

The validation command specification will use `prosiform --root '<source-root>' --check --diagnostics json '<entry-reference>'`. A separate specification will describe compilation to a temporary output with `--output`, and the information commands will have their own specifications. Inputs are substituted and shell-quoted before execution. The mode owns all these specifications; no command wrapper is planned.

## Compatibility Coverage

| Area | Guidance the skill must carry | Observable check |
| --- | --- | --- |
| Encoding and files | UTF-8 sources with `.md` or `.markdown` suffixes; suffix recognition is case-insensitive, filesystem spelling is preserved | Accepted supported source and explicit rejection of invalid encoding or entry suffix |
| Markdown grammar | CommonMark with tables and strikethrough; literal task-list markers; no raw HTML, wiki links, footnotes, custom heading attributes or include directives as active constructs | A document exercising supported constructs compiles; active unsupported constructs fail; fenced examples remain literal |
| Metadata | A recognized leading `---` block closes with exact `---` or `...`; it is stripped, not a dependency or instruction source; use `***` for a literal opening thematic break | Required prose remains in the bundle body; leading metadata does not |
| Sections | Document-level ATX and Setext headings are selectable; selection ends at the next equal-or-higher document-level heading and includes deeper subsections | A selected section includes its descendants and excludes its sibling |
| Prerequisites | Parent body text, preambles and sibling prerequisites are not inherited by a section; heading-only ancestors provide outline only | A procedure selected directly still carries every required rule through explicit links |
| Fragments | Target source-heading slugs, with exact lookup; colliding source slugs are ambiguous; renderer-generated duplicate ordinals are not source identities | Unique headings resolve; duplicate targets and invented `-1` disambiguation fail |
| Containers | A heading inside a list or blockquote is not a selectable section root | Nested headings may occur in included content, but direct fragment selection fails |
| Paths and root | CLI entries are root-relative; source links are relative to their containing file; fragment-only CLI entries need `--from`; source access below the root refuses symlinks | The same source resolves correctly from multiple callers; unsupported path forms produce diagnostics |
| URI spelling | Forward-slash paths; valid percent encoding interpreted once; no query on local Markdown dependencies | A filename containing a literal `#` is addressable without treating it as a fragment delimiter |
| Dependencies | Ordinary local Markdown links under the root recursively include their targets; apparent links in code and unlinked path text do not | Required shared content occurs once; code examples and plain path mentions add no dependencies |
| Optional branches | Text such as “when needed” does not suppress a link; `[¬ Label](target.md#section)` defers it, with a valid target and instructions for later compilation | The target contributes no content through the deferred link; the emitted destination supports a separate run |
| External material | Web links, source links outside the root, non-Markdown resources and images are not bundled content; images are resources even when naming Markdown | Compilation does not imply those references were fetched, embedded or verified |
| Reference links | Definitions belong to their source file; resolved reference-style links work, including definitions outside selected sections | The result preserves the intended reference and does not borrow another file's definitions |
| Heading arrangement | Output headings and anchors are compiler-owned; shifts, absorbed titles and requested grouping can change available depth | Validate the actual entry/grouping combination; reject H6 overflow rather than flattening authored structure silently |
| Source identity | Filenames differing only by Markdown suffix or case can collide in file groups; avoid confusing names | Distinct intended sources retain distinguishable groups under the tested arrangement |
| Source and bundle roles | Maintain original source files, with compiled output separate; rebundling generated output is unsupported | Validation and later authoring use the sources, not an earlier bundle |
| Completeness and execution | Compilation follows explicit links; it neither infers missing instructions nor authorizes execution of included procedures | Review checks the requested meaning and includes no automatic execution of document examples |
| Failure and scope | `--check` validates the selected closure, with necessary file-wide parsing checks; budgets fail rather than truncate | Every promised entry has a result; failure is reported with diagnostics and no claim of successful compilation |

Keep rare path and arrangement details under focused reference headings. Authoring reads the common syntax and dependency guidance first; advanced guidance is loaded only for a document that uses it. Use fenced examples so illustrations of invalid syntax and dependency links do not become active constructs in the skill itself.

## Acceptance Criteria

| ID | Required outcome | Evidence |
| --- | --- | --- |
| AC1 | The skill activates for general Prosiform Markdown authoring without imposing agent-skill headings on ordinary documents | Description review and an ordinary-document authoring evaluation |
| AC2 | A standalone authored document preserves the requested content and compiles under the recorded build/profile | Source review, command, status and output |
| AC3 | Direct section entry includes every explicitly required dependency and excludes unrelated sibling body content | Multi-file specimen and inspection of its compiled closure |
| AC4 | A conditional branch uses deferral correctly and its promised later entry compiles independently | First-run and deferred-run results, plus target existence failure case |
| AC5 | Authoring repairs missing targets, ambiguous fragments and unsupported active syntax without altering the requested meaning | Controlled defective specimens, diagnostics, corrected sources and reruns |
| AC6 | Section boundaries, reference-style links, metadata and heading depth are explained accurately | Coverage matrix linked to compiler fixture evidence and small skill examples |
| AC7 | The agent distinguishes validation success, untested selections and unavailable or mismatched validation environments | Evaluation with an unavailable executable and a multi-entry request |
| AC8 | Skill files meet the requested guidelines, contain resolving links and expose all required common context through supported reading paths | Shared checker, frontmatter validator and disclosure review |
| AC9 | Realistic authoring succeeds in fresh agent contexts with the intended reading scope | Independent behavioral evaluations, actual reads, generated files and compiler results; repeat affected scenarios after corrections |

## Sequential Delivery

One implementation task produces one pull request against `workspace`. Complete each stage before the next; commit distinct implementation work incrementally on the same branch.

| Stage | Work | Exit condition |
| --- | --- | --- |
| 1 — Establish the baseline | Create a dedicated linked workspace worktree, reread its instructions and guidelines, and verify an isolated compiler build against the selected source revision | Version/profile and fixture evidence recorded; discrepancies below resolved for the rules the skill will promise |
| 2 — Write the skill | Add the three instruction files, grounded examples and the one authoring path; retain the general-Markdown boundary | AC1 and the complete compatibility coverage have identifiable homes |
| 3 — Validate behavior | Run structural checks and representative compilations; evaluate ordinary, multi-file, deferred and defective-input requests in fresh independent contexts | AC2–AC9 have evidence; observed failures corrected and affected scenarios repeated |
| 4 — Deliver | Review the final diff and source trace, record validation and any limitations, commit and push, and open the implementation PR | Reviewable skill with accurate local evidence; merge remains a user decision |

Planned structural checks are `python3 skills/scripts/check_skill_files.py skills/prosiform-author` and the skill-creator `quick_validate.py` against the new skill. Run shared checker tests if shared checker code changes; no shared checker change is currently planned. Do not run the entire compiler suite for instruction-only work unless a new finding requires it.

Independent evaluations use disposable output directories and realistic requests, without expected routing choices or solutions. Inspect actual tool reads, generated sources and compiler results. Repeat any scenario whose instructions change. Structural validation and behavioral evaluation are separate evidence; file counts are not a claim of token savings.

## Known Evidence Constraints

- The inspected source declares `0.9.0`, while the existing virtual-environment executable reports `0.1.0`. That environment is not yet an identified validation baseline.
- One general paragraph in the design's path section says a reference leaving the root fails; its classification section, resolution table and invocation guide distinguish rejected outside-root entries from authored outside-root links retained as text. The skill must preserve that distinction and verify it with the corresponding fixture.
- The design's deferred-target paragraph simultaneously requires heading validation and says the target is not opened or parsed. Teach the observable contract—target validity and exclusion from the compiled content—and verify it with fixtures, without repeating that implementation claim.
- Grouping work is active on separate worktrees. Teach and test only behavior supported by the selected implementation revision; future or proposed behavior is not an authoring guarantee.

These are implementation verification requirements, not permission to modify the compiler or its contract as part of creating this skill. No user scope decision remains open for this plan.
