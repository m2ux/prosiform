# Protection Evidence

Repository ruleset 25628172, `default branch`, active since 2026-10-22 and last updated 2026-10-24, governs `main`, `engineering` and `workspace`.

| Branch | Pull request | Approvals | Force-push | Deletion | Creation and update | Bypass |
| --- | --- | --- | --- | --- | --- | --- |
| `main` | Required | 1 | Refused | Refused | Restricted | Admin role, always |
| `engineering` | Required | 1 | Refused | Refused | Restricted | Admin role, always |
| `workspace` | Required | 1 | Refused | Refused | Restricted | Admin role, always |

- **AC1 holds.** `main` requires a pull request before merge and refuses a force-push and a deletion ([rules-main.json](rules-main.json)).
- **AC3 holds.** `engineering` and `workspace` refuse a force-push and a deletion ([rules-engineering.json](rules-engineering.json), [rules-workspace.json](rules-workspace.json)), and the Admin role's bypass carries a direct push: planning records `40e7e3a2` through `2f57239e` were pushed straight to `engineering` on 2026-10-26 under the ruleset.
- **Epic bases and task branches are outside the ruleset.** `i01/e12/main` and `i01/e12/engineering` were created under it on 2026-10-26.

The ruleset is stricter than a guard on `engineering` and `workspace` alone: a writer without the bypass needs a pull request there too. That is the configuration kept; the Admin bypass is what the direct-push flows rely on.

The full ruleset is [ruleset.json](ruleset.json).
