# Linked Skill Bootstrap Examples

These artifacts define the end-to-end task's reference scenarios. The skill entry point is read directly; its three links are separate compiler inputs. The executable prototype builds real Markdown stacks and calls the selected pf executable in subprocesses.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [Bootstrap skill](bootstrap-skill/SKILL.md) | Instructions to compile and read three linked targets independently |
| [Executable prototype](test_linked_stack.py) | Source generation, black-box assertions and durable run capture |
| [Baseline run](runs/baseline-93fe6b3/README.md) | Preserved source trees and observed failures against the current compiler |

## Scenario Matrix

| Entry link | Root and grouping | Linked stack | Observable result |
| --- | --- | --- | --- |
| Assemble | Explicit workspace root; procedures at depth 2 | Alpha rules → nested checks → shared → working-directory leaf → tail | Alpha content only; independent groups; depth-3 checks and pooled depth-2 leaf sections |
| Review | Explicit beta-library root; reviews at depth 3 | Beta rules → shared → working-directory leaf → tail | Beta content only, even though alpha has the same filenames |
| Defaults | Root absent; defaults at depth 2 | Working-directory leaf → tail | Caller-directory content, with source-directory and parent-root decoys excluded |

Further prototype tests change the working directory, select a fragment, compare explicit file output with stdout, introduce conflicting depths within one group and reject invalid depth types/ranges. The delivery task also covers derived output filenames, repeated targets, rewritten destinations and the shared-source case described in its work item.

## Reference Layout

```text
workspace/
  skills/pf-bootstrap-specimen/
    SKILL.md
    modes/{assemble,review,defaults}.md
  libraries/
    alpha/{rules,shared}.md
    alpha/nested/checks.md
    beta/{rules,shared}.md
  run/{leaf,tail}.md
```

Additional same-named decoy files reveal incorrect resolution. Source markers identify provenance in a bundle; they are fixture data, not authoring requirements. Explicit roots are relative to the file declaring them. Absent roots use the invocation working directory for every source. Group declarations belong to individual sources.

## Running The Prototype

From this folder, pass an installed executable and a fresh artifact destination:

```bash
python3 test_linked_stack.py --pf /absolute/path/to/pf --artifacts runs/verified-revision -v
```

Each test retains its generated workspace. Each invocation retains its input snapshot, command, working directory, exit status, stdout and JSON diagnostics. A successful bundle is saved as `bundle.md` alongside that invocation. Existing run directories are refused so an inspection record cannot be overwritten by a rerun.

The delivery record must identify the tested source commit in addition to the executable's version. CI integration and a verified run of every scenario belong to the planned task. The prototype checks deterministic command behavior; it does not establish that an agent followed the skill.

## Visual Inspection

Open a run's source SKILL.md and its three targets, then compare each target's linked source stack with that run's bundle. Check source markers, group headings, pooled sections, preserved fragment selections and absence of decoy or unrelated content. Each per-link result has its own artifact entry. A failed run retains its diagnostics and explicitly records that no bundle was produced.

Only successful runs against the identified implementation become validated output examples. The baseline is a reproducible gap demonstration, not a passing conformance example.
