# I05:E03:W02 All-or-Nothing Publication — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E03 W02: a run that publishes several bundles validates every one before it writes any, writes each atomically, and on any failure writes none. A `-c` run validates the whole set and writes nothing, and files in the output folder the run does not produce are left as they are.

Every later row of the epic publishes a set of bundles from one run: one for the entry and one per dispatched target. A caller then reads either the whole set a run produced or the set that was there before it, never a mixture.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E03 Dispatch Bundles](https://github.com/m2ux/prosiform/issues/351) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Dispatch Bundles planning record](../2026-10-28-351-i05-e03-dispatch-bundles/README.md) |
| Prior task | [W01 Output Folder and Joined Derived Names](../2026-10-28-351-i05-e03-w01-output-folder-and-joined/README.md) |
