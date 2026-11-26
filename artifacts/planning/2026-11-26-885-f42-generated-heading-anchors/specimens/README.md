# F42 Before and After

The same synthetic source is compiled with the original main build and the fixed build. No paid agent runs are involved.

- Before: 6eb02cb5c44bf8942ad16e5c4e6104438a969438, build metadata 0.35.0
- After: e271c2252afb5ff3f23845dac3860ed0b6832fad, build metadata 0.35.0 plus F42

## Specimens

- [Generated heading first](generated-first/README.md): dispatch destination #investigate; authored destination #investigate-1
- [Authored heading first](authored-first/README.md): authored destination #investigate; dispatch destination #investigate-1

Each pair has byte-identical sources. Before F42, compilation refuses the heading collision and publishes no bundle. With F42, ordinary and Mermaid links retain their separate destinations. The exact diagnostics, compiler source digests, commands, source digests and bundle digests are retained in [the receipts](receipts.json).
