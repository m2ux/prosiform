# I05:E03 review findings (reviewed at main 8e56baf3, the #355 merge)

Reproductions were run against the build at that revision.

1. HIGH, CONFIRMED — cli.py:2087 `folder = Path(options.output, f"{run_name(selected)}{RUN_FOLDER_SUFFIX}").resolve()` then publish_folder cli.py:1875–1895. resolve() follows a symlink at <DIR>/<entry>.bundles, so the swap renames aside and rmtree's the link's target (out/ref.bundles -> ../precious: precious/data.txt deleted, precious/ now holds bundles); a dangling link writes the set outside -o. Violates design.md:573. The folder.is_symlink()/aside.is_symlink() branches are dead. Fix: resolve only the parent (Path(options.output).resolve() / name); treat a symlink at that path as an entry to unlink (never follow) or refuse it; keep the captured-source check against that path; test live and dangling symlinks.

2. HIGH, CONFIRMED — dispatch.py:447 (unmarked(link_text(...))) and dispatch.py:573 (f"{DISPATCH} {link.text}"): link text enters an ATX heading unnormalised. Soft-wrapped text or hard break, trailing space, or empty text → exit 4 E_UNEXPECTED_INTERNAL_ERROR, nothing published. Fix: collapse whitespace (" ".join(text.split())) for heading and ⫽ listing; refuse empty link text with an input diagnostic; fixtures for wrapped, trailing-space, empty.

3. MEDIUM, CONFIRMED — dispatch.py:686 `emitted = {PROSIFORM, PARALLEL} | {...}` always reserves both, so a bundle with no dispatch containing `## Prosiform` is refused (E_HEADING_COLLISION). Contradicts design.md:421/424 and the user-confirmed rule (refused only when pf emits that heading in the same bundle). Fix: drop the hard-coded pair; rely on emitted PROSIFORM_SECTION/DISPATCH_SECTION; fixture with these headings and no dispatch.

4. MEDIUM, CONFIRMED — derived-name collisions (a/b.md vs a_b.md; x.md#y vs x__y.md; a dispatched target named like the joined entry bundle) are caught only by open("x") at cli.py:1869: `pf -c` exits 0 while the real run exits 3 E_PUBLICATION_FAILED naming the hidden staging path with a wrong remedy. Violates design.md:573 and :109. Fix: detect duplicate names in publication() before the check branch, naming both targets; test under -c.

5. MEDIUM-LOW, CONFIRMED from code — cli.py:2100–2104 merges per-bundle captures keeping the last per path; a source edited between two bundles' reads publishes a mixed set. Fix: on merge, if two captures of one path differ, fail with the source-changed diagnostic.

6. LOW, CONFIRMED from code — cli.py:1884–1895: the restore os.rename(aside, folder) is unguarded (concurrent run → exit 4, old set orphaned as .x.bundles.old.<uuid>); rmtree(aside) failure after a successful swap reports exit 3 though published; staging suffix adds 38 chars → ENAMETOOLONG for 218–255-char names. Fix: guard restore and report the aside path; aside-cleanup failure becomes a warning; shorter staging suffix.

7. LOW, CONFIRMED —
   a. cli.py:1334 says "names no heading of the document it defers" for dispatched links too.
   b. `pf -c -o /nonexistent/zz ref.md` exits 0 while the real run exits 3 (design.md:99/109).
   c. Graph.beyond (dispatch.py:221–225) re-implements distinct(); distinct(hops) in cycle/analysed is redundant because traverse dedups.
   d. Dispatched links are discovered twice (cli.dispatches via uses; dispatch.written_in via inlines/events); disagreement would raise a bare KeyError at held[served]. Derive the hops from written_in.
   e. checks/tests/test_conformance.py:118,139 and checks/tests/test_independence.py:120,138 write manifests with stdout = "expected/stdout.md", which the schema rejects.
   f. fixtures/run-set and fixtures/delivery keep names of retired concepts.

Test gaps: symlinked run folder; wrapped/empty/trailing-space link text; Prosiform/Dispatch in parallel headings without dispatch; -c on a name collision; source change between bundles; restore failure.

Environment note: a pf installed on the host ahead of the build can shadow it in tests; run the checkout's own build.
