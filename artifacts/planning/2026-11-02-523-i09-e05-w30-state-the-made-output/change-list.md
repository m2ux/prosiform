# Change List

The plan changes the I09:E05 W30–W32 delivery session applied and held.

## Applied

- **None.** The session changed no row, criterion or epic beyond recording its own delivery.

## Held

- **Disposition of #588** (Check Mode: Make No Output Folder). The design at ea76fd37 states the build as it is: a check run makes an absent output folder, as a publishing run does, and `publication/a-check-run-into-a-folder-that-does-not-exist-makes-it` holds it. Recommended: close #588 as settled by the design following the build, the issue's own cheaper option; the alternative is a new #523 row making `-c` make nothing, which amends the design clause W30 wrote.
