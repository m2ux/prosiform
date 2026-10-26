---
prosiform:
  root: "."
---
# Bootstrap

A link whose text opens with a symbol below is loaded through `pf`, not read as a file. Run `pf` from this file's directory, on the link's destination as written, with `<scratch>` an existing working directory outside the repository and `<name>` the destination's file name without its suffix.

| Symbol | Names | Run | Use of the bundle |
| --- | --- | --- | --- |
| `↳` | A mode | `pf -o <scratch>/<name>.bundle.md <destination>` | Read the whole bundle and follow it as the mode's procedure. |
| `»` | Dispatched work | `pf -o <scratch>/<name>.bundle.md <destination>` | Hand the bundle to one sub-agent as its instructions, with the inputs the request names, and continue with the result it returns. |

A bundle carries every protocol, artifact and reference its entry reaches. A sub-agent following a dispatched bundle dispatches nothing further. A non-zero exit stops the run and reports `pf`'s diagnostics.
