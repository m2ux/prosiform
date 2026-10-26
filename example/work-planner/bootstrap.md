---
prosiform:
  root: "."
---
# Instructions

A link whose text opens with a symbol below is loaded through `pf`, *not* read as a file. Run `pf` from this file's directory.

| Parameter | Value |
| --- | --- |
| `<destination>` | The link's destination as written. |
| `<name>` | The destination's file name without its suffix. |
| `<scratch>` | An existing working directory outside the repository. |

| Symbol | Names | Run | Use of the bundle |
| --- | --- | --- | --- |
| `↳` | A Prosiform target | `pf -o <scratch>/<name>.bundle.md <destination>` | Read the whole bundle and follow the instructions in its preamble. |
| `»` | A dispatched target | `pf -o <scratch>/<name>.bundle.md <destination>` | Hand the bundle to one sub-agent, with the inputs the request names, to follow the instructions in its preamble, and continue with the result it returns. |

A sub-agent following a dispatched bundle dispatches nothing further. A non-zero exit stops the run and reports `pf`'s diagnostics.
