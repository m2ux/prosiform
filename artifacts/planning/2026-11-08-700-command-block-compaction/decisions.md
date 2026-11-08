# Decisions

## Confirmed

- The bundle emits a command block without its `<big><pre>` and `</pre></big>` tags, without `**` enclosing a link's whole text, and with every character reference decoded. The source keeps the rendered form (user, 2026-11-08).
- The hot-fix is raised as `[F08]` (#700) on the Python board at `priority: 10`, and `contract/v0.23.0` and `python/v0.23.0` are cut after merge (user, 2026-11-08).

## Implementation Details

- Compaction applies inside a command block only, as F07's `command_block()` recognises it. Entities and bold elsewhere are emitted as written.
- `**` is unwrapped only where it encloses a link's whole text. Other emphasis in the block stays.
- `&#92;` decodes to `\`. At a line end it is a Markdown hard break, which leaves the line structure intact for a reader.
- The design's bundle transformations name the compaction, so Preservation holds against it; the amendment lands on `engineering` and is re-pinned.
- The bundle reparse reads a decoded `<name>` inside link text as inline HTML. The candidate checks accept it inside a compacted command block; source refusal of raw HTML is unchanged.
- F07's `a-command-block-is-carried-as-written` fixture is renamed for the compacted form and its expected bundle regenerated. That fixture failing under the previous corpus is what moves the minor.
- One pull request into `main`, opened as a draft and marked ready once review clears.

## Collision

- `2026-11-08-symbol-grammar-in-bundle` is an unraised hot-fix plan that rewrites `bundle.py`'s `§ Instructions` section and regenerates 432 expected bundles. It still names v0.21.0. Delivered together, the two contend for `bundle.py`, the expected bundles and the release number, so one lands and the other rebases.

## Review

- Fixed: the bundle doc's statement of which references decode, decoding through markdown-it's `UNESCAPE_ALL_RE` and `replaceEntityPattern`, and `LINE_FEED` imported from `source.py`.
- Rejected, as no skill source writes them: doubled or escaped backslashes around `&#92;`, references decoding to Markdown syntax, decoded HTML comments, an indented first line, and a block opening with a list marker. Each fails the run or changes only rendered output.
