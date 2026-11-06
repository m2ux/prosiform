# Main-target integration validation

E07 merges the completed E04 main at `d8265c82e797355a55cf7ec7d921949b4d7eb6c0`. The reviewed integration is `e7e4af6268fc0cdf843f7c0e8257c6171cd6df8f`; its worktree is clean. All required targets pass across two runs, with an explicit fixture-only revision attestation.

## Compiler and callers

The evaluation expected-run model describes one optional entry and requested presets. Its real compiler subprocess, source and generated-line readers, shell serialization, scorer and deterministic manifests agree with `--entry` and `--presets`. Effective selection comparison preserves equivalent requests. Informational invocations satisfy no guide or compile expectation. E04's nested command capability stays independent of nested starts.

Generated deferred activation lines preserve their parsed source title, including absent and empty values, entities, quotes, backslashes and whitespace. The composition reference carries the title's requested tags. Candidate validation checks the generated line's target and requested selection. Immediate source regressions pass 169 tests; the full gate includes them.

## Observations

All required gates pass: 1,825 source tests, 1,627 deterministic harness tests and 530 corpus fixtures, plus lint, format, strict types (90 files), locked dependencies, installed-wheel smoke, layout, command tables, online links, vocabulary, invocation, conformance and independence. The initial [make-check.log](make-check.log) passes source/harness gates and identifies two corpus expected files omitting the title. The correction changes those two expected lines alone; all runtime, check and test bytes equal the tested merge `e1a0ac023`. The [final-check.log](final-check.log) replays the entire corpus and every target after it at the final head. [integration.json](integration.json) records the exact revision and two-file diff. This is complete target coverage, not a claim that the initial full command passed.

Root reviewed every evaluation caller change against the merged E04 interfaces, the source publication/provenance/candidate changes and their actual passing and failing paths. No instrument is weakened, waived or deferred. No new package or paid run is involved. This integration debt is folded into E07; W08 retains dedicated deferred publication/parity corpus acceptance and W09 retains dedicated tagged workflow/variant acceptance. Coverage, dependencies and lane remain as planned.
