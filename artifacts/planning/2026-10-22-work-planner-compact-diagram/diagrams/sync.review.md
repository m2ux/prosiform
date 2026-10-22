# sync-mode.md

Compiler: main 800081b75ad8eb1b6ecbbfb59ac382592f496853

Source files opened by the compiler appear beside the bundle body. The opening compiler paragraph appears under Entry Points, with links into the exact stdout file. Opened files can include deferred targets; their presence does not imply their content is bundled. Images simplify Markdown presentation; the stdout file preserves exact content and link destinations. Compact view replaces body content with … while retaining headings and links. Input content is shown through H2; H3 sections show titles only.

![Source documents and compiled bundle](sync.svg)

### Command

```bash
prosiform --root /tmp/prosiform-diagram-engineering/artifacts/planning/2026-10-22-work-planner-compact-diagram/work-planner --max-output-bytes 1048576 --group artifacts:2 --group protocols:2 modes/sync-mode.md
```

### Entry Points

This bundle was built for [Modes/Sync-Mode](sync.stdout.md#modessync-mode); everything else is material it references.

### Diagnostics

Exit status: 0

```text
W_ENTRY_DESTINATION: the entry reference 'Modes/Sync-Mode' resolves to the destination 'modessync-mode', which the bundle's entry line links it to
  reference: Modes/Sync-Mode
  resolved: modessync-mode
```
