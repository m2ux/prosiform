# I05:E01:W08 Session Isolation — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

This record holds the delivery of I05:E01 W08: a session is given one form of one workflow and the instruction, and nothing else. The eval's own config directory had been injecting another repository's rules into every session, so a pass measured an agent obeying a second instruction set that arrived alongside the form.

The task refuses a config directory holding an installed plugin, reads what each session's transcript carries before its first turn, and states in the eval's README which mechanism keeps a session to its form.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W08 work item](w08.md) | The preflight refusal, the injected-context read and the stated boundary |
| [W08 validation](validation-w08.md) | The test-plan results, the mutation checks and the limitations |
| [W08 change list](change-list-w08.md) | What this delivery applied, and what it held |

## Decisions

- **The login stays in the config directory.** The plugin and remote settings arrive under `CLAUDE_CONFIG_DIR` because that is where the OAuth login lives. Moving the login to `apiKeyHelper` through `--settings` would let the directory carry nothing the eval did not write, but the preflight refusal and the injected-context read already refuse or report what reaches a session, and no run's authentication changes. (User, 2026-10-29.)

## Boundary Held

Each part of the boundary names the mechanism that holds it, and for the first two, the file its refusal names.

| Part | Mechanism |
| --- | --- |
| The caller's configuration and memory | `CLAUDE_CONFIG_DIR` names the eval's directory, and every `CLAUDE*` and `ANTHROPIC_*` variable is dropped |
| MCP servers, slash commands and skills | `--strict-mcp-config` and `--disable-slash-commands` |
| Every tool past the five the form needs | `--tools Read,Write,Edit,Glob,Grep`, with `--permission-mode acceptEdits` for writes |
| A plugin installed in the directory | Refused by `preflight`, naming `plugins/installed_plugins.json` |
| A plugin enabled by remote settings, and its `env` | Refused by `preflight`, naming `remote-settings.json` |
| Context the agent added anyway | Read from each session's transcript, which fails the run naming the session and what it carried |

The login stays in the config directory, so `--bare` is not used: it would stop reading the OAuth login.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Diagram Following planning record](../2026-10-27-333-i05-e01-diagram-following-eval/README.md) |
| Task issue | [#395](https://github.com/m2ux/prosiform/issues/395) |
| Predecessor | [#393](https://github.com/m2ux/prosiform/pull/393) — the linked form and `errored` class this boundary is measured over |
| Review pull request | [#353](https://github.com/m2ux/prosiform/pull/353) |
| Pull request | [#400](https://github.com/m2ux/prosiform/pull/400) — delivered and merged |
| Deferred debt | [#402](https://github.com/m2ux/prosiform/issues/402) — a settings file's hook, held for I05:E05 |
