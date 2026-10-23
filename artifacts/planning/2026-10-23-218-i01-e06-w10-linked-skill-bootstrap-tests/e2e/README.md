# Linked Skill Bootstrap Runs

These runs are the installed-command evidence for the linked skill suite. The skill entry is read from disk. Each of its three links is a separate `pf` process. The wheel is `prosiform-0.9.0-py3-none-any.whl`, installed outside the repository. The command reports `pf 0.9.0 (skill-markdown-v1)`. The source commit is `b6b505366e7f57d8912c3254f33fbc47a1e08ecf`.

Entries are paths relative to the caller directory. A target outside that directory is reached with a parent-relative path, which the command accepts. A leading slash is a path the source root cannot contain.

## Artifact inventory

The [artifact inventory](runs/b6b505366e7f57d8912c3254f33fbc47a1e08ecf/inventory.md) links every run to its source tree, command, diagnostics and bundle. [Compiler identity](runs/b6b505366e7f57d8912c3254f33fbc47a1e08ecf/compiler.json) records the wheel, the version response and the source commit. A run that publishes nothing records `not produced` and keeps its diagnostics.

## Three linked targets

[Independent compilations](runs/b6b505366e7f57d8912c3254f33fbc47a1e08ecf/test_three_skill_links_are_independent_compilations/) runs 01, 02 and 03 are Assemble, Review and Defaults. Assemble uses an explicit workspace root and the procedures group. Review uses the beta library root and the reviews group. Defaults declares no root, so its leaf comes from the caller directory. Each bundle contains that target's markers and group headings, and omits the other targets and the decoys.

## Publication and adverse runs

The same commit retains the other scenarios in the inventory:

- Absent roots follow a second caller directory.
- A section fragment keeps the entry file's root and drops the unselected introduction.
- Stdout, an explicit file and the derived filename carry one bundle.
- A repeated target is included once.
- Two parents with different explicit roots reach one absent-root source, and that source's leaf is the caller directory's leaf.
- A second compilation rewrites the same destinations.
- A group depth conflict and invalid depths publish nothing. Those rows link `bundle-absent.txt`.

## Project check

`make check` on `b6b505366e7f57d8912c3254f33fbc47a1e08ecf` passed. Pytest reported 1038 passed, the harness reported 614 passed, and the lock, lint, format, type, corpus, smoke, layout, table, link, vocabulary, invocation, conformance and independence checks completed.
