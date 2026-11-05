# Deferred external example

## Confirmed source set

On 2026-11-05 the user states: "i will deploy an example skill in a different repo: prosiform-skills. this is deferred for now but will exist soon".

I01's exposure set contains the example skill planned for `prosiform-skills` and the real workspace skills. Deployment is user-owned and deferred. The repository owner, source revision, entry paths and invocation are recorded when available; no invented source link or entry stands for them. The freeze remains conditional on recorded bundling of both parts.

## Delivery evidence

The delivered declaration at `origin/i01/e00/main:ledger/exposure.toml` names ten commands under the removed `example/work-planner` tree. `checks/ledger.py` validates those paths against the local example directory, and `ledger/README.md` describes that local source. This delivery does not establish a declaration for the forthcoming external skill.

I01 AC7 states the confirmed source set and remains unticked. E00 AC6 states the corresponding declaration and is unticked because the external entries and their validation remain pending. W01 retains its historical PR link; the missing declaration is a further-work finding, not a claim that its original delivery included the external skill. E13's exposure gate remains open, and its criteria require no change.

## Pending follow-up

A declaration follow-up needs the deployed example's identity and invocation, the exposure schema and check to read that external source, and an observing test. Its component paths are `main:ledger/exposure.toml`, `main:ledger/exposure.schema.json`, `main:ledger/README.md`, `main:checks/ledger.py` and `main:checks/tests/test_ledger.py`. The run-record work must use the same source identity.

Task placement is pending the gap-task decision; no new tracker task, repository, deployment, source revision or paid run is created by this record.
