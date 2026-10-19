# I00:E01:W05 Warning Diagnostics, and Every Document the Link Check Reads - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the last task of [I00:E01] Corpus Harness. The task opens the manifest schema to the warnings a run emits alongside success: a warning diagnostic sits beside an error one, its code drawn from a catalogue of the warning codes the design declares, and a manifest naming a code outside that catalogue fails validation. The catalogue test reads both prefixes, so a code the design names and the schema omits fails the check whichever kind it is. The task also widens the link check from the READMEs to every Markdown document the repository tracks, the fixture corpus excepted.

It matters because a diagnostic carries a stable code and the corpus currently states nothing about a successful run's output on stderr, so two of the design's clauses have no fixture that could express them. It matters for the documents because `docs/glossary.md` ships inside the installed build and the tool's diagnostics draw their vocabulary from it, and nothing resolves the references it carries. The task covers AC7 and AC8, the last two criteria of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w05.md](w05.md) | The task's plan: how a severity pairs a diagnostic with its catalogue, how the catalogue test derives both prefixes from the design, and how the link check separates a document from a fixture's source |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Fixture layout and manifest schema](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-3-i00-e01-w01-fixture-layout-and-manifest) |
| W04 record | [Documentation held to the project](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-3-i00-e01-w04-documentation-held-to-the) |
| Epic review | [#41](https://github.com/m2ux/prosiform/pull/41) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
