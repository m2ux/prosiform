# standup-mode.md

Compiler: main 00fd19df3660304cc5bdc979eb635032b905c4aa

Source files opened by the compiler appear beside the bundle body. The opening compiler paragraph appears under Entry Points, with links into the exact stdout file. Opened files can include deferred targets; their presence does not imply their content is bundled. Images simplify Markdown presentation; the stdout file preserves exact content and link destinations. Compact view replaces body content with … while retaining headings and links. Content is shown through H2; H3 sections show titles only.

![Source documents and compiled bundle](standup.svg)

### Command

```bash
prosiform --root /tmp/prosiform-diagram-engineering/artifacts/planning/2026-10-22-work-planner-compact-diagram/work-planner --max-output-bytes 1048576 --group artifacts:2 --group protocols:2 modes/standup-mode.md
```

### Entry Points

This bundle was built for [Modes/Standup-Mode](standup.stdout.md#modesstandup-mode); everything else is material it references.

### Diagnostics

Exit status: 0

```text
W_ENTRY_DESTINATION: the entry reference 'Modes/Standup-Mode' resolves to the destination 'modesstandup-mode', which the bundle's entry line links it to
  reference: Modes/Standup-Mode
  resolved: modesstandup-mode
```
