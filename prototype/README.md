# Prototype

The Python build of prosiform.

It establishes the behavioural contract, runs the [fixture corpus](../fixtures/README.md), and stays in use as a differential oracle once the production build exists.

## Environment

`pyproject.toml` declares the supported Python version and the build's dependencies. `uv.lock` records the exact version and hash of every package those dependencies resolve to, so two checkouts install the same tree.

```bash
cd prototype
uv sync --frozen
```

`--frozen` installs what the lockfile records and resolves nothing, so a dependency change reaches an environment only by way of a lockfile change. `uv sync --check` reports an environment whose versions have drifted from the lockfile. `uv lock` rewrites the lockfile after an edit to `pyproject.toml`.

| Declared | Value | Why |
| --- | --- | --- |
| Python | `>=3.13` | The version the environment is created with and the one continuous integration runs. |
| [`markdown-it-py`](https://pypi.org/project/markdown-it-py/) | `==4.2.0` | The parser the `skill-markdown-v1` profile is configured on. Its `commonmark` preset with the `table` and `strikethrough` rules enabled gives the profile's pipe tables and double-tilde strikethrough; its typographer stays off, which is the profile's disabled typographic substitution; it leaves source task-list markers as text rather than generating checkbox HTML; and it emits raw HTML as its own token, which is what lets the build refuse it. |

`mdurl` is resolved as `markdown-it-py`'s own dependency. The profile needs no parser plugin, so `mdit-py-plugins` is not declared: pipe tables and strikethrough are core rules of the parser, and preserving task-list markers means leaving the plugin that renders them out.

## Packaging

The wheel carries [`docs/glossary.md`](../docs/glossary.md) at `prosiform/docs/glossary.md`, so the vocabulary the tool's diagnostics use travels with an installed build rather than only with the source tree.

```bash
uv build --wheel
```

## Layout

| Path | Holds |
| --- | --- |
| `pyproject.toml` | The project definition: the supported Python version, the dependencies and the package data. |
| `uv.lock` | The exact resolved version and hash of every package. |
| `src/prosiform/` | The package. |

The commands that run this build's tests and static checks are a later task.
