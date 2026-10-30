# Bootstrap Baseline At 93fe6b3

The three independent link invocations ran against source commit `93fe6b354a85e244f64e33af700a55aab4f26044`, using that checkout's editable installation. All three returned exit status 2 and `E_INVALID_USAGE`: this compiler requires `-r`. No resulting bundles were produced. The failures establish the missing invocation behavior; they do not validate grouping or per-file roots.

## Artifacts

| Artifact | What it contains |
| --- | --- |
| [Compiler identity](compiler.json) | Executable path and observed version response |
| [Generated workspace](test_three_skill_links_are_independent_real_compilations/workspace/) | The directly read skill, its three linked targets, transitive sources and decoys |
| [Source skill](test_three_skill_links_are_independent_real_compilations/workspace/skills/pf-bootstrap-specimen/SKILL.md) | The specimen entry point, excluded from compiler inputs |
| [Assemble run](test_three_skill_links_are_independent_real_compilations/runs/01/) | Command, captured source tree, empty stdout and failure diagnostics; no bundle produced |
| [Review run](test_three_skill_links_are_independent_real_compilations/runs/02/) | Command, captured source tree, empty stdout and failure diagnostics; no bundle produced |
| [Defaults run](test_three_skill_links_are_independent_real_compilations/runs/03/) | Command, captured source tree, empty stdout and failure diagnostics; no bundle produced |

The test prototype remains available alongside these artifacts. A passing implementation run must publish its own named directory with the resulting bundles for inspection and later reuse as reference examples.
