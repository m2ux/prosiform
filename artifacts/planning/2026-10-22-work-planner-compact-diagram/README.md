# Work Planner Compact Diagram

[Compact Diagram Review](work-planner-compact.review.md)

## Source

The [workspace skill](https://github.com/m2ux/prosiform/tree/032ea2e8e79eeec62f073e129e3692ca74fbc2e5/skills/work-planner) is copied into [work-planner/](work-planner/): 64 files, including 38 Markdown documents. The copy omits 24 Prerequisites sections, each through the next heading of equal or higher level. One stale internal link is repaired as recorded below. Other sections and non-Markdown files retain their source content.

[Source Manifest](source-manifest.json) records the source revision, source and copy hashes, and removed section ranges.

## Rendering

The [main-branch renderer](https://github.com/m2ux/prosiform/blob/560926e9c1817d601ec23efe6294bfdb45d9068a/scripts/render-diagram.py) uses `work-planner/SKILL.md` as its entry document with `--compact`, without grouping rules. Headings and links remain visible; other body content is represented by `…`. Exact output, diagnostics and compiler provenance accompany the diagram.

Compilation succeeds, opening all 38 Markdown files and producing a 283,084-byte bundle. The output budget is 1,048,576 bytes. From this folder, using a clean compiler checkout at the pinned revision:

```bash
/path/to/prosiform/src/.venv/bin/python /path/to/prosiform/scripts/render-diagram.py work-planner/SKILL.md --compact --max-output-bytes 1048576 --revision 560926e9c1817d601ec23efe6294bfdb45d9068a --output work-planner-compact
```

## Source Link Review

The copied `guidelines.md` links to `SKILL.md#conventions`, matching the entry document's Conventions heading. The source snapshot contains `SKILL.md#command-conventions`; the source manifest records the repair. The workspace originals are untouched.
