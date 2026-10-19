# I00:E02:W07 An Error Code for Every Failing Outcome the Contract Names - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for a task raised during the delivery of [I00:E02] Walking Skeleton rather than planned with it. The contract declares twelve error codes, every one naming a defect in a source document or in the closure drawn from it. It names none for a fault in the command line other than a grouping rule, and none for an unexpected internal error, although it declares an exit status for both. A diagnostic reporting one of those outcomes therefore carries a severity and a message and no code, because a code is the name of a defect the contract declares and inventing one puts a name in the tool the contract does not carry. The task declares the missing codes in the design and carries them into the manifest schema's catalogue, as one piece of work.

It matters because a fixture's manifest requires a catalogued code for every diagnostic it declares, so an outcome with no code is an outcome the corpus cannot state. Eight are known: five from the command interface, and three refusals the profile makes — raw HTML, a recognized unsupported construct, and an entry reference whose suffix lies outside the profile. The last three are the refusing direction of two epic criteria, so those criteria are verified by the corpus in one direction and by unit tests in the other, which binds that direction to one implementation and defeats what the corpus is for. The two documents change together because the catalogue test holds them in exact agreement across branches. The task covers AC12.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w07.md](w07.md) | The task's plan: the failing outcomes the contract names no code for, the codes and the clause each is declared under, and the order the design and the schema change in |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Command interface, streams and exit statuses](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w01-command-interface-streams-and) |
| W02 record | [Profile configuration and source parsing](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w02-profile-configuration-and-source) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
