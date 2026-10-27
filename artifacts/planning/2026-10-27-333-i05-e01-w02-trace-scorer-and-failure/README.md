# I05:E01:W02 Trace Scorer and Failure Classes — October 2026

> Task delivery · Created 2026-10-27

## Executive Summary

This record holds the delivery of I05:E01 W02: the deterministic scorer that reads one finished agent workspace against its scenario, passes a run that walked the expected path with every action done, and classifies a failing run by how it went wrong.

It reads the corpus W01 delivered through `workflow.py`; W03's runner calls it on every session, and W04's report aggregates its verdicts.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W02 work item](w02.md) | The scorer, its failure classes and verdict schema |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prior row | [W01 record](../2026-10-27-333-i05-e01-w01-workflow-corpus-in-three/README.md) |
