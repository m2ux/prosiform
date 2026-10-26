# Delivery Branch Evidence

Each push ran against `origin` on 2026-10-26 with ruleset 25628172 active on `main`, `engineering` and `workspace`.

| Branch | Kind | Created from | Created | Deleted |
| --- | --- | --- | --- | --- |
| `i01/e12/main` | Epic base | `origin/main` | Yes | Yes |
| `i01/e12/engineering` | Epic base | `origin/engineering` | Yes | Yes |
| `i01/e10/w02-delivery-branches` | Task branch | `origin/main` at `6554db86` | Yes | Yes |

- **AC2 holds.** Creating and deleting an epic base and a task branch succeeds under the settings; `git ls-remote` shows none of the three on the remote after deletion.
- The epic bases were created for a unit later withdrawn before any work landed, and deleted unused.
