# I05:E05 W03 Session Isolation — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

A session's config directory cannot deliver a hook the eval did not write. The preflight refuses an installed plugin and its remote-settings enablement, and the transcript read refuses a session that carried context the run did not supply. A `settings.json` carrying a `hooks` block reaches a session through neither check, so a directory the eval writes can still deliver a hook before the read that would catch it.

This record holds the delivery of #402: the preflight refuses a settings file that declares a hook, naming the file and its events, with the tests that hold the refusal and its boundary against a file holding only preferences.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W03 work item](w03.md) | The preflight refusal for a settings file's hook, its boundary against a file of preferences, and the checks it requires |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E05 Deferred Debt](https://github.com/m2ux/prosiform/issues/374) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Issue | [#402](https://github.com/m2ux/prosiform/issues/402) — the deferred refusal this task delivers |
| Raised by | [W08 delivery](https://github.com/m2ux/prosiform/pull/400) |
