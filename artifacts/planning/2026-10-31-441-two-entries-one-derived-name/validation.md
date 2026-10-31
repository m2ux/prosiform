# Validation — 441 Two Entries and One Derived Name

> Evidence record · Created 2026-10-31

The worktree is `.worktrees/i05/e09/w11-guide-sentence`, cut from `i05/e09/main` at `52ebf130`. The build under test is the repository's own `pf`.

## T1 — Two entries deriving one name publish one joined folder

**Ran:** from a directory holding `a/b.md` and `a_b.md`, each a document of one heading and one paragraph:

```bash
pf -o . a/b.md a_b.md
```

**Observed:** exit `0`, one folder `a_b+a_b.bundles/` holding one bundle `a_b+a_b.bundle.md`. Nothing was refused and nothing was left unwritten.

The joiner is the `+` between each selection's derived name, so the two entries are distinguished by the name the Combined selection rule already states. The run makes no refusal to make.

## T2 — The command and declaration tables are unchanged

**Ran:** `python3 checks/tables.py`.

**Observed:** exit `0`, `table check: 21 command(s) and 8 declaration(s), each declared by the project and named by a table`.

## T3 — No local link broke

**Ran:** `python3 checks/links.py`.

**Observed:** every local link `ok`. The failures are the remote addresses in `README.md` and `checks.md`, each reported as `remote, and --online was not given` — the flag the sandbox cannot use, not a broken link.

## T4 — The guide now agrees with the design

**Read:** the design's Combined selection row, at the revision `README.md` pins (`a59b62fc`): multiple selections "produce one bundle, in a run folder of the same name, whose name joins each selection's name in command-line order".

**Observed:** the corrected sentence in `docs/bundles.md` states the same thing. The guide contradicted the design before this change; it agrees with it now.
