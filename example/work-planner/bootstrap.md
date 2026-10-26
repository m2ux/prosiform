---
prosiform:
  root: "."
---
# Bootstrap

Run `pf` from this file's directory, on a link's destination as written. A link opening with `↳` names a mode: on selecting it, run `pf -o <scratch>/<mode>.bundle.md <destination>`, with `<scratch>` a working directory outside the repository, then read the whole bundle and follow it as that mode's procedure. The bundle carries every protocol, artifact and reference the mode reaches. A non-zero exit stops the run and reports `pf`'s diagnostics.
