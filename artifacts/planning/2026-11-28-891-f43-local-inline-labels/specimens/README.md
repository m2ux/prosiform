# Local Mermaid Label Specimen

The identical [source](source/guide.md) is compiled with released pf 0.36.0 and the F43 source build. Both produce valid local targets. Only the corrected build consumes inline operators on local node labels; the worker-file dispatch and unrecognised literal label remain visible.

| Build | Parent Bundle | Worker Bundle |
| --- | --- | --- |
| Released 0.36.0 | [Before](before/guide.bundles/guide.bundle.md) | [Before worker](before/guide.bundles/worker.bundle.md) |
| F43 | [After](after/guide.bundles/guide.bundle.md) | [After worker](after/guide.bundles/worker.bundle.md) |

The specimen covers quoted labels, metadata labels, a same-line click, deferred inline content and literal text without the required operator spacing. The deferred directive stays inside the local contribution for later compilation. [Receipts](receipts.json) pin the actual output hashes. This is compiler inspection, not an agent trial.
