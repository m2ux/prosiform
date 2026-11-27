# W00 Review

## Validation

| Check | Result |
| --- | --- |
| Each field and exclusion in the ledger specimen README's "Each Feature And Its Field" and "What The Ledger Leaves Out" | Stated in the contract's Build ledger clauses and in [ledger-contract.md](../2026-11-26-prosiform-preset-architecture/ledger-contract.md) |
| Each property of `ledger.schema.json` | Listed in the coverage's "Each Schema Field" with the build that writes it |
| Each specimen ledger against the schema, Draft 2020-12 | `fixed.ledger.yaml` and the run's `ledger.yaml` validate |
| Each `sha256` against the file it names | All source and bundle hashes match; the fixed control's equal `specimens/baseline.json` |
| The run's digest | `sha256sum -c ledger.yaml.sha256` passes |
| The two builds rerun under pf 0.36.0 | Bundle hashes reproduce byte for byte; the files opened match each `use` |
| List order in all five specimen ledgers | Each list stands in the order the contract's Order clause gives |
| The matrix against `specimen-matrix.md`'s Ledger line | Every case names a fixture W02 or W04 declares, or the test module carrying it |
| Diagnostic codes | No code is added; the verification codes are stated by E01:W04 |

## Cross-Family Review

Codex, architecture mode, read-only, over the three declared files and the ledger specimen set.

| Finding | Severity | Disposition |
| --- | --- | --- |
| F1. The contract's automatic output names append `--p-` and a digest, where pf 0.36.0 writes `-alpha+small` | High | Held as an arising issue: the divergence predates the ledger and sits in Automatic output names, outside this unit's clauses |
| F2. The source order rule does not reproduce the run specimen's order | High | Fixed: sources follow placement order across the run, alternatives' sources in bundle order, which reproduces all five specimen ledgers |
| F3. A path holding `#` is ambiguous beside a fragment | Medium | Fixed: reference fields percent-encode `%` and `#` in the path, read back by the reference grammar; a test case is added to the matrix |
| F4. The determinism test changed hashed inputs | Medium | Fixed: the test reruns one tree and feeds the projection reordered records |
| F5. No case fails a ledger or digest write after the bundles are staged | Medium | Fixed: the publication test module carries that case |
| F6. Check mode promised empty output after a failed standard-output write | Medium | Fixed: a failed write is a publication failure |
| F7. Substitution rows could tie | Medium | Fixed: ties break by preset declaration order, then substitute path order |
| F8. A picking deferral's `published` title and an absent alternative were misstated | Low | Fixed in the clause and the coverage table |
