# W09: Release Tags

> Task record. Created 2026-11-26.

## Executive Summary

A repository check fails a commit whose build tag names a version the build does not report, or whose build and contract tags disagree.

The row belongs to the repository checks epic, whose rows state a rule a check makes imprecisely.

## Artifacts

| Artifact | Purpose |
| --- | --- |
| [w09.md](w09.md) | Work item for W09. |
| [test-evidence.md](test-evidence.md) | The check's tests, its run over the `python/v0.35.0` release commit with real and faulty tags, and `make check-all`. |
| [run.py](run.py) | Runs `checks/releases.py` over a named repository. |

## Links

| Resource | URL |
| --- | --- |
| Task issue | https://github.com/m2ux/prosiform/issues/191 |
| Epic I19 E00 | https://github.com/m2ux/prosiform/issues/187 |
