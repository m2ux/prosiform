# Validation — I05:E06 W02

The checks ran on branch `i05/e06/w02-authoring-check-reporting-findings` at `256a032f`. The branch was cut from `i05/e06/main` at `6dc691dd`. `PROSIFORM_BUILD` was set to `uv run --project <worktree>/src --frozen pf`.

## T1 Authoring Check Tests

`checks/tests/test_authoring_check.py` has 15 cases and observes AC2. All 15 pass.

- **One failing case per finding kind.**
  - **Inputs and Outputs.** A prose Inputs line and a missing Outputs line. A link with no contract fragment. An Inputs line running onto a second line.
  - **Commands section.** A `## Commands` section with the command beneath it, which is both a Commands section finding and a placement finding.
  - **Command placement.** A command fenced under Fields, which is outside a step.
  - **File-relative links.** An absolute link, a link written from the declared root, and a repository URL to a file the checkout holds.
- **Cases that report nothing.**
  - A file meeting every rule. It includes a command in a single-step operation and a template fence holding a `## Commands` heading.
  - A command in a step's unindented fenced block.
  - A guidelines-like file that names the Commands rule in prose and has no `## Commands` heading.
  - Links written inside a code span or a fenced block.
- **Indented fence.** An indented fenced command inside a step is a finding.
- **Size report.** A file of 9 operations is listed and one of 8 is not. A file of 20,481 bytes is listed and one of 20,480 is not.
- **Areas.** Each document is placed in exactly one area.

Result: Pass.

## T2 Findings Scan

`make authoring` ran over `example/work-planner/` and observes AC2.

- It read 58 documents, reported 431 findings and exited 1.
- [Findings scan](findings.md) records the findings by area, kind and file, with the size report.
- `guidelines.md` raises no Commands finding and appears only in the size report, as W01 noted.

Result: Pass, since the check reports and exits as specified.

## T3 Harness

`make harness` reported `758 passed`. That is the 743 earlier tests plus this check's 15.

Result: Pass.

## T4 Repository Checks

`make check` exited 0. Each of its checks passed:

| Check | Output |
| --- | --- |
| ruff | `All checks passed!` |
| format | `69 files already formatted` |
| mypy | `no issues found in 68 source files` |
| tests | `1302 passed` |
| harness | `758 passed` |
| corpus | 342 pass |
| smoke | passed |
| layout | passed |
| tables | 19 commands, `make authoring` named by `checks/README.md` |
| links | 106 documents |
| vocabulary | passed |
| invocation | passed |
| conformance | passed |
| independence | passed |
| steps | 58 documents |

Result: Pass.
