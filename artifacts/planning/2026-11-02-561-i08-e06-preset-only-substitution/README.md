# I08:E06 Preset-Only Substitution Integration — November 2026

> change-overview · Created 2026-11-02

## Executive Summary

This record explains the integration pull request that carries I08:E06 Preset-Only Substitution into `main`: a preset's `subst` entry is the only substitution channel, a pair resolves from its declaring file and reaches only the links that file writes, and `-m`, its folder form and the example mock scenarios are removed.

Its overview gives a reviewer new to the codebase the structure, flows and reading order of the integration diff, measured over the repository graph at the reviewed head.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Architecture Overview](architecture-overview.md) | The integration change's structure, its flows, and the order to read the diff |

## Links

| Resource | Link |
| --- | --- |
| Pull request | [m2ux/prosiform#561](https://github.com/m2ux/prosiform/pull/561) |
