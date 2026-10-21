# README compilation diagrams

- [Shared context](compilation.svg): selected documents, a recursive dependency, and deferred Codex and Claude rules under `rules/`.
- [Agent-specific rules](agent-rules.svg): each agent selects and compiles its applicable rules under a Rules group.

These editable SVGs record the approved designs from `main` commit `96f011d`. Published SVGs and PNGs reside in `docs/images/` on `main`.

Render with IBM Plex Mono installed:

```bash
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 1152 /absolute/path/compilation.svg /absolute/path/compilation.png
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 840 /absolute/path/agent-rules.svg /absolute/path/agent-rules.png
```
