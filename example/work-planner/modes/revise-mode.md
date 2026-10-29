---
prosiform:
  root: ".."
---
# Revise Mode

Changes the skill itself: SKILL.md, its modes, artifacts, references and scripts.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Read the Guidelines

Read the [shared skill guidelines](../../guidelines.md) and [¬ skill guidelines](../guidelines.md) whole before the first edit.

### 2. Understand the Request

Interview the user, putting each question as the [Rules](../rules.md) state, until the change and its scope are clear.
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

Read every changed file against the [shared skill guidelines](../../guidelines.md) and [¬ skill guidelines](../guidelines.md), checking:
- The [description](../../guidelines.md#frontmatter), when the skill's reach changed.
- [Layout](../../guidelines.md#layout).
- [Prose](../../guidelines.md#prose), with the skill's own [¬ Prose](../guidelines.md#prose), and [stale claims](../../guidelines.md#changes).
- [Commands](../../guidelines.md#commands).
- [Links](../../guidelines.md#links).
- [Progressive disclosure](../../guidelines.md#progressive-disclosure).
- Fix each departure.

### 6. Run Script Tests

When an executable script, its consumed template or a test changed, run the script tests from the work-planner directory in the supplied workspace checkout. Resolve `<workspace>` to that checkout, as [Helper invocation](../conventions.md#helper-invocation) states. Otherwise continue at [7. Check Skill Files](#7-check-skill-files).

```bash
cd "<workspace>/skills/work-planner" && "<workspace>/scripts/sbx" python3 -m unittest discover -s test
```

### 7. Check Skill Files

If the script tests ran, read their exit code and output before continuing. Correct any failure and repeat [6. Run Script Tests](#6-run-script-tests) until they pass.
- When SKILL.md changes, confirm its frontmatter opens and closes with `---` and holds `name` and `description`.

From the supplied workspace checkout, check every affected skill's Markdown structure and links as [Helper invocation](../conventions.md#helper-invocation) states. Resolve `<skill-directory>` to the affected skill's path relative to that checkout; supply one directory argument per affected skill.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py "<skill-directory>"
```

**Example:** Work Planner in the selected checkout.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/scripts/check_skill_files.py skills/work-planner
```

### 8. Verify Disclosure and Dependencies

Read the skill-file check's exit code and output. Correct any failure and repeat the affected checks from [6. Run Script Tests](#6-run-script-tests) before continuing.
- Apply [disclosure verification](../../guidelines.md#disclosure-verification) with the skill's [¬ representative scenarios](../guidelines.md#progressive-disclosure).
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
