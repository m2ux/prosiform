# Diagram renderer

`render-diagram.py` bundles one Markdown entry document and draws its opened source files beside the output. Each call produces one diagram. Local Markdown dependencies are discovered by Prosiform.

## Run

Use a clean Prosiform compiler checkout. In its `src/` directory, run `uv sync --frozen --no-dev` to install the compiler. From this engineering checkout, use that environment's Python:

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
| `--branch NAME` | Compiler branch; required for a detached checkout. Must point to its current commit. |
| `--revision SHA` | Require an exact compiler commit. |

Call the tool again for another document or grouping arrangement, using a different output prefix.

## Output

Each prefix produces `.svg`, `.review.md`, `.stdout.md`, `.stderr.txt`, `.command.txt` and `.run.json`.

The image header contains only the compiler branch and commit. The opening compiler paragraph appears under Entry Points in the review Markdown, alongside the command, image, exit status and diagnostics. The run record pins the compiler revision and hashes the source bytes and output.

The tool returns the compiler's exit status. A rejected bundle still produces review artifacts; a source file appears only if the compiler opened it. Deferred targets may be displayed without contributing content. The SVG simplifies Markdown formatting; consult `.stdout.md` for exact content and link destinations.
