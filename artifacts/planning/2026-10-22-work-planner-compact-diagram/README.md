# Work Planner Mode Diagrams

[Mode Diagram Review](work-planner-compact.review.md)

## Source

The [workspace skill](https://github.com/m2ux/prosiform/tree/959dbc6635f76a31048a9734ae5ac80de8a3b367/skills/work-planner) is copied into [work-planner/](work-planner/): 77 files, including 49 Markdown documents. The copy omits 35 Prerequisites sections, each through the next heading of equal or higher level. All other content matches that source revision.

[Source Manifest](source-manifest.json) records the source revision, source and copy hashes, and removed section ranges. The workspace originals are untouched.

## Rendering

Each of the ten links under Modes in the copied SKILL.md supplies a separate compiler entry. The Markdown review has one subsection per mode, in that link order. Local dependencies are bundled under the shared work-planner root.

The canonical sections declared by [structure.json](work-planner/structure.json) are H2 headings. `--group artifacts:2 --group protocols:2` pools those sections within each directory group: Operations, Fields, Guidance and Commands for artifacts; Procedure and Guidance for protocols. Only reached content contributes. An unused group produces a diagnostic.

Every call uses `--compact --section-level 2 --max-output-bytes 1048576`. Images show content through H2 and H3 titles only. Links, body content and deeper headings within H3 sections are hidden. Other displayed body content is represented by `…`. Each mode has its own SVG, complete stdout, diagnostics, command, review and run record under [diagrams/](diagrams/). [Mode Runs](mode-runs.json) records all ten successful compilations.

## Reproduce

Use a clean compiler checkout with its locked environment installed and the [renderer](https://github.com/m2ux/prosiform/blob/00fd19df3660304cc5bdc979eb635032b905c4aa/scripts/render-diagram.py). From this planning folder:

```bash
/path/to/prosiform/src/.venv/bin/python render-modes.py --compiler-checkout /path/to/prosiform
```

The script reads the mode links, invokes the single-document renderer once per mode, verifies successful outputs, and assembles the combined review. Compiler provenance is recorded for each invocation.
