# Revise Mode

Changes the skill itself: SKILL.md, its modes, artifacts, references and scripts.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

1. **Read the guidelines.**
   Read the [shared skill guidelines](../../guidelines.md) and [skill guidelines](guidelines.md) whole before the first edit.
2. **Understand the request.**
   Interview the user, putting each question as the [Rules](#rules) state, until the change and its scope are clear.
   - Find every file the change touches: the rule's home, each file that cites it, and any script, docstring or test that states it.
3. **Work in a worktree.**
   Branch a worktree for the change.
   - Commit each distinct change as its own commit.
4. **Revise.**
   Make the change in the rule's one home.
   - Link to it from every other file that needs it.
   - Write it to the guidelines' layout, prose, link and command rules as it is written, not in a later pass.
   - When the user states a new writing rule, add it to the applicable shared or skill-specific guidelines before validation and delivery.
5. **Check against the guidelines.**
   Read every changed file against the [shared skill guidelines](../../guidelines.md) and [skill guidelines](guidelines.md), checking:
   - The [description](../../guidelines.md#frontmatter), when the skill's reach changed.
   - [Layout](../../guidelines.md#layout).
   - [Prose](../../guidelines.md#prose), with the skill's own [Prose](guidelines.md#prose), and [stale claims](../../guidelines.md#changes).
   - [Commands](../../guidelines.md#commands).
   - [Links](../../guidelines.md#links).
   - [Progressive disclosure](../../guidelines.md#progressive-disclosure).
   - Fix each departure.
6. **Verify.**
   - Run [Run Tests](#run-tests) when an executable script, its consumed template or a test changed.
   - When SKILL.md changes, confirm its frontmatter opens and closes with `---` and holds `name` and `description`.
   - Run [Check Skill Files](#check-skill-files) for every affected skill.
   - Apply [disclosure verification](../../guidelines.md#disclosure-verification) with the skill's [representative scenarios](guidelines.md#progressive-disclosure).
   - Resolve every required file, command and heading without an implicit external dependency.
7. **Deliver.**
   - Commit.
   - Push.
   - Report what changed in each file.

## Outcomes

- **The skill matches the request.**
  The user has the change they asked for in the skill, committed and pushed.
- **The guidelines hold.**
  The change agrees with the guidelines, and a new rule the user stated for how the skill is written is part of that change.

## Commands

### Run Tests

Runs the skill's script tests.

**Inputs:** Workspace checkout containing the installed skill and its tests.

```bash
cd "<workspace>/skills/work-planner" && "<workspace>/scripts/sbx" python3 -m unittest discover -s test
```

### Check Skill Files

Checks the affected skill's Markdown structure and links.

**Inputs:** Workspace checkout and affected skill directory; repeat the skill argument for additional affected skills.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py "<skill-directory>"
```

**Example:** Work Planner in the selected checkout.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py skills/work-planner
```

# Rules

- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Bootstrap.**
  A link whose text opens with a symbol is compiled and used as the [bootstrap](#bootstrap) states.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing. Calls run in order unless a step links a [run-set](#symbols), whose items never write to the same object; that step continues when every item has returned, with every failure returned together as blockers.

# Conventions

- **Session.**
  Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.
- **Repository.**
  `gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.
- **Bodies.**
  - Bodies and long comments always go through a file (`-F body=@file`), never inline, which avoids quoting.
  - **Example.**  workflow-server's dynamic-shell restrictions deny a body inlined in the command.
  - Keep these files in a working directory outside the repository.
- **Scripts.**
  Scripts run under `sbx`, invoked by its absolute path from `<workspace>`, the checkout holding this skill.
- **Boards.**
  A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.
- **Example values.**  Substitute the real ones:
  - `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
  - `950` a pull request, `I07` and `I08` initiative numbers;
  - board `9`, workflow-server's Canon theme, and `419167630` its Status field id;
  - `1` the Initiative Template board, `13` a board copied from it;
  - `14` the Proposals Template, `15` the Proposals board;
  - `m2ux` the user.
  - `<checkout>` any checkout of the project, a linked worktree included.

# Artifacts

## Plan Change

### Fields

#### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.

# Bootstrap

A link whose text opens with a matching [symbol](#symbols) follows the usage instructions and is *not* read as a file.

## Compile

Compile a target file. Run from the skill's directory, which holds `SKILL.md`.

```bash
pf -o <scratch>/<name>.bundle.md <destination>
```

- `<destination>`  The link's destination as written.
- `<name>`  The destination's file name without its suffix.
- `<scratch>`  An existing working directory outside the repository.

> A non-zero exit stops the run and reports `pf`'s diagnostics.

## Symbols

| Symbol | Description | Usage |
| --- | --- | --- |
| `↳` | An inline target | [Compile](#compile) it, read the whole bundle and follow the instructions in its preamble. |
| `⇉` | A dispatched target | [Compile](#compile) it, hand the bundle to one sub-agent, with the inputs the request names, to follow the instructions in its preamble, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered to the session that dispatched it. That session puts each returned question to the user, or returns it in turn when it was itself dispatched, then dispatches again with the answers. A [run-set](#symbols) hands each dispatched item to a sub-agent of its own at once. |
| `⫽` | A run-set | Run the calls the linked section lists concurrently in this session, as parallel tool calls: top-level items together, a nested item once its parent alone has returned, an item that says "for each" once per item, together. Continue when every item, nested, per-item and dispatched, has returned. A failed item cancels nothing: the others finish, then the run-set returns every failure together as blockers. Questions dispatched items return are put to the user together once every item has returned, and only the items that asked are dispatched again, with their answers. |
