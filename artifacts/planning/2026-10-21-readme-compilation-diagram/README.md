# README compilation diagrams

- [Shared context](compilation.svg): root-level procedure and tips documents, and Agents and Common in separate document sections with deferred Codex and Claude rules under `rules/`.
- [Agent-specific rules](agent-rules.svg): each agent selects and compiles its applicable rules under its source path.

These editable SVGs show title-cased generated headings and source-spelled filenames. Published SVGs and PNGs reside in `docs/images/` on the build branch.

Render with IBM Plex Mono installed:

```bash
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 1500 /absolute/path/compilation.svg /absolute/path/compilation.png
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 840 /absolute/path/agent-rules.svg /absolute/path/agent-rules.png
```
