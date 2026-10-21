# README compilation diagrams

- [Shared context](compilation.svg): root-level procedure and tips documents, and Agents and Common under Rules / Overview with deferred Codex and Claude rules under `rules/`.
- [Agent-specific rules](agent-rules.svg): each agent compiles its instructions and non-deferred dependencies under a Checks group.

These editable SVGs record the approved designs from `main` commit `b2c6ec8`. Published SVGs and PNGs reside in `docs/images/` on `main`.

Render with IBM Plex Mono installed:

```bash
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 1500 /absolute/path/compilation.svg /absolute/path/compilation.png
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 1600 /absolute/path/agent-rules.svg /absolute/path/agent-rules.png
```
