# Metadata Contract Review

## Reviewed Inputs

The criterion is epic #218 AC1: the normative design defines per-file conversion metadata and its failure behavior, observed through contract review. The reviewed component is `artifacts/planning/2026-10-17-prosiform-v1/design.md` on `i01/e06/w01-declared-metadata-contract`.

Candidate commit: `91eecd4c89bcd461806b5d70806714dde48bcd54`, published in [PR #219](https://github.com/m2ux/prosiform/pull/219). Candidate SHA-256: `d0677eaca3cc972c6eabbb79ed53e8c7d102b4e000ab2ba2aa7fe5992b878367`. Compiler baseline: `cd3d8e635b8db500ceb7230b26209bdd37f637da`. The candidate is contract prose; no compiler behavior is claimed. The baseline remains the fixture oracle until the decoder, source-reader and compilation tasks implement this contract.

## Requirement Trace

| Design decision | Normative clause | Review observation |
| --- | --- | --- |
| Per-file skill-compatible strings | Conversion metadata, field table | Paired fields, quoted decimal depth, absent values and unrelated skill fields are explicit. |
| Explicit membership | Grouping — Group membership | Exact identity, individual groups, unrelated directories and no discovery are defined. |
| Coherent group depth | Grouping — Consistent depth; Metadata failures | Contributors agree; deterministic pair and both coordinates are specified. |
| Destination ownership | Conversion metadata — Source ownership | Direct, fragment, ordinary, transitive and repeated selection use one captured immutable value. |
| Deferred boundary | Conversion metadata — Selection boundary; deferred link target | Local validation on normal open; no deferred-only membership or outgoing discovery. |
| Safe interpretation | Conversion metadata — YAML grammar; Bounded parsing | YAML 1.2 Core, duplicate equality, aliases/tags/merge rejection, byte and preconstruction nesting limits are specified. |
| Original source capture | Frontmatter policy | BOM and delimiters retained; metadata bytes participate in accounting/hash and source coordinate mapping. |
| Structural CLI removal | CLI table, examples; Operational interface | Only source metadata supplies structure; unsupported option fails with usage exit 2. |
| Atomic failure | Metadata failures; existing publication contract | Exit 1, no bundle on stdout, preserved output file and check-mode failure. |
| Assembly and validation | Grouping; Selection boundary; Outline preservation | Member names, variants, overview, anchors and candidate validation use the same source declarations. |
| Language handoff | Implementation verification — Source-language handoff | Tagged contract and fixture evidence bind Python and Rust; review does not assert implementation. |

## Verification Matrix Review

All twelve rows of the approved proposal's Verification Matrix have normative fixture obligations:

| Proposal outcome | Candidate metadata conformance row |
| --- | --- |
| A file controls its own arrangement | Per-file ownership |
| Metadata is local | Per-file ownership; Explicit grouping |
| Shared groups are coherent | Explicit grouping; Atomic failure |
| Repeated reachability is stable | Stable selection |
| Deferred settings take effect only for contributions | Stable selection |
| YAML interpretation is explicit | Accepted YAML; Rejected metadata |
| Metadata parsing remains bounded | Safe YAML |
| Metadata stays outside the body | Body separation |
| Output retains source meaning | Preserved assembly |
| Failure publishes nothing | Atomic failure |
| CLI has one structural source | Public interface; CLI adversarial fixtures |
| Published package exercises the contract | Public interface |

Expected outcomes are prescribed, not measured compiler results: valid declarations merge only contributing members; unannotated files stay individual; local malformed metadata fails even on deferred validation; deferred-only depth differences do not conflict; contradictory contributing depths fail atomically and deterministically. Fragment selection does not select the frontmatter as content. Representative baseline comparisons annotate exactly the contributing members, then compare bundle bytes at the recorded baseline. New failure fixtures must be independent of parser/assembler implementation.

## Diagnostic Inventory

The exact candidate adds `E_INVALID_FRONTMATTER`, `E_INVALID_CONVERSION_METADATA` and `E_GROUP_DEPTH_CONFLICT`, and removes `E_INVALID_GROUP_RULE` and `W_EMPTY_GROUP_RULE`. Existing `E_UNTERMINATED_FRONTMATTER`, `E_RESOURCE_LIMIT` and `E_INVALID_USAGE` retain their categories. YAML/root safety errors and metadata-schema errors have distinct ownership; related locations distinguish duplicate keys and group conflicts.

The baseline JSON diagnostic carries a rendered source field, not structured coordinates. The contract therefore explicitly specifies `location` and `related` objects for metadata errors, with physical lines and Unicode code-point columns. Implementing that surface belongs to the metadata implementation tasks.

## Candidate Checks

Passed against the candidate bytes named above:

- `git diff --check`: no whitespace defects.
- Pinned `checks/vocabulary.py` helpers: all 36 marked contract terms are defined in the baseline glossary; no avoided term introduced.
- Pinned `checks/links.py` helper against the candidate: the new local `#conversion-metadata` link resolves. Seven references inventoried; six existing external references were not reached. External availability is outside this local check.
- Independent full link check: `python3 checks/links.py --online /home/mike1/projects/dev/md-composer/.worktrees/i01-e06-w01/artifacts/planning/2026-10-17-prosiform-v1/design.md`, run from the pinned baseline checkout, passed with exit 0. All six external references and the local anchor resolved.
- Exact diagnostic inventory comparison: three additions and two removals, as listed above.
- Stale-wording search: no active directory-rule, discarded-YAML, old diagnostic-code, accepted structural-option or deferred-not-opened claims survive in the amended component.
- Requirement and verification-matrix review above: every agreed decision and every proposal verification row has a normative home.

The reproducible helper is [contract-check.py](contract-check.py). It uses the pinned baseline checker functions and reads the candidate path explicitly; it does not mistake the README's remote engineering design for the edited candidate. The first local-link attempt reported existing external links as unchecked; the final helper distinguishes that limitation from local resolution failures.

## Limits and Handoff

Full compiler conformance, fixture execution, installed-wheel smoke and semantic glossary migration remain the already planned compiler and consumer tasks. Running baseline conformance against the new design would intentionally disagree on metadata codes and the retired CLI grouping surface. Those checks cannot establish AC1 and are not represented as passing compiler tests. No new package, parser selection, source code or historical capture is changed here.

Independent review reconciled YAML key-error categories, defined nesting and structured coordinates, and confirmed group ordering by least contributing source path already matches baseline `grouping.py`; directory-key prose was stale. The new schema specifies single-line printable nonblank slugs for safe generated headings while preserving colon/slash exclusions and exact string identity. This is a bounded field-contract refinement, recorded in the change list.

## Merge and Delivery

The user explicitly confirmed that the repository's automatic closure of issues on linked pull-request merge is disabled. Fresh readiness checks found PR #219 at the reviewed head `91eecd4c89bcd461806b5d70806714dde48bcd54`, targeting `i01/e06/engineering`, mergeable and clean. Branch protection returned 404 (unprotected), and active rules returned an empty array. No check runs, status contexts or reviews existed; the status endpoint's aggregate `pending` value had zero contexts and represented no outstanding check. The three published Test Plan rows passed on the reviewed head. The epic base was current, and a final read confirmed the same task head.

PR #219 merged with a merge commit, explicitly guarded by that head SHA. Readback confirms merge commit `ed61bd28cfac18b4d2d066328a986902ba783767`. Delivery synchronization marks W01 Done and AC1 checked, with every other task and criterion still incomplete. No task issue exists to close; W02 was not started.

Draft [epic review #220](https://github.com/m2ux/prosiform/pull/220) presents the actual W01 changes from `i01/e06/engineering` into `engineering`, citing task PR #219. It remains draft and unmerged. Refreshed delivery reconciliation finds the review in flight and the remaining four tasks undelivered; the epic remains In Progress.

Both PR Development relations were read completely and are empty. W01 correctly has no task-issue link. The epic review requires a link to epic #218 through GitHub's Development sidebar. No authenticated browser, computer-use or GitHub linking capability is exposed in this session, so that relation remains the sole recording limitation. The review body contains no closing-keyword workaround. A user can open issue #218, choose Development, and select PR #220.
