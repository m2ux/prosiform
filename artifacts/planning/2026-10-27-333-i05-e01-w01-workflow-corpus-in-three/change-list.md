# W01 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| The corpus tests sit beside the reader in `evals/diagram-following/`, not in a `tests/` directory. | Trivial: a second `conftest.py` would give mypy two modules named `conftest`; beside the reader, pytest's own path handling imports it. |
| The AC1 test bundles with the `pf` on the locked environment's path rather than `PROSIFORM_BUILD`. | Trivial: the eval measures this checkout's bundle, and `make harness` runs in that environment, so it needs no configured build. |
| `checks/layout.py` requires `evals/`, and `checks.md` and `src/README.md` describe the harness and layout as they now run. | In scope: the brief admits the tree; no check's rule changes. |

## Held

None.
