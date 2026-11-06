# Release record: the version the previous corpus selects

> Measured 2026-11-06

## What was run

The `contract/v0.15.0` corpus was run against the build at `origin/main` (`fb17c2c97524b649dc4b619f1b88cd825a797d85`), which reports `pf 0.16.0 (prosiform-markdown)`.

```bash
git worktree add --detach .worktrees/release/corpus-v0.15.0 contract/v0.15.0
git worktree add --detach .worktrees/release/main origin/main
cd .worktrees/release/corpus-v0.15.0
env -u VIRTUAL_ENV PROSIFORM_BUILD=<release build>/src/.venv/bin/pf \
  uv run --project src --frozen python checks/corpus.py
```

The corpus is the 312 fixtures `contract/v0.15.0` (`240268522ccddc15801a80a821b0f7a9faff6e82`, `Declare Python build version 0.15.0`) holds.

## Result

```text
corpus check: 312 fixture(s), 7 pass, 305 fail, 0 awaited, 0 unexpected pass
```

The run's complete output is [the corpus log](corpus-v0.15.0.log).

The 305 failures fall into two groups:

| Group | Fixtures | What the build answers |
| --- | --- | --- |
| A positional entry reference | 295 | `E_INVALID_USAGE: unrecognized arguments: <ref>`, because the build takes `--entry REF` and no positional reference |
| The retired CLI surface | 10 | `pf -h` no longer prints `pf [OPTIONS] REF [REF ...]`, `-v` prints `(prosiform-markdown)` where the fixture expects `(skill-markdown-v3)`, `-f` is absent, and a diagnostic message no longer names `note.md` |

The 7 fixtures that pass are the ones whose subject is a refusal no grammar reaches: three CLI refusals, the unknown-diagnostics-format refusal, the output-naming-an-input refusal, and the two limit overrides.

## Selected version

`docs/versioning.md` settles the number by running the previous revision's corpus against the new build. 305 fixtures fail, so the change is a major one under [What the numbers mean](https://github.com/m2ux/prosiform/blob/main/docs/versioning.md#what-the-numbers-mean), and below `1.0.0` the minor carries what the major would:

```text
0.15.0  →  0.16.0
```

The contract and build tags for it are `contract/v0.16.0` and `python/v0.16.0`.

## What this record does not cover

`main` already declares `version = "0.16.0"` in `src/pyproject.toml` and the `prosiform` entry of `src/uv.lock`, set by `98763ec4b` (`2026-10-30`). No `contract/v0.16.0` or `python/v0.16.0` tag exists; the highest tags in this repository's history are `contract/v0.15.0` and `python/v0.15.0`.

The measurement confirms the number `main` declares rather than moving it. Whether the release branch carries a version commit of its own beyond `main` is the next row's question, and `main` already holding that change means the row's stated one-commit shape does not hold as written.
