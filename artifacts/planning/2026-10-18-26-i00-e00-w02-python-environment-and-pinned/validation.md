# Validation

The environment setup run this task carries, as it was run. It was run on a clean checkout of the tested revision, with no environment present, and then run again against an environment deliberately moved off the recorded version, so a pass is known to mean something.

| Field | Value |
| --- | --- |
| Repository | `m2ux/prosiform` |
| Branch | `i00/e00/w02-python-environment-and-pinned` |
| Tested revision | `0d6385995523697ea895c5c8f211eec5e8d50f7b` |
| Clean location | `git archive HEAD` extracted to an empty directory outside the worktree, so no `.venv`, no `dist/` and no build output came with it |
| Run from | `prototype/` in that extracted tree |
| Toolchain | `uv 0.11.14`, system CPython 3.13.7 at `/usr/bin/python3.13` |
| Network | Available. Packages were served from uv's local cache, which holds the same artifacts the lockfile's hashes name. |
| Date | 2026-10-18 |

## T1 Environment setup run

**Observes AC2.** A fresh checkout installs the Python build's dependencies at the exact versions the lockfile records.

```bash
uv sync --frozen
uv pip list
```

**Pass.** Exit 0. The virtual environment did not exist before the command and was created by it. The three packages installed are the three the lockfile records, at the versions it records.

```text
Using CPython 3.13.7 interpreter at: /usr/bin/python3.13
Creating virtual environment at: .venv
Prepared 3 packages in 293ms
Installed 3 packages in 4ms
 + markdown-it-py==4.2.0
 + mdurl==0.1.2
 + prosiform==0.0.0 (from file:///…/clean/prototype)
```

```text
Package        Version
-------------- -------
markdown-it-py 4.2.0
mdurl          0.1.2
prosiform      0.0.0
```

`uv.lock` records `markdown-it-py` at `4.2.0` and `mdurl` at `0.1.2`, each with the sha256 of the wheel and the sdist it may come from. The installed versions are those two.

## T2 The same check against a differing version

**Observes AC2.** The agreement the setup run reports is an observation, not an assumption: the check fails when an installed version differs from the recorded one.

```bash
uv sync --frozen --check
uv pip install markdown-it-py==3.0.0
uv sync --frozen --check
```

**Agrees on the synced environment.** Exit 0.

```text
Checked 3 packages in 0.08ms
Would make no changes
```

**Fails when a version differs.** With `markdown-it-py` moved to `3.0.0` in the environment, the same check exits 1 and names both the version present and the version recorded. The environment was restored with `uv sync --frozen` afterwards.

```text
Would uninstall 1 package
Would install 1 package
 - markdown-it-py==3.0.0
 + markdown-it-py==4.2.0
The environment is outdated; run `uv sync` to update the environment
```

**What it establishes and what it does not.** `--frozen` makes the lockfile the only input: the command resolves nothing, so what it installs is what the lockfile records and nothing else. The check compares the environment with the lockfile, so it catches a version that drifted after the sync; it does not assert that the lockfile agrees with `pyproject.toml`, which is what `uv lock --check` is for and which W04 is the natural place to run on every change.

## T3 The glossary in an installed build

**Carries a clause of AC6.** The glossary is published with the build, not only with the source tree.

```bash
uv sync --frozen --no-editable
python -c "from importlib.resources import files; files('prosiform').joinpath('docs/glossary.md')"
uv build --wheel
```

**Pass.** The non-editable install places the glossary inside the installed package, and its bytes are those of `docs/glossary.md` in the source tree.

```text
installed path: …/.venv/lib/python3.13/site-packages/prosiform/docs/glossary.md
exists: True bytes: 5759
sha256 installed: d6a55d17058a55da78dace83550f4e059e7314dc24db25cc293ffe95e2261eab
sha256 source   : d6a55d17058a55da78dace83550f4e059e7314dc24db25cc293ffe95e2261eab
identical: True
```

The built wheel holds the same file:

```text
prosiform/__init__.py                           245
prosiform/docs/glossary.md                     5759
prosiform-0.0.0.dist-info/METADATA             2641
```

`pip install ./prototype`, the command the root README documents, was run into a separate `venv` and produced the same result: `markdown-it-py 4.2.0`, `mdurl 0.1.2`, `prosiform 0.0.0`, and the glossary present at 5,759 bytes.

**What it establishes and what it does not.** The wheel target force-includes a path above the project root, so the glossary reaches a wheel built from the checkout. An sdist built from `prototype/` alone would carry no such path, so a wheel built from an sdist would not hold the glossary; the build is installed from the checkout, and no sdist is published.

## Each dependency against the profile

The profile the dependency set must satisfy is `skill-markdown-v1`. Each clause was run against `markdown-it-py 4.2.0` rather than taken from its documentation.

| Profile clause | Observed |
| --- | --- |
| Pipe tables | `MarkdownIt("commonmark").enable("table")` emits `table_open` … `table_close`. A core rule; no plugin. |
| Double-tilde strikethrough | `.enable("strikethrough")` renders `~~gone~~` as `<s>`. A core rule; no plugin. |
| Source task-list markers preserved | `- [ ] todo` and `- [x] done` survive into the output as text, with no `<input>` generated. This is the parser's behaviour without the `tasklists` plugin, so the profile is met by leaving that plugin out. |
| Typographic substitution disabled | `md.options["typographer"]` is `False` by default; `"quoted"`, `--` and `...` are emitted unchanged. |
| HTML recognized so it can be refused | Raw HTML arrives as an `html_block` token rather than as paragraph text, so the build can fail on it. |

**`mdit-py-plugins` is not declared.** The three syntax clauses it might have supplied are core rules of the parser or are met by omitting a plugin, so the package would be carried rather than required.

**`mdurl` is not declared.** It is `markdown-it-py`'s own dependency; the lockfile records it, and nothing in the build imports it directly.
