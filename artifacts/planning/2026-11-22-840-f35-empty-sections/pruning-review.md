# Pruning Side-Effect Review

## Result

No correctness regression found at F35 head 4737171c6db91e4c9735fcfcbb1f775e6d39382c. The review covers the pruning implementation, both assembly passes, reference protection, destination/position mapping, composition ownership, final candidate validation and diagnostic publication. The narrow policy is suitable to ship within these checked boundaries; it is not a proof over every possible document or downstream consumer.

## Preserved Behaviour

- Only empty, unreferenced generated group, overview, member-overview and preamble wrappers are eligible. Authored headings and structural ancestors remain, including empty anchors.
- Body content, containers and code examples retain their surrounding outline. Selected source ranges retain their bytes and provenance.
- Referenced document identities and their ancestors remain. The first destination owner is protected independently in each assembly pass.
- Filename, variant, composition, dispatch brief, choice and parallel-dispatch sections remain outside the pruning set.
- Dispatch positions are translated through the retained-heading map before anchors are assigned. Composition owners use retained heading identities. Final validation checks coverage, structure, anchors, references, contributions and dispatch destinations before publication.
- Input source files are read-only to compilation; probe hashes confirm they retain their bytes.

## Observable Effects

- Every omitted wrapper emits W_EMPTY_SECTION while successful compilation retains exit status zero. Consumers that treat any stderr or an unknown warning code as failure must accept this diagnostic. The classifier warning guard already recognizes its precise expected instances.
- The output outline loses the omitted wrappers. Removing a duplicate heading can change later generated anchor suffixes. Internal destinations are assigned from the retained outline. External bookmarks or manually stored fragments from an older generated bundle are outside that rewrite and may need updating.
- The outline-stage probe demonstrates beta-1 becoming beta with a correct retained-position map. This is a construction-level boundary check, not a claim that the end-to-end link-preservation specimen changes its anchor: that specimen retains beta-1 before and after.

## Verification

- Fresh focused rerun: all 28 pruning and dispatch-display tests pass.
- Six additional [probes](side-effect-probes.json) pass: explicit title targets through inline, reference-style and diagram links; a document reference from composed content; internal-link preservation with a pruned sibling; and duplicate-anchor reassignment at the outline stage. The [probe program](side-effect-probes.py) records their construction.
- The same head's [completed full checks](current-main-make-check.txt) pass: 2,318 compiler tests, 1,155 harness tests and all 708 corpus fixtures, plus guards and smoke checks. No product code changes follow that run.
- Against merged F34, the F35 corpus delta consists of one empty generated Beta heading and its declared warning. Its fixture source is preserved; no broad source-padding migration is included.

## Limits

GitNexus has no index for this worktree; its registered Prosiform indexes predate the change. Callers and downstream stages were traced directly in the current source. Arbitrary external consumers, historical external bookmarks and large-input performance are not independently validated by this review. The additional reference scanning in each assembly pass has no isolated overhead measurement here.
