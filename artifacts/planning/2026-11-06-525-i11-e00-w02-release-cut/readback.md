# Publication and readback

> Recorded 2026-11-06

## Branch

```text
release/v0.17.0 → origin/release/v0.17.0
base: origin/main fb17c2c97524b649dc4b619f1b88cd825a797d85
head: b10437ea7f064715f54e192fad415aba0bdfe692

$ git log --oneline origin/main..HEAD
b10437ea7 Declare Python build version 0.17.0

$ git diff --name-only origin/main..HEAD
src/pyproject.toml
src/uv.lock
```

## Tags

Both are annotated tags naming the version commit.

```text
$ gh api repos/m2ux/prosiform/git/ref/tags/contract/v0.17.0
{"object":"912248e7cccb01dc232a3b6ba17ba6b4c7c5460f","ref":"refs/tags/contract/v0.17.0","type":"tag"}
$ gh api repos/m2ux/prosiform/git/ref/tags/python/v0.17.0
{"object":"7249d0997b7fa607751c8c5215e5a8293fa452c2","ref":"refs/tags/python/v0.17.0","type":"tag"}

contract/v0.17.0 -> b10437ea7f064715f54e192fad415aba0bdfe692
python/v0.17.0   -> b10437ea7f064715f54e192fad415aba0bdfe692
```

The tags were pushed only after the head's `Checks` run reported `completed success`, so no tag names a commit whose continuous integration is unverified.

## Pull request

```text
$ gh api repos/m2ux/prosiform/pulls/678
{"state":"open","draft":false,"mergeable":true,
 "head":"release/v0.17.0","head_sha":"b10437ea7f064715f54e192fad415aba0bdfe692",
 "base":"main","number":678}
```

## Check conclusions

```text
$ gh api repos/m2ux/prosiform/actions/runs/42256282157
run: completed success   head_sha: b10437ea7
$ gh api repos/m2ux/prosiform/commits/b10437ea7…/check-runs
Checks: completed success
```

`Checks` is the only check the repository's workflow declares for a pull request, so there is no second conclusion to read.

## Epic readback

```text
W01 → commit 9380588ce   ✓
W02 → #678    AC2
W03 → #678    AC3, AC4
W04 → #678    AC5, AC6
AC1–AC6 all ticked
```

The rows stay undelivered, and the epic stays open, until the pull request merges: `sync.py` reports `undelivered W02, W03, W04` because an open pull request does not deliver a task.

## Left to the user

- **The merge.** `main` carries a `pull_request` rule with `required_approving_review_count: 1`. This session supplies no approval and does not self-approve, so the pull request is handed over unmerged.
- **Nothing else.** The branch, both tags and the pull request exist; `main` reports `0.17.0` once the merge lands.
