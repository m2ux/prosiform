# Diagram Renderer

`render-diagram.py` bundles one Markdown entry document and draws its opened source files beside the output. Each call produces one diagram. Local Markdown dependencies are discovered by Prosiform.

## Run

Use a clean Prosiform compiler checkout. In its `src/` directory, run `uv sync --frozen --no-dev` to install the compiler. From the repository root, use that environment's Python:

```bash
/path/to/prosiform/src/.venv/bin/python scripts/render-diagram.py /path/to/my-skill/SKILL.md --group rules:2 --output /tmp/skill-diagram
```

| Argument | Purpose |
| --- | --- |
| `document` | Entry Markdown file, such as `SKILL.md`. |
| `--output PREFIX` | Required output path prefix. Existing files with this prefix are overwritten. |
| `--root DIR` | Allowed source root; defaults to the entry document's directory. |
| `--group SLUG:DEPTH` | Grouping rule; repeat for distinct slugs. |
| `--section FRAGMENT` | Bundle one section of the entry document. |
| `--max-output-bytes N` | Compiler output-size budget in bytes; use a positive integer. |
| `--compact` | Retain headings and links; replace other body content with `…` in both image panels. |
| `--section-level N` | Keep titles through HN (1–6); deeper titles require links in their section or subsections. Defaults to all titles. |
| `--branch NAME` | Compiler branch; required for a detached checkout. Must point to its current commit. |
| `--revision SHA` | Require an exact compiler commit. |

Call the tool again for another document or grouping arrangement, using a different output prefix.

For a large document set, add `--compact`. It preserves heading levels, inline and reference links, autolinks and image references. Prose, lists and code examples collapse to placeholders between retained items. Exact stdout and diagnostics remain complete.

Compact mode affects the image, not the bundle size. If compilation exceeds the output budget, pass a larger limit, for example `--max-output-bytes 1048576`.

Use `--compact --section-level 3` to hide H4–H6 titles whose sections contain no links. This filter also works without compact mode. Inline links, reference links, autolinks and image references count; code examples do not. Both panels are filtered; saved stdout remains complete.

## Output

Each prefix produces `.svg`, `.review.md`, `.stdout.md`, `.stderr.txt`, `.command.txt` and `.run.json`.

The image header contains only the compiler branch and commit. The opening compiler paragraph appears under Entry Points in the review Markdown, alongside the command, image, exit status and diagnostics. The run record pins the compiler revision and hashes the source bytes and output.

The tool returns the compiler's exit status. A rejected bundle still produces review artifacts; a source file appears only if the compiler opened it. Deferred targets may be displayed without contributing content. The SVG simplifies Markdown formatting; consult `.stdout.md` for exact content and link destinations.
