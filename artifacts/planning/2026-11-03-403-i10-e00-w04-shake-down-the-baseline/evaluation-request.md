# Baseline Shakedown Execution

## Reviewable Scope

- Delivery: I10:E00 W04, the existing reserved branch `i10/e00/w04-shake-down-the-baseline`; the #650 implementation and full local checks are committed and pushed at `f9d69cbb`.
- Destination: OpenAI through the installed native Codex app-server, harness `codex`, eval model `gpt-6.1-sol`, reasoning `medium`, using the user's existing Codex account.
- Material: the prepared diagram-following workflow documents and bundles, each scenario's input files and answers, and the eval instructions the runner gives its isolated sessions. The runner prepares these from `evals/diagram-following/workflows/` and its instruction files; the shakedown does not submit the whole repository.
- Subsequent messages: tool results containing the guide, compilation output and session files, and sub-agent prompts and reports. The adapter isolates caller configuration and checks the native instruction-source readback. Committed managed metadata holds count and fingerprint only. GitHub currently reports the source repository public.
- Matrix: 76 cells, one repetition each. Results stay under the task checkout's `evals/diagram-following/results/baseline-shakedown`; workspaces stay under `/home/mike1/projects/eval/prosiform/workspaces/baseline-shakedown`.
- Limits: each session has the recorded 1,130,000-token cap; the run has an 85,880,000-token budget. Codex reports no dollars, so the runbook's token-only rule applies; no price is inferred. Earlier Claude attempts spent USD 0.677 of their USD 5 aggregate allowance, and no further Claude session starts.
- Purpose: verify the real CLI behavior after #632, #637 and #650, triage every failure, and derive the baseline session, token and cost caps from the completed shakedown.

## Command

From the task checkout, with its build on the path:

```bash
UV_CACHE_DIR=/tmp/i10-w04-uv-cache make eval-diagrams HARNESS=codex ARGS='--models gpt-6.1-sol --reasoning-effort medium --repetitions 1 --session-budget-tokens 1130000 --budget-tokens 85880000 --run-id baseline-shakedown'
```

## Approval State

Automatic approval review rejected the earlier Claude monitor launch before any paid session started. The user responded on 2026-11-04 with “use the codex eval harness instead”, then explicitly selected `gpt-6.1-sol` with `medium` reasoning. The prepared eval payload to native Codex/OpenAI is authorized; no separate Anthropic approval remains pending and no Anthropic run proceeds. The adapter's local verification precedes this Codex run.
