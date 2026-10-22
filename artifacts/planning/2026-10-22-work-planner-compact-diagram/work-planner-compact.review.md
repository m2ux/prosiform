# SKILL.md

Compiler: main 560926e9c1817d601ec23efe6294bfdb45d9068a

Source files opened by the compiler appear beside the bundle body. The opening compiler paragraph appears under Entry Points, with links into the exact stdout file. Opened files can include deferred targets; their presence does not imply their content is bundled. Images simplify Markdown presentation; the stdout file preserves exact content and link destinations. Compact view replaces body content with … while retaining headings and links.

![Source documents and compiled bundle](work-planner-compact.svg)

### Command

```bash
prosiform --root /tmp/prosiform-diagram-engineering/artifacts/planning/2026-10-22-work-planner-compact-diagram/work-planner --max-output-bytes 1048576 SKILL.md
```

### Entry Points

This bundle was built for [SKILL](work-planner-compact.stdout.md#skill); everything else is material it references.

### Diagnostics

Exit status: 0

```text
W_ENTRY_DESTINATION: the entry reference 'SKILL' resolves to the destination 'skill', which the bundle's entry line links it to
  reference: SKILL
  resolved: skill
```
