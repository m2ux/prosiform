---
prosiform:
  root: "."
---
# Bootstrap

A link whose text opens with one of the [symbols](#symbols) is loaded through `pf`, *not* read as a file: fill the [load command](#load)'s parameters from that link, run it, then use the bundle as its symbol states.

## Load

Run from this file's directory. A non-zero exit stops the run and reports `pf`'s diagnostics.

```bash
pf -o <scratch>/<name>.bundle.md <destination>
```

- `<destination>`  The link's destination as written.
- `<name>`  The destination's file name without its suffix.
- `<scratch>`  An existing working directory outside the repository.

## Symbols

| Symbol | Names | Use of the bundle |
| --- | --- | --- |
| `↳` | A Prosiform target | [Load](#load) it, then read the whole bundle and follow the instructions in its preamble. |
| `»` | A dispatched target | [Load](#load) it, then hand the bundle to one sub-agent, with the inputs the request names, to follow the instructions in its preamble, and continue with the result it returns. A sub-agent following a dispatched bundle dispatches nothing further. |
