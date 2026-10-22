# Validation

Documented-command verification revision: `2697757fcf6f2d96ee4bd182d8b02839c073ed8c`, based on epic revision `c876051`.

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

At implementation revision 446f70e9b3c08562b20b7b586233b09412bfa0fc, passed: 754 source tests; 606 harness tests with one existing skip; all 251 corpus fixtures; lint, formatting, type checking, layout, command tables, vocabulary, invocation, conformance and independence.

```text
python -m pytest -c src/pyproject.toml src/tests
make lint format-check typecheck harness corpus layout tables vocabulary invocation conformance independence UV_RUN=
git diff --check
```

The commands used the existing installed tools on PATH and the task worktree source through PYTHONPATH. An initial source-test invocation lacked the console entry point on PATH; all tests passed after supplying that environment. No product failure was found. The final revision clarifies one documentation sentence; all command and diagram comparisons were rerun successfully. Lock, installed-wheel smoke and online links are covered by the remote full check set.

## GitHub checks

Passed [Checks](https://github.com/m2ux/prosiform/actions/runs/39740025573/job/119694728292) at exact head 2697757fcf6f2d96ee4bd182d8b02839c073ed8c. The workflow ran the full make check set, including lock validation, installed-wheel smoke and online links.

## Delivery verification

PR #211 merged into i01/e02/main as aea9a90f5ba1b83b4f27cefe985ff68073e25b59. All documented-command, excerpt and diagram checks passed again at that merged revision; AC6 and W08 were then marked complete. Epic #195 is In Review and remains open. The updated review #198 cites every task merge and remains draft. Auto-close was confirmed disabled by the user. Actual Development-field access remains unavailable; the user authorized proceeding through the recorded issue and PR links. W08 has no task issue and its task PR needs no Development relation. Epic review #198 stays draft.

Target branch readback showed protected=false and protection.enabled=false; both detailed protection APIs reported the private-repository plan restriction. No review requirement was active. Checks passed at exact task head 2697757fcf6f2d96ee4bd182d8b02839c073ed8c, mergeability was clean, and the merge request specified that head. Historical coverage disagreements on #197/AC2 and #201/AC3 remain recorded; neither affects W08/AC6.
