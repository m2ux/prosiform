# Native Codex Adapter

The user selects native Codex, `gpt-6.1-sol` with `medium` reasoning, for the W04 shakedown on 2026-11-04. The adapter is folded into W04; the two delivery lanes and the following default-model row retain their scope.

## Native Transport

- A standard-library bridge drives the installed `codex app-server` over JSON lines on standard input and output. The existing runner still owns each session's workspace, subprocess group, timeout and records.
- Initialize the connection, create an ephemeral thread with the exact model and no provider fallback, then start its turn with the shared eval instruction and explicit reasoning effort.
- Record native notifications and responses. `rawResponseItem/completed` retains tool call ids and arguments; `rawResponse/completed` separates model responses. A parallel start shares that real response boundary, never a guessed time window.
- `collabAgentToolCall` supplies prompt, sender/receiver thread ids, operation and agent states. `spawnAgent`, `sendInput` and `followupTask` create starts; returned reports come from `agentsStates.message`, read by the guide's `Question:` marker.
- Subscribe newly spawned child threads through native `thread/resume` so their dispatches, completed reports and usage are observable. Missing native evidence is a harness defect, not an inferred success.

## Isolation and Material

- Use an eval-owned `CODEX_HOME` with authentication from the existing account, without caller configuration, rules, instructions, memory or installed skills. No credential bytes enter logs or commits.
- Use the workspace-write sandbox with the single prepared workspace as its root; disable external capabilities and validate the native `instructionSources` readback.
- Every form receives the chosen build as `pf` on its path, with no workspace copy. Codex's bootstrap material lives under its native `.agents/skills` root.
- Native shell confinement must be proven by its configuration or tool boundary. Workspace-write alone states a filesystem boundary, not a pf-only command rule. The adapter's implementation records the supported boundary precisely.

## Usage and Completion

- Use the latest cumulative `totalTokens` for each observed thread, counted once per thread; cached input and reasoning output are already included. Native raw completion usage and ids support response grouping and usage verification.
- Codex supplies no dollar amount. `cost_usd` is absent, and the runbook holds the run to its token budget alone.
- Refusals, failed turns, requested approvals and incomplete protocol evidence remain explicit errors. The runner's stop rules and triage still govern the shakedown.

## Verification

- Native-shape transcript tests cover exact prompt targets, real response boundaries, child reports, answered questions, nested starts, commands, cumulative usage and missing telemetry.
- A stub app-server exercises initialization, isolated thread/turn requests, child subscriptions, model matching, refusals and shutdown without a model call.
- The full 76-cell shakedown on the selected model proves the real CLI behavior. Every failure receives `miss`, `defect` or `unclear`; a defect or unclear result stops delivery before caps are derived.

## Sources

- [Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode) documents the exec JSON stream and usage fields.
- [App-server](https://learn.chatgpt.com/docs/app-server) documents initialization and thread/turn lifecycle.
- The installed CLI's generated TypeScript protocol at version `0.165.0` supplies `ThreadStartParams`, `ThreadStartResponse`, raw response notifications, `ThreadItem.collabAgentToolCall` and per-thread usage fields.
