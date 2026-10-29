---
prosiform:
  root: "."
---
# Conventions

The prerequisites every mode's run shares: the session it starts in, where a command runs, how a result is read, and the values its examples use. Each is stated once here, and every step applying one links it.

## Session

Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.

## Repository

`gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.

## Bodies

- Bodies, long comments and commit messages always go through a file (`-F body=@file`), never inline, which avoids quoting. The file holds the exact intended text.
- Keep these files in a working directory outside the repository.

## Helper Invocation

A helper is a script in `<workspace>`, the checkout holding this skill. It runs from `<workspace>`, or the directory within it that its command names, under the sandbox invoked by its absolute path, `<workspace>/scripts/sbx`. A file kept outside `<workspace>`, such as a body file, is passed by its absolute path.

## Command Result

Read each command's exit code and output before the next step. A failing exit code, or a refusal the command reports, returns to the caller as an execution error or refusal before the work continues.

## Helper Result

A helper's written body exists only on a zero exit code. An invocation failure returns as a blocker, and only a successfully written body is published.

## Write Confirmation

Only a fresh re-read confirms a write: read the written object again and compare it with the intended state. The write's own output confirms nothing. A re-read that fails, or shows another state, leaves the write uncertain; that uncertainty returns to the caller, and the write is never retried as a different write.

- A list read can lag a write, so a written item confirms by its own read alone. An item still showing the preceding state has the same write repeated and that item read again.

## Boards

A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.

## Example Values

Substitute the real ones:

- `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
- `950` a pull request, `I07` and `I08` initiative numbers;
- board `9` a theme board, and `419167630` its Status field id;
- `1` the Initiative Template board, `13` a board copied from it;
- `14` the Proposals Template, `15` the Proposals board;
- `m2ux` the user.
- `<checkout>` any checkout of the project, a linked worktree included.
