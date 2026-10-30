# W03 and W04 Change List

Plan changes arising in delivery. Allowance: none, so every non-trivial change is held for the planner.

## Applied

| Change | Reason |
| --- | --- |
| The design's profile statement names `skill-markdown-v2`, in the same `engineering` commit as the Examples rule. | The design otherwise named `skill-markdown-v1` beside a rule only `skill-markdown-v2` holds. |
| The README's profile badge links the design at `e1b82283`, not `5e6192d`. | That link is the ref `make vocabulary` and `make conformance` read the design from, so it names the revision stating the diagram rule. |
| The glossary's **reference** covers a `mermaid` click destination naming a local document or section. | It defined a reference as a Markdown link alone, which a click destination is not. |
| `profile.py`'s docstring gains a paragraph stating that a code block carries no use except a `mermaid` click destination. | The brief's docstring correction; the module stated no use rule before, only that a code block carries no unsupported-construct spelling, which still holds. |
| The harness test refusing another profile's version response (`test_runner.py`) declares `skill-markdown-v2` and replays `skill-markdown-v1`. | It used `v2` as the mismatching identifier, which is now the current one. |

## Held

| Change | Reason |
| --- | --- |
| The next release bumps the build's minor (to at least `0.12.0`); `src/pyproject.toml` stays `0.11.0` here. | `docs/versioning.md` makes a profile change a contract major, which below `1.0.0` bumps the minor, and the previous contract's `cli/informational-version-response` fixture fails against this build. The release process sets the bump from that old-corpus run, so no task branch moves it. |
