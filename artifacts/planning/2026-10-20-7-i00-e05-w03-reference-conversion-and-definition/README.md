# I00:E05:W03+W04 Reference Conversion, Definition Removal and the Absorbed Title - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the last two rows of [I00:E05] Destination Identity, delivered as one unit because W04 depends on the rewriting path W03 completes.

W03 resolves each source's reference-style links and images against that source's own definition environment, publishes each resolved use inline with its visible content and title preserved, removes every original definition node including the unused ones, and leaves bracketed text the parser did not resolve as literal text. It also carries the resource policy: a relative image or other non-Markdown reference is emitted byte-identical with a warning that resource portability is not guaranteed.

W04 settles the destination a reference reaches when it names a heading the file heading absorbed. [#57](https://github.com/m2ux/prosiform/issues/57) is its origin: a document's self-reference to its own title resolved to a destination the bundle assigned to nothing, so the published bundle carried a link to a fragment no heading generated and the run reported nothing.

It matters because these two rows close the epic. Until they land, a bundle carries one source's definitions where another source's literal brackets can reach them, and a reference to an absorbed title points at nothing.

## What W02 Already Landed

The map entry W04 needs is implemented. [#86](https://github.com/m2ux/prosiform/pull/86) folded it in as the behaviour needed to avoid a fault: `bundle.Group` carries an `absorbed` field and `cli.py` enters the absorbed slug against the file heading's own destination. It was deliberately **not** ticked, because AC8 is this unit's to tick on this unit's evidence. W04 is therefore mostly a fixture and a review that a title which was *not* absorbed is unaffected.

W02 also left one case raised rather than resolved: a marked reference-style link cannot be rewritten until the conversion to inline form lands. The run refuses rather than publishing a bundle naming a source path, and the case is declared as `rewriting/a-marked-reference-style-link` awaiting `I00:E05:W03`. A marked fixture fails the job if it unexpectedly passes, so this unit either clears it or explains why it stands.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | W03's plan: the definition environment, the inline conversion, the escaping and the removal |
| [w04.md](../2026-10-20-7-i00-e05-w04-a-reference-naming-an/w04.md) | W04's plan, in its own record: the absorbed slug mapped to the file heading's destination |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#7 \[I00:E05\] Destination Identity](https://github.com/m2ux/prosiform/issues/7) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Preceding row | [#86 \[I00:E05\] Link Rewriting Through the Destination Map](https://github.com/m2ux/prosiform/pull/86) |
| Absorbed-title gap | [#57 A Reference Naming an Absorbed Title](https://github.com/m2ux/prosiform/issues/57) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
