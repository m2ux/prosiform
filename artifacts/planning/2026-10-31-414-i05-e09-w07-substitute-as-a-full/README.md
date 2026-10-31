# I05:E09 W07 Substitute as a Full Source — October 2026

> Task delivery · Created 2026-10-31

## Executive Summary

The substitute as a source in its own right. Its title, its group and group-depth, its own root and its own links are the ones the run uses, so a substitute declaring a group contributes to that merged group beneath a member heading naming its own path, and one declaring a root bounds its own outgoing links — a link above it stays the citation its author wrote and is never opened.

Two corpus fixtures carry the criteria. `a-substitute-declaring-a-group-joins-it` merges three members beneath one `Rules` heading with the substitute among them, where the same tree without `-m` gives `rules.md` its own file group. `a-substitute-root-bounds-its-own-links` compiles a detail beside the substitute and emits a link above its root as authored, where removing that root compiles the same link. Each fixture is therefore a statement about the substitution rather than about its tree, and each counterfactual is recorded here and in the pull request body because a manifest declares one invocation.

AC20 is the parent-segment capability the AC11 fixture already shows, so this row states it against that fixture and adds a unit case rather than a third fixture. Nine cases in `src/tests/test_mock.py` hold what a corpus manifest cannot: the substitute's own membership, a depth conflict naming its declaration, its metadata failure on its own location and chain, one capture contributing one membership across two routes, and a substitute above the working directory reading its own group and root.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W07 work item](w07.md) | The substitute's own settings and root, its two fixtures and its cases |
| [Validation](validation.md) | The checks T1–T9 at the revisions they ran, with their observations |
| [Change list](change-list.md) | Every plan change this session applied, and every one it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E09 Mock Substitution](https://github.com/m2ux/prosiform/issues/414) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Mock Substitution design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-mock-substitution) |
| Predecessor | [W01 Mapping, option and identity](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-30-414-i05-e09-w01-mapping-option-and-identity) |
| Pull request | [#439 Substitute as a Full Source](https://github.com/m2ux/prosiform/pull/439) |
| Base | `i05/e09/main`, merged at `52ebf130` |
