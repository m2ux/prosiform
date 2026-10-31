# I05:E09 W06 Section Keys and No Chaining — October 2026

> Task delivery · Created 2026-10-31

## Executive Summary

What a section key means, and where the mapping stops. A key carrying a fragment names one section, so the reference it serves compiles the substitute's section while every other reference to that document compiles the document as it ships. A key naming the whole document and a key naming one of its sections serve their references in one run, the narrower taking the section it names. A mapping is one hop: a substitute whose own path is another key is read from disk, and the key naming it is reported unused.

W01 landed the exact-then-bare lookup and owns AC14's mechanism, so this row writes no second lookup. What it adds is the observation: three corpus fixtures, each rendered from a run against the pinned build before its expected bundle was written, and five unit cases that state the section's precedence, the substitute's own section, and the end-to-end pair.

This record holds the delivery: the work item, the validation evidence for every check the work item names, and the plan changes the session applied and held.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W06 work item](w06.md) | What a section key redirects, why the mapping stops after one hop, and the three fixtures |
| [Validation](validation.md) | The checks T1–T9 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
| Predecessor | [W04 Substitution warnings and check mode](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w04-substitution-warnings-and-check) |
| Pull request | [#437 Section Keys and the End of Chaining](https://github.com/m2ux/prosiform/pull/437) |
