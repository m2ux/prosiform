## Overview

A live session of the diagram-following eval in a form that hands it a bundle set cannot bundle a deferred line its bundle carries. Since #819, a bundle names each deferred line's target from the folder the bundle is in, and the guide tells an agent to run `pf` on the line from there. The eval's runner, instruction and sandbox predate that contract. This hot-fix asks for a live session to be able to follow the guide on a deferred line.

Target: `main`

## Problem

- **The copied bundles name the wrong sources.**
  The runner bundles a form in a temporary folder, then copies the bundle files into the session's workspace beside a copy of the sources. Each deferred line still names its target from the temporary folder, so it points at the repository's own sources by a path that resolves to nothing from the workspace.
- **The instruction and the guide disagree.**
  The bundle-set instruction tells a session to run each `pf` command from its workspace. The guide `pf` prints tells it to run a bundle's link from the folder that bundle is in.
- **The sandbox admits `pf` alone.**
  The harnesses admit commands that begin with `pf`, so a session cannot change to the bundle's folder before running the line.
- **No test caught it.**
  The eval harness bundles each form where its tests can resolve the lines, so it passes while a live workspace fails. A layout built as the runner builds one, from the `deferred-dispatch` workflow, fails the line as written from both the workspace and the bundle's folder with `E_TARGET_NOT_FOUND`.
- **Affected runs.**
  Every live session in the `bundle-set` and `briefed` forms whose path reaches a deferred line, which the deferral, agent-pick, deferred-dispatch and sub-agent scenarios all do.

## Proposal

- **A live session can follow the guide on a deferred line.**
  The session runs `pf` on a deferred line its bundle carries, as the guide states, and bundles the target in its workspace.
- **A test holds the live layout.**
  The eval harness exercises a workspace laid out as the runner lays one out, so the harness fails where a live session would.

## Acceptance Criteria

- [ ] **AC1.** A deferred line in a workspace the runner prepares names a document of that workspace, as a test over `run.py`'s layout shows.
- [ ] **AC2.** A session following the guide runs `pf` on that line within its sandbox and bundles the target, as a stub-agent run of the `deferred-dispatch` scenario shows.
- [ ] **AC3.** The instruction, the guide and the harness permissions agree on where a session runs `pf`, as the eval `README.md` and its tests show.
- [ ] **AC4.** `make eval-harness` and `make check` pass.

## Open Questions

- Where a live session runs `pf` on a deferred line, and how its sandbox admits that run.

## References

- **R1.** [#819](https://github.com/m2ux/prosiform/pull/819) — Publishes deferrals from the folder each bundle is in.
- **R2.** [#852](https://github.com/m2ux/prosiform/issues/852) — The eval-harness failures the same change caused in the tests.
- **R3.** [Invocation](https://github.com/m2ux/prosiform/blob/main/invocation.md) — Run a link in a bundle as written, from the folder that bundle is in.
