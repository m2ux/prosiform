# § Instructions

Run `pf`, then follow the guidance it prints. Follow [Guide](#guide) next.

# Guide

```mermaid
flowchart LR
  G["⇉ Gather"] --> D["⇉ Decide"] --> P["⇉ Plain"]
  click G "stages_gather.bundle.md"
  %% G on haiku
  click D "stages_decide--p-3bcbdbfeabe6.bundle.md" "deep"
  %% D on opus
  click P "stages_plain.bundle.md"
```

- Nested:

  ```mermaid
  flowchart LR
    X["⇉ Gather"]
    click X "stages_gather.bundle.md"
    %% X on haiku
  ```
