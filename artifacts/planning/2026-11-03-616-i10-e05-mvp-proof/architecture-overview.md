# Architecture Overview — MVP Proof

> architecture-overview · [m2ux/prosiform#616](https://github.com/m2ux/prosiform/pull/616) · 2026-11-03

## Summary

The diagram-following eval gains a runbook and triage rubric for every live run, a run record that counts and fingerprints the managed configuration its sessions carried, a report that sums cost and lists each failing session with its disposition, and the committed MVP proof run. The change lands in the eval harness, `evals/diagram-following/`, and leaves the `pf` build and its bundling contract untouched. It lets a live run be repeated to the letter and read without naming any platform's configuration.

## Structure

The runner `run` asks the harness to preflight the eval's settings and then to read the **managed configuration**: a plugin installed at managed scope or enabled by signed remote settings, the environment those settings add, and the hooks its plugins and the host's managed settings file declare. `counted` turns it into counts and a fingerprint, a SHA-256 digest over the sorted identifiers, versions, keys and events. The report reads that record and the triage's `dispositions.json` beside `run.json`.

```mermaid
---
title: Components — MVP Proof
---
flowchart LR
    Caller([eval caller])

    subgraph Runner [Eval runner: run.py]
        RN[run]
        IJ[injected]
    end

    subgraph Harness [Eval harness: harness.py]
        PF[Claude.preflight]
        MG[Claude.managed]
        CT[counted]
        RC[_record]
    end

    subgraph Report [Report: report.py]
        RP[report]
        FL[failing]
        ML[managed_line]
    end

    RJ[(run.json)]
    DJ[(dispositions.json)]

    Caller -->|options, eval root| RN
    RN -->|config, workspaces, form trees| PF
    RN -->|after preflight| MG
    MG -->|plugins, env keys, hook events| CT
    MG -->|read JSON| RC
    RN -->|hooked| IJ
    RN -->|managed counts| RJ
    RP -->|reads| RJ
    FL -->|reads| DJ
    RP -->|failing sessions| FL
    RP -->|managed record| ML

    style PF fill:#c8e6c9,stroke:#2e7d32
    style MG fill:#c8e6c9,stroke:#2e7d32
    style CT fill:#c8e6c9,stroke:#2e7d32
    style FL fill:#c8e6c9,stroke:#2e7d32
    style ML fill:#c8e6c9,stroke:#2e7d32
    style DJ fill:#c8e6c9,stroke:#2e7d32
    style RN fill:#fff9c4,stroke:#f9a825
    style IJ fill:#fff9c4,stroke:#f9a825
    style RP fill:#fff9c4,stroke:#f9a825
    style RJ fill:#fff9c4,stroke:#f9a825
    style RC fill:#f5f5f5,stroke:#9e9e9e
```

### Eval Harness

- **`Claude.preflight`.**
  Admits a plugin installed at managed scope or enabled by remote settings with a signature beside them; refuses one at any other scope, one unsigned remote settings enable, and every settings hook the config directory, a form tree or a workspace ancestor declares.
- **`Claude.managed` and `counted`.**
  Collect the managed plugins with versions, the signed `env` keys and the hook events, then return counts and a fingerprint, null when nothing is managed. Cursor and opencode count nothing.

### Eval Runner

- **`run`.**
  Runs the preflight after the corpus read and session choice, reads the managed record, and writes it to `run.json` under `managed`.
- **`injected`.**
  Takes `hooked`, true when a managed plugin or hook is counted, so a hook response is the managed configuration's and fails no run.

### Report

- **`report` and `failing`.**
  Sum every session's reported cost into `cost_usd` and list each failing session with the disposition `dispositions.json` gives it, refusing an unknown disposition or an entry naming no failing session.
- **`managed_line`.**
  States the counts and fingerprint, or none.

## Behaviour

Two flows change: reading the managed configuration before the first session, and writing the report from a finished run.

### Managed Record

`run` starting a run yields a `managed` record of counts and a fingerprint.

```mermaid
---
title: Sequence — Managed Record
---
sequenceDiagram
    actor Caller
    participant Run as run
    participant Claude as Claude.managed
    participant Rec as _record
    participant Count as counted

    Caller->>Run: options
    Run->>Claude: managed(config)
    Claude->>Rec: installed plugins, remote settings, hooks files
    Rec-->>Claude: JSON records
    Claude->>Count: versions, env keys, hook events
    Count-->>Claude: counts, fingerprint
    Claude-->>Run: managed
    Run-->>Caller: run.json with managed
```

- **Managed hooks.**
  A managed plugin's `hooks/hooks.json` under its install path, and the host's managed settings file, each give the events they declare a hook for.
- **Signed settings.**
  The remote settings' enabled plugins and `env` keys count only with the signature file beside them.

### Report

`main` writing a report yields `report.md` and `report.json` with cost, managed configuration and failing sessions.

```mermaid
---
title: Sequence — Report
---
sequenceDiagram
    actor Caller
    participant Main as main
    participant Rep as report
    participant Fail as failing
    participant Md as markdown

    Caller->>Main: run directory
    Main->>Rep: report(run_directory)
    Rep->>Fail: dispositions.json, records
    Fail-->>Rep: failing sessions
    Rep-->>Main: built report
    Main->>Md: markdown(built)
    Md-->>Main: cost, managed line, Failing Sessions
    Main-->>Caller: report.md, report.json
```

- **Untriaged.**
  A failing session the file does not name reads `untriaged`.

## What Changed

### Eval Harness

- **Managed configuration.**
  A managed plugin starts its sessions and is recorded by count and fingerprint, naming none of it.

### Eval Runner

- **Run record.**
  `run.json` holds `managed` as counts and a fingerprint.

### Report

- **Cost and triage.**
  The report sums cost and lists each failing session with its disposition.

### Runbook and Proof

- **Runbook.**
  `RUNBOOK.md` holds the triage rubric and each live run's arguments, caps and stop rules.
- **Proof record.**
  `mvp-proof.json` and `mvp-proof.md` hold the live proof run, with `baseline.json` unchanged.

## Reading Order

1. **[RUNBOOK.md](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/RUNBOOK.md#triage-rubric)** — the rules every live run and its triage follow.
2. **[harness.py](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/harness.py#L136-L162)** — `counted`, then [`Claude.preflight`](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/harness.py#L253-L331) and [`Claude.managed`](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/harness.py#L333-L374).
3. **[run.py](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/run.py#L722-L765)** — where `run` preflights and records the managed configuration.
4. **[report.py](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/report.py#L199-L275)** — `report`, `place` and `failing`, then [`managed_line`](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/report.py#L362-L371).
5. **[README.md](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/README.md#isolation)** — Isolation and MVP proof as the eval states them.
6. **[mvp-proof.md](https://github.com/m2ux/prosiform/blob/2780aea53c518cfaa4c67155b5fa2079c7d2f8a6/evals/diagram-following/mvp-proof.md)** — the proof run's report.

## Risks and Watch Points

- **Managed hook discovery.**
  `Claude.managed` reads hooks only from a managed plugin's `hooks/hooks.json` under its install path and the host's managed settings file; a hook declared elsewhere is admitted through `hooked` but not counted.
- **Signature by presence.**
  Remote settings count as signed when the signature file exists; its content is not verified.
