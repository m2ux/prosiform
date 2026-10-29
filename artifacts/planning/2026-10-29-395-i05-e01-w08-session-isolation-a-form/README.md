# I05:E01:W08 Session Isolation — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

This record holds the delivery of I05:E01 W08: a session is given one form of one workflow and the instruction, and nothing else. The eval's own config directory had been injecting another repository's rules into every session, so a pass measured an agent obeying a second instruction set that arrived alongside the form.

The task refuses a config directory holding an installed plugin, reads what each session's transcript carries before its first turn, and states in the eval's README which mechanism keeps a session to its form.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W08 work item](w08.md) | The preflight refusal, the injected-context read and the stated boundary |

## Decisions

- **The login stays in the config directory.** The plugin and remote settings arrive under `CLAUDE_CONFIG_DIR` because that is where the OAuth login lives. Moving the login to `apiKeyHelper` through `--settings` would let the directory carry nothing the eval did not write, but the preflight refusal and the injected-context read already refuse or report what reaches a session, and no run's authentication changes. (User, 2026-10-29.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Diagram Following planning record](../2026-10-27-333-i05-e01-diagram-following-eval/README.md) |
| Task issue | [#395](https://github.com/m2ux/prosiform/issues/395) |
| Predecessor | [#393](https://github.com/m2ux/prosiform/pull/393) — the linked form and `errored` class this boundary is measured over |
| Review pull request | [#353](https://github.com/m2ux/prosiform/pull/353) |
