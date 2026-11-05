# Diagram Renderer

Two scripts draw a bundle. `render-diagram.py` takes any entry document and draws the files it opened beside the bundle. `render-example.py` draws the fixed cases the architecture pages carry, from the cases declared in `scripts/examples.json`.

Both use dark file panels, blue link labels and amber operator marks. The README's `run` example uses three columns: the source tree and entry, the linked documents, and the complete bundle. Arrows trace each link to its destination; repeated rules links converge on one bundled section. The other drawings mark heading levels at the left margin.

The scripts draw bundles for a reader of these pages. How a Mermaid diagram's own links are read is stated at [Diagram links](references.md#diagram-links), and `make render` holds them to rendering as links a reader can follow, as [Rendering](../checks.md#rendering) states.

## The architecture examples

`scripts/examples.json` declares one case per picture: an entry and the files around it. The build runs for real over a copy of that tree, and the drawing shows what it read beside what it wrote, so a picture cannot state a result the build does not produce.

```bash
make examples
```

That re-renders every case into `docs/images/`. A single case, at a chosen build:

```bash
python3 scripts/render-example.py dispatch --build 'pf' --output /tmp
```

| Argument | Purpose |
| --- | --- |
| `case...` | Case names from `scripts/examples.json`; every case when none is named. |
| `--output DIR` | Directory the drawings are written to; `docs/images` when absent. |
| `--build COMMAND` | The build's command line, split as a shell splits one; `pf` when absent. |

Every case draws and reports the build's exit status, so a case meant to fail is visible as one. A case declares the status it expects as `status`, `0` when absent, and the script fails when the build exits otherwise.

## Rendering any entry

`render-diagram.py` bundles one Markdown entry document and draws its opened source files beside the entry's bundle. Each call produces one diagram; a dispatched target's bundle is not drawn. Local Markdown dependencies are discovered by Prosiform.

Use a clean Prosiform compiler checkout. In its `src/` directory, run `uv sync --frozen --no-dev` to install the compiler. From the repository root, use that environment's Python:

```bash
/path/to/prosiform/src/.venv/bin/python scripts/render-diagram.py /path/to/skill/SKILL.md --output /tmp/skill-diagram
```

| Argument | Purpose |
| --- | --- |
| `document` | Entry Markdown file, such as `SKILL.md`. |
| `--output PREFIX` | Required output path prefix. Existing files with this prefix are overwritten; a prefix that would overwrite a source document is refused. |
| `--cwd DIR` | Invocation working directory; defaults to the entry document's directory. |
| `--section FRAGMENT` | Bundle one section of the entry document. |
| `--max-output-bytes N` | Compiler output-size budget in bytes; use a positive integer. |
| `--compact` | Retain headings and links; omit other body content in both image panels. |
| `--input-section-level N` | Input panels: show content through HN (1–6) and titles one level deeper. Defaults to all content. |
| `--compiled-section-level N` | Compiled panel: same cutoff, independently selected. Defaults to all content. |
| `--branch NAME` | Compiler branch; required for a detached checkout. Must point to its current commit. |
| `--revision SHA` | Require an exact compiler commit. |

Grouping comes from each source file's [conversion metadata](../invocation.md#conversion-metadata). Call the tool again for another entry, using a different output prefix.

For a large document set, add `--compact`. It preserves heading levels, inline and reference links, autolinks and image references. Other prose and code examples are omitted without placeholders. The saved bundle and diagnostics remain complete.

Compact mode affects the image, not the bundle size. If compilation exceeds the output budget, pass a larger limit, for example `--max-output-bytes 1048576`.

Use `--compact --input-section-level 2 --compiled-section-level 2` to show H3 titles without their body content, links or deeper headings. Content under H1–H2 follows the compact-mode rules. The section cutoff also works without compact mode. Set either panel independently: `--input-section-level 2 --compiled-section-level 3` shows H3 input titles and H4 compiled titles. Omit an option to show that panel at full depth. The saved bundle remains complete.

## Output

Each prefix produces `.svg`, `.review.md`, `.bundle.md`, `.stderr.txt`, `.command.txt` and `.run.json`.

The image header contains only the compiler branch and commit. The review Markdown carries the command, image, exit status and diagnostics. The run record pins the compiler revision and hashes the source bytes and output.

Body content and links are indented one step beyond their containing heading in both panels.

The tool returns the compiler's exit status. A rejected bundle still produces review artifacts; a source file appears only if the compiler opened it. Deferred targets may be displayed without contributing content. The SVG simplifies Markdown formatting; consult `.bundle.md` for exact content and link destinations.
