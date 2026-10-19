# I00:E01:W01 Fixture Layout and Manifest Schema - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the first task of [I00:E01] Corpus Harness. The task settles how a fixture is laid out on disk and defines the manifest schema that declares one: its source tree, its invocation, its expected standard output, its expected exit status and its expected diagnostics, in one place. It carries the schema validation that rejects a manifest which is incomplete or which names an error code outside the declared catalogue.

It matters because the corpus is the contract. A fixture that declares everything a decision needs binds any implementation of prosiform, in any language; one that leaves part of its expectation implicit binds only the implementation that happens to satisfy it. This task fixes the shape every later fixture is written in, so it is the one place where getting the declaration wrong is cheap to correct. The task covers AC1 and AC5 of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Preceding epic | [#26 \[I00:E00\] Project Foundation](https://github.com/m2ux/prosiform/issues/26), closed |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
