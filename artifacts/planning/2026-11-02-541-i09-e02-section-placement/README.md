# I09:E02 Section Placement Integration — November 2026

> change-overview · Created 2026-11-02

## Executive Summary

This record explains the integration pull request that carries I09:E02 Section Placement into `main`: a file's `group` pair places its own sections in the result its parent merges, composition runs from the leaves up, and a merged group nests in the division of the document that placed it.

Its overview gives a reviewer new to the codebase the structure, flows and reading order of the integration diff, measured over the repository graph at the reviewed head.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Architecture Overview](architecture-overview.md) | The integration change's structure, its flows, and the order to read the diff |

## Links

| Resource | Link |
| --- | --- |
| Pull request | [m2ux/prosiform#541](https://github.com/m2ux/prosiform/pull/541) |
