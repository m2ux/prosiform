# Validation

Tested revision: `446f70e9b3c08562b20b7b586233b09412bfa0fc`, based on epic revision `c876051`.

## Documented commands and diagrams

Passed. [verify-examples.py](verify-examples.py) executes all 14 compiler command occurrences in README.md, invocation.md and example/README.md, including the three file-producing diagram commands. Five usage fixtures compare byte for byte; eight Markdown excerpts match the actual bundles or their source excerpts. Both diagram heading lists match the emitted headings, and the retained planning SVGs match the published SVGs byte for byte.

Run from the task worktree with `PYTHONPATH` pointing to its `src` and `PROSIFORM_BUILD` set to the installed console entry point:

```text
python verify-examples.py /absolute/path/to/task-worktree
```

The run used the existing W04 Python 3.13 environment and the W08 source tree. Every compiler command returned zero. The grouped work-tracker output contains Overview and member headings; grouped my-skill places Agents and Common directly under Rules. Deferred source paths retain their original spelling.

Rendered with the repository's existing tooling:

```text
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 1500 docs/images/compilation.svg docs/images/compilation.png
QT_QPA_PLATFORM=offscreen ksvgtopng 1800 840 docs/images/agent-rules.svg docs/images/agent-rules.png
```

Both PNGs were visually inspected: titles fit their panels, source filenames remain lowercase, and emitted headings read Procedure, Rules/Agents, Rules/Common, Tips, Rules/Codex and Rules/Claude.

## Local checks

Passed: 754 source tests; 606 harness tests with one existing skip; all 251 corpus fixtures; lint, formatting, type checking, layout, command tables, vocabulary, invocation, conformance and independence.

```text
python -m pytest -c src/pyproject.toml src/tests
make lint format-check typecheck harness corpus layout tables vocabulary invocation conformance independence UV_RUN=
git diff --check
```

The commands used the existing installed tools on PATH and the task worktree source through PYTHONPATH. An initial source-test invocation lacked the console entry point on PATH; all tests passed after supplying that environment. No product failure was found. Lock, installed-wheel smoke and online links are covered by the remote full check set.

## GitHub checks

Pending the exact-head Checks workflow, which runs `make check` including lock validation, installed-wheel smoke and online link checks.

## Delivery verification

Pending merge. Auto-close was confirmed disabled by the user. Actual Development-field access remains unavailable; the user authorized proceeding through the recorded issue and PR links. W08 has no task issue and its task PR needs no Development relation. Epic review #198 stays draft.
