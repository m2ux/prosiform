# Revise Mode

Changes the skill itself: SKILL.md, its modes, artifacts, references and scripts.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Read the Guidelines

Read the [shared skill guidelines](../../guidelines.md) and [skill guidelines](guidelines.md) whole before the first edit.

### 2. Understand the Request

Interview the user, putting each question as the [Rules](#rules) state, until the change and its scope are clear.

- Find every file the change touches: the rule's home, each file that cites it, and any script, docstring or test that states it.

### 3. Work in a Worktree

Branch a worktree for the change.

- Commit each distinct change as its own commit.

### 4. Revise

Make the change in the rule's one home.

- Link to it from every other file that needs it.
- Write it to the guidelines' layout, prose, link and command rules as it is written, not in a later pass.
- When the user states a new writing rule, add it to the applicable shared or skill-specific guidelines before validation and delivery.

### 5. Check Against the Guidelines

Read every changed file against the [shared skill guidelines](../../guidelines.md) and [skill guidelines](guidelines.md), checking:

- The [description](../../guidelines.md#frontmatter), when the skill's reach changed.
- [Layout](../../guidelines.md#layout).
- [Prose](../../guidelines.md#prose), with the skill's own [Prose](guidelines.md#prose), and [stale claims](../../guidelines.md#changes).
- [Commands](../../guidelines.md#commands).
- [Links](../../guidelines.md#links).
- [Progressive disclosure](../../guidelines.md#progressive-disclosure).
- Fix each departure.

### 6. Run Script Tests

When an executable script, its consumed template or a test changed, run the script tests from the work-planner directory in the supplied workspace checkout. Resolve `<workspace>` to that checkout, as [Helper invocation](#helper-invocation) states. Otherwise continue at [7. Check Skill Files](#7-check-skill-files).

```bash
cd "<workspace>/skills/work-planner" && "<workspace>/scripts/sbx" python3 -m unittest discover -s test
```

### 7. Check Skill Files

If the script tests ran, read their exit code and output before continuing. Correct any failure and repeat [6. Run Script Tests](#6-run-script-tests) until they pass.

- When SKILL.md changes, confirm its frontmatter opens and closes with `---` and holds `name` and `description`.

From the supplied workspace checkout, check every affected skill's Markdown structure and links as [Helper invocation](#helper-invocation) states. Resolve `<skill-directory>` to the affected skill's path relative to that checkout; supply one directory argument per affected skill.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py "<skill-directory>"
```

**Example:** Work Planner in the selected checkout.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py skills/work-planner
```

### 8. Verify Disclosure and Dependencies

Read the skill-file check's exit code and output. Correct any failure and repeat the affected checks from [6. Run Script Tests](#6-run-script-tests) before continuing.

- Apply [disclosure verification](../../guidelines.md#disclosure-verification) with the skill's [representative scenarios](guidelines.md#progressive-disclosure).
- Resolve every required file, command and heading without an implicit external dependency.

### 9. Deliver

Deliver only after the required checks and disclosure verification pass.

- Commit.
- Push.
- Report what changed in each file.

## Outcomes

- **The skill matches the request.**
  The user has the change they asked for in the skill, committed and pushed.
- **The guidelines hold.**
  The change agrees with the guidelines, and a new rule the user stated for how the skill is written is part of that change.

# Rules

What binds every mode, protocol and artifact operation, stated once here and linked by the step that applies it.

## Decisions

A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.

- A plain-language paragraph before the question gives the context the user needs to answer it.
- The question offers more than one choice. The recommended choice is marked on its option.
- Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
- The user can select Other and specify a response beyond the options.
- Use the native tool for presenting the question when one is available.

## Layers

Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.

## Execution

A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing. Calls run in order. A step's `⇉` call runs in a sub-agent, from any session, dispatched or not; its `⫽` calls run in sub-agents together, as the bundle's Prosiform section states, and those together never write to the same object.

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

# Artifacts

## Plan Change

### Fields

#### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.
