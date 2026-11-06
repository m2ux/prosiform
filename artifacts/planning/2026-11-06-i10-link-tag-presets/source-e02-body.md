## Overview

The eval's preflight refuses a config directory whose `settings.json` declares a hook, and Claude Code reads further settings files by project scope, discovered from a session's working directory rather than from the config directory. The preflight reads none of them, so a session's own tree can deliver a hook before the read that would catch it, and the read that does catch it spends the sessions first. This epic reads every scope a session will see, before it starts.

## Problem

- **Hooks arrive by project scope, and the preflight reads only the config directory.**
  A `hooks` block in a workspace's `.claude/settings.json` or `.claude/settings.local.json` reaches a session exactly as one in the config file does, and the [preflight](https://github.com/m2ux/prosiform/blob/23882b7d9c4faa78407468072a9eee1f8baeba4c/evals/diagram-following/harness.py#L203-L235) reads neither.
- **The session's workspace is copied from a corpus form's tree.**
  A form whose tree carries `.claude/settings.json` delivers its hooks to every session of that form.
- **An ancestor `.claude` is project scope too.**
  The eval root defaults to a directory under the caller's home, and project discovery walks up from the working directory, so the caller's own settings are read as the project's for every workspace.
- **The host's managed settings reach every session.**
  Claude Code reads a managed settings file from a system path whatever the config directory names, and no run states what it carried.
- **The read that catches it pays for the sessions first.**
  A run is refused after a session's hook response is observed, where a preflight refusal costs nothing.

## Proposal

- **The preflight reads every scope a session will see.**
  It reads the config directory's file, each workspace's two project-scope files and the `.claude` settings of every directory above the workspaces, and names whichever file it refuses and the events that file declares.
- **An ancestor declaring a hook is refused and named.**
  A `.claude` directory between the workspaces and the filesystem root is project scope, so a run refuses one whose settings declare a hook, naming it and `--eval-root` as the remedy; a bare ancestor directory refuses nothing.
- **The host's managed settings are recorded.**
  The run reads the host's managed settings file, at a path the harness holds so a test can plant it, and records the file and the events its hooks declare in the run record; the sessions start, since the managed scope is the host administrator's (user, 2026-11-03).
- **Each file is planted by a test.**
  Stub-agent tests plant a `SessionStart` hook in each workspace file, and in an ancestor and assert the refusal, the empty stub log and the absent results folder; another holds an ancestor declaring none and asserts its session starts; another plants a managed settings hook and asserts the sessions start and the run record names it.
- **The README states each scope.**
  The Isolation section names each settings file the preflight refuses, the scope it is read from, and `--eval-root` as the remedy for one above the workspaces.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Done |
| --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/pull/598) | Every project-scope settings file refused | AC1, AC2, AC3 | | | ✓ |
| [W02](https://github.com/m2ux/prosiform/pull/599) | Managed settings hook recorded | AC4 | W01 | | ✓ |
| [W03](https://github.com/m2ux/prosiform/pull/601) | The settings the preflight reads | AC5, AC6 | W02 | | ✓ |
| [W04](https://github.com/m2ux/prosiform/pull/602) | The check catalogue states every refused scope | AC7 | W03 | | ✓ |

## Acceptance Criteria

- [x] **AC1.** A run whose session workspace's `.claude/settings.json` or `.claude/settings.local.json` declares a hook is refused before its first session starts, naming the file and the events it declares, as a stub-agent test `make check` runs shows.
- [x] **AC2.** A run whose workspaces and their ancestors hold no `.claude` settings file declaring a hook starts its sessions, as a stub-agent test `make check` runs shows.
- [x] **AC3.** A run under a `.claude` directory between the session's workspace and the filesystem root whose `settings.json` or `settings.local.json` declares a hook is refused before its first session starts, naming that file and `--eval-root` as the remedy, as a stub-agent test `make check` runs shows.
- [x] **AC4.** A run on a host whose managed settings file declares a hook starts its sessions, and its run record names that file and the events it declares, as a stub-agent test `make check` runs shows.
- [x] **AC5.** The eval's README states each settings file the preflight refuses and the scope it reads that file from, as an inspection of the README against the preflight shows.
- [x] **AC6.** The eval's README names `--eval-root` as the remedy for a refused settings file above the workspaces, as an inspection of the README against the preflight shows.
- [x] **AC7.** The eval runner entry of `checks.md` names every settings scope the runner check refuses, the form tree's and each workspace ancestor's `.claude` settings beside the config directory, as an inspection of `checks.md` against the preflight shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-01-464-i10-evaluation-and-checks) — the design, the work items, the joins and the planning decisions.
- **R2.** [Session isolation validation](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-29-402-i05-e05-w03-session-isolation-a-settings/validation.md) — the limitation this epic is raised from.
- **R3.** [Settings files and precedence](https://code.claude.com/docs/en/settings) — the settings files, their scopes, and how the config directory relocates the user file.
