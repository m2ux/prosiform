# I10:E02 Session Isolation Integration — November 2026

> change-overview · Created 2026-11-03

## Executive Summary

This record explains the integration pull request that carries I10:E02 Session Isolation into `main`: the eval preflight reading every settings scope a session will see before the run starts one, refusing a project-scope settings file that declares a hook and recording the host's managed settings hook in the run record.

Its overview gives a reviewer new to the codebase the structure, flows and reading order of the integration diff, measured over the repository graph at the reviewed head.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Architecture Overview](architecture-overview.md) | The integration change's structure, its flows, and the order to read the diff |

## Links

| Resource | Link |
| --- | --- |
| Pull request | [m2ux/prosiform#600](https://github.com/m2ux/prosiform/pull/600) |
