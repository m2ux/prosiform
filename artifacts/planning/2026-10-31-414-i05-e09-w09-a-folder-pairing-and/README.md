# I05:E09 W09 A Folder Pairing and Its Precedence — October 2026

> Task delivery · Created 2026-10-31

## Executive Summary

A mapping side ending in a separator makes its entry a folder pairing, so a folder of stand-ins costs one entry rather than one per file. The key folder matches every reference under it, the substitute folder takes the same remainder, the reference keeps its section it named, and exact keys answer before folder keys — with the longer of two matching folders winning.

The work is a grammar change to `-m` as much as a resolution change: `closure.normalized` drops an empty path segment, so the trailing separator that states the folder must be read before normalisation or it is gone before anything can interpret it. Both sides must agree on the separator, and a folder side is exempt from the Markdown-suffix refusal W10 added, because a folder legitimately names no document.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Plan | [Declared Inclusion, Target Presets and Exclusion](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-31-i05-inclusion-profiles-and-folders) — where the folder pairing was designed |
