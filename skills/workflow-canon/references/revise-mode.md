# Revise Mode

Changes the skill itself: its entry point, mode files, shared guides, commands and templates.

## Prerequisites

Before the first command spec, read the [command conventions](command-conventions.md#common).

## Procedure

1. **Read the guidelines.**
   Read the [skill guidelines](../../guidelines.md) and this skill's [guidelines](guidelines.md) whole before the first edit.
2. **Understand the request.**
   Resolve missing decisions with the user until the change and its scope are clear. Find the rule's home, its consumers, and any script, template or test that states it. The workspace branch owns the skill and shared guidelines. Locate a shared [planning record](planning.md) when the revision needs planning artifacts.
3. **Work in a worktree.**
   [Create Skill Worktree](#create-skill-worktree) for the change.
4. **Revise.**
   Make the change in its authoritative home and update every consumer. Apply the guidelines' layout, prose, link and command rules while writing.
5. **Check the guidelines.**
   Read each changed file against both guidelines: discovery description, mode summaries, bold leads, one line per item, single rule homes, command links, resolved file links and anchors, and [progressive disclosure](../../guidelines.md#progressive-disclosure).
6. **Verify.**
   - Confirm frontmatter opens and closes with `---`, contains the required fields and names the skill's folder.
   - [Run Skill Checks](#run-skill-checks), [Check Skill Summaries](#check-skill-summaries) and [Run the Edit Guard Tests](canon-context.md#run-the-edit-guard-tests). Changes to shared rules or templates also run their affected consumer suites.
   - Walk a representative request through each changed decision.
   - For every affected mode, apply [disclosure verification](../../guidelines.md#disclosure-verification) using the skill's [representative scenarios](guidelines.md#progressive-disclosure).
7. **Deliver.**
   [Commit Skill Changes](#commit-skill-changes) for each distinct change, then [Push Skill Branch](#push-skill-branch). When requested, [Open Skill Pull Request](#open-skill-pull-request). Report the files, validation and delivery link.
8. **Revise the guidelines.**
   When the user states an authoring rule, put it in the [skill guidelines](../../guidelines.md) if it binds every skill, or this skill's [guidelines](guidelines.md) if it binds only this one.

## Rules

- **Complete.**
  A revision is complete only when it conforms to both guidelines, its links resolve, applicable checks pass and [disclosure verification](../../guidelines.md#disclosure-verification) succeeds for every affected mode.
- **Scope.**
  This mode changes the skill; an example integration is reviewed only as far as needed to validate the requested revision.

## Commands

### Create Skill Worktree

Create the skill's branch in its own worktree from its repository's current target.

```bash
git fetch <remote> <target-branch>
git worktree add <skill-worktree> -b <revision-branch> <remote>/<target-branch>
```

### Run Skill Checks

Validate the skill's structure and run the checks its repository and changed resources require.

- Run from the worktree containing the edits. Discover relevant test folders and use [Run Project Check](command-conventions.md#run-project-check) for their actual commands; choose additional suites from the affected consumers.
- Inspect every local Markdown link and heading anchor, frontmatter and unfinished scaffold text. If an installed skill validator is available, run it too.
- A behavioral walkthrough follows [Revise](revise-mode.md#procedure); mechanical checks alone do not establish instruction quality.

```bash
git diff --check
```

### Commit Skill Changes

Commit the intended change set with a message describing the resulting behavior.

- Stage every changed rule home and consumer, including shared guidelines, moved or removed paths, templates and tests. Inspect the staged diff against the request before committing; leave unrelated work unstaged.

```bash
git add -- <changed-path> <other-changed-path>
git diff --cached --stat
git commit -F <message-file>
```

### Push Skill Branch

Publish the skill branch with a plain push to its matching remote branch.

- Check the current branch before setting its tracking configuration. A non-fast-forward rejection needs the repository's branch-rewrite decision.

```bash
git branch --show-current
git config branch.<revision-branch>.remote <remote>
git config branch.<revision-branch>.merge refs/heads/<revision-branch>
git push
```

### Open Skill Pull Request

Open the requested PR against the repository's chosen target with a reviewed body file.

```bash
gh api --method POST repos/{owner}/{repo}/pulls -f title='<title>' -f head='<revision-branch>' -f base='<target-branch>' -F body=@<body-file>
```

### Check Skill Summaries

Run the shared mode-summary tests from the checkout containing its skills.

- Run from the workspace checkout containing the skill under revision.

```bash
python3 -m unittest discover -s skills/work-planner/test -p test_modes.py
```
