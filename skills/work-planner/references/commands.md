# Commands

Every command that several of the skill's procedures run, one spec per operation. A procedure names a spec by linking to it.

## Issues

### Fetch Issue

Saves an issue whole, as JSON, for the scripts that read issues.

```bash
gh api repos/{owner}/{repo}/issues/943 > issue-943.json
```

### Fetch Body

Saves an issue's body alone, for [Check Dependencies](#check-dependencies), the renumber scripts and an original-body comment.

```bash
gh api repos/{owner}/{repo}/issues/943 --jq .body > live-943.md
```

### List Initiative Titles

Lists every numbered initiative, epic and task title, for finding the next initiative number. A proposal has no prefix, so it is not listed.

```bash
gh api --paginate "repos/{owner}/{repo}/issues?state=all&per_page=100" --jq '.[] | select(.pull_request==null) | .title' | grep '^\[I[0-9]'
```

### Find User

Prints the login `gh` runs as, the user assigned to work from Ready on.

```bash
gh api user --jq .login
```

### Fetch Comments

Prints an issue's comments.

```bash
gh api --paginate repos/{owner}/{repo}/issues/874/comments
```

### Create Issue

Creates an issue from a body file, with its title and labels, and prints its number.

```bash
gh api --method POST repos/{owner}/{repo}/issues -f title='[I07:E00] Name: Subtitle' -F body=@epic.md -f 'labels[]=type:epic' -f 'labels[]=enhancement' --jq .number
```

### Patch Body

Replaces an issue's body from a file.

```bash
gh api --method PATCH repos/{owner}/{repo}/issues/943 -F body=@epic.md --jq .number
```

### Retitle Issue

Replaces an issue's title.

```bash
gh api --method PATCH repos/{owner}/{repo}/issues/943 -f title='[I07:E00] Name: Subtitle' --jq .title
```

### List Labels

Lists the labels that exist in the repository.

```bash
gh api "repos/{owner}/{repo}/labels?per_page=100" --jq '.[].name'
```

### Add Labels

Adds labels to an issue.

```bash
gh api --method POST repos/{owner}/{repo}/issues/943/labels -f 'labels[]=type:epic' --jq '.[].name'
```

### Comment on Issue

Posts a comment: one line inline, anything longer from a file.

```bash
gh api --method POST repos/{owner}/{repo}/issues/637/comments -f body='Delivered by #950.' --jq .html_url
gh api --method POST repos/{owner}/{repo}/issues/874/comments -F body=@comment-874.md --jq .html_url
```

### Close as Completed

Closes an issue whose normal delivery checks and [Issue Closure](work-breakdown.md#issue-closure) pass.

- Refresh the evidence with [Capture Issue Development](work-breakdown.md#capture-issue-development) immediately before this call. Use absolute evidence paths when changing directory, and the issue's repository and number in the REST path.
- The closure gate must exit 0 before the PATCH executes. A sync report of closable supplies the normal delivery check, not permission to skip this gate.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/closure.py --issue /tmp/issue-943.json --development /tmp/development-943.json --prs /tmp/development-prs-943.json && gh api --method PATCH repos/{owner}/{repo}/issues/943 -f state=closed -f state_reason=completed --jq .state
```

### Development Access

Reads and edits GitHub Development links through authenticated GitHub or an available supported tool.

- Follow [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue). The issue's Development sidebar supports selecting pull requests across repositories.
- Read the actual field, including every page and state; record repository and number for each link. A missing tool or inaccessible field is a blocker, not an empty link set.
- Confirm the [Issue Closure](work-breakdown.md#issue-closure) repository prerequisite before linking or merging. Observe the repository setting, or obtain the user's explicit confirmation; an absent API field is unknown.
- After a link edit, re-read the field to verify it. Removing a link follows [Issue Closure](work-breakdown.md#issue-closure).

## Sources

## Pull Requests

### Fetch Pull Request

Appends one pull request, as one JSON line, to the file [Match Pull Requests](sync-mode.md#match-pull-requests) reads. A row that links a number that file does not hold is fetched this way.

```bash
gh api repos/{owner}/{repo}/pulls/439 --jq . >> prs.json
```

### Fetch Initiative Pull Requests

Saves the task and epic pull requests that name one initiative's epics.

```bash
gh api --paginate "repos/{owner}/{repo}/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I07"))' > prs.json
```

### Fetch Pull Request Issue Links

Saves each pull request's Development-linked issues as a JSON array for the scripts' `--links` input.

- Read every pull request in `prs.json` through [Development Access](#development-access), and repeat after a link changes.
- Save one entry per pull request in `links.json`, with every linked issue's repository and number. An observed empty field uses an empty array. An unreadable field leaves the fetch incomplete.

```json
[
  {
    "repo": "owner/repo",
    "number": 950,
    "closingIssuesReferences": [{"repo": "owner/repo", "number": 637}]
  }
]
```

### Retarget Pull Request

Points a pull request at another base branch, such as its epic's base branch.

```bash
gh api --method PATCH repos/{owner}/{repo}/pulls/950 -f base='i07/e00/main' --jq .base.ref
```

### Patch Pull Request Body

Replaces a pull request's body.

- The file is the whole body. The issue a pull request delivers is linked on the pull request itself, so this call leaves that link standing.

```bash
gh api --method PATCH repos/{owner}/{repo}/pulls/950 -F body=@pr-950.md --jq .html_url
```

### Update Review Pull Request

Adds a merged task pull request's change to the review pull request that merges the epic base it landed in.

- Run it after [Sync Epic](#sync-epic), on the session that merged, as the [Work Breakdown Guide](work-breakdown.md#review-pull-request) states.
- The first call prints the review pull request's number, by the epic base as head. It prints nothing while no pull request merges that base, and the base opens as a draft first.
- The second writes the current body to a file. The unit's change goes under Changes, beneath the heading for its area or a new one, and its pull request is appended to References as the next R number.
- The third replaces the body with that file.

```bash
gh api "repos/{owner}/{repo}/pulls?state=open&head={owner}:i07/e00/main" --jq '.[0].number'
gh api repos/{owner}/{repo}/pulls/980 --jq .body > review-980.md
gh api --method PATCH repos/{owner}/{repo}/pulls/980 -F body=@review-980.md --jq .html_url
```

### List Epic Bases

Prints one epic's base branch names, one per line.

- A base is `i07/e00/<name>` whose `<name>` is a long-lived branch, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- [Find Available Work](#find-available-work) takes these names as `--bases`.

```bash
git ls-remote --heads origin 'refs/heads/i07/e00/*' | cut -f2 | sed 's|refs/heads/||'
```

### Update Task Branch

Merges the epic base into the unit's task branch.

- Run it in the unit's worktree when [Merge Pull Request](work-breakdown.md#merge-pull-request) is refused, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- Then run [Merge Pull Request](work-breakdown.md#merge-pull-request) again.
- A conflict stops the update. The pull request stays open, and the conflict is reported.

```bash
git fetch origin i07/e00/main && git merge --no-edit origin/i07/e00/main && git push origin HEAD:refs/heads/i07/e00/w01-queue-plan
```

### Link Pull Request to Issue

Sets the [Issue links](work-breakdown.md#delivery) relation through [Development Access](#development-access).

- Open the issue's Development selector, select the pull request's repository and pull request, and verify the saved link.
- Refresh [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) after the edit.

## Project Boards

### Find Theme Board

Prints the number of the open board for one theme, by the theme's name that opens its title.

```bash
gh api --paginate "users/{owner}/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | startswith("Canon: ")) | .number'
```

### Create Board

Copies the Initiative Template into a new open board, links the copy to the repository, and prints the new board's number.

- The template is the open board titled `Initiative Template`. The copy carries its Status options: Backlog, Ready, In Progress, In Review and Done.
- The title is the new board's title: a theme board's title from [Themes and Boards](../SKILL.md#themes-and-boards).
- The copy's JSON is one project, and `.number` is the new board.

```bash
gh api --paginate "users/{owner}/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "Initiative Template") | .number'
gh project copy 1 --source-owner {owner} --target-owner {owner} --title 'Canon: Definitions Checked Against the Design Canon' --format json --jq .number
gh project link 13 --owner {owner} --repo {repo}
```

### Create Proposals Board

Copies the Proposals Template into a new open board, links the copy to the repository, and prints the new board's number.

- The template is the open board titled `Proposals Template`. The copy carries its Status options, listed under Proposals in [Themes and Boards](../SKILL.md#themes-and-boards).
- The title is `Proposals`.

```bash
gh api --paginate "users/{owner}/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "Proposals Template") | .number'
gh project copy 14 --source-owner {owner} --target-owner {owner} --title 'Proposals' --format json --jq .number
gh project link 15 --owner {owner} --repo {repo}
```

### Fetch Board Fields

Saves a board's fields.

```bash
gh api --paginate "users/{owner}/projectsV2/9/fields?per_page=100" > fields.json
```

### Find Status Field

Prints the id of a board's Status field.

```bash
gh api --paginate "users/{owner}/projectsV2/9/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

### Fetch Board Items with Status

Saves a board's items with their Status, each carrying its issue whole.

```bash
gh api --paginate "users/{owner}/projectsV2/9/items?per_page=100&fields=419167630" > items.json
```

### Set Item Status

Sets one board item's Status. The body names the Status field id and the option id, both taken from [Fetch Board Fields](#fetch-board-fields): `{"fields":[{"id":419167630,"value":"OPTION"}]}`.

```bash
gh api --method PATCH users/{owner}/projectsV2/13/items/1001 --input status-backlog.json --jq .id
```

## Planning records

### Add Planning Record

Adds the folder for one planning record on the long-lived engineering worktree.

- The path is `artifacts/planning/<yyyy-mm-dd>[-<ref>]-<slug>/`. The date is the day the record is opened.
- `<ref>` is the bare number of the issue or the pull request the record is for. A record for ad hoc work, which has neither, has no ref segment.
- The slug is lowercase words separated by hyphens, a short name of the work.
- The folder's files are the [planning layout](planning-layout.md).
- Edits are made on that worktree. The engineering branch takes no further worktree and no branch.

```bash
mkdir -p artifacts/planning/<yyyy-mm-dd>[-<ref>]-<slug>
```

## Sessions

### Create Task Worktree

Cuts the worktree and branch one unit's session works in, from the epic's base branch.

- The worktree, the branch and the base are the ones [Find Available Work](#find-available-work) names, with the branch following the [Work Breakdown Guide](work-breakdown.md#delivery).
- When the unit line names several bases, cut from the one for the long-lived branch the unit changes.
- Run it in the checkout of the repository the work changes.

```bash
git fetch origin i07/e00/main && git worktree add .worktrees/i07-e00-w01 -b i07/e00/w01-queue-plan origin/i07/e00/main
```

### Create Pull Request Worktree

Cuts the worktree [Understand Mode](understand-mode.md#procedure) measures a pull request in, at its head commit.

- Run it in the checkout of the repository the pull request changes.
- The worktree is detached at the head commit, so the graph reads the change as the reviewer meets it.

```bash
git fetch origin pull/950/head && git worktree add --detach .worktrees/review-950 FETCH_HEAD
```

## Graph

### Graph Conventions

Every graph command runs in the worktree [Create Pull Request Worktree](#create-pull-request-worktree) cut, and prints JSON carrying a `staleness` block. A block reporting the index behind sends the run back to [Index Repository](#index-repository), as [Understand Mode](understand-mode.md#rules) states under Fresh index.

### Index Repository

Indexes the repository, which an unindexed or behind repository needs before any measurement.

```bash
gitnexus analyze
```

## Scripts

### Check Dependencies

Checks the task dependency graph across the epics given, and with `I=` the initiative's Depends on cells.

- Initiative edges follow the [whole-epic prerequisite rule](work-breakdown.md#tables); narrower dependencies stay in the task graph.

- It also reports dependencies listed twice or already implied, and Joins pairs.
- It prints each pair of tasks in an epic where neither depends on the other and the two do not name each other in Joins.
- It prints each whole-epic dependency with that epic's row count, the binding row and its level, and the earliest row and its level.
- It reads bodies from [Fetch Body](#fetch-body), or local drafts.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/deps.py I=live-936.md E00=live-943.md E01=live-937.md
```

### Renumber Tasks

Renumbers one epic's tasks by the map given, in the files given.

- It renumbers `E01 Wxx` and `E01:Wxx` everywhere, and bare `Wxx` inside E01's own body.
- It rewrites and refuses as [Renumber Epics](review-passes.md#renumber-epics) does.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/renumber.py --initiative 07 --epic 1 --own live-937.md --tasks 7:3,3:5 live-*.md
```

### Check Format

Checks one issue against its template, and with `--fix` writes the body with the mechanical fixes made.

- It reads the format from `templates/`, and checks that every criterion is delivered by a Work Breakdown row.
- An epic's check takes its initiative's JSON, which lists the epic issues its references link to.
- An initiative's takes each epic's JSON with `--epic`, whose title names its row.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/format.py issue-943.json --initiative issue-936.json --fix fixed-943.md
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/format.py issue-936.json --epic issue-943.json --epic issue-937.json --fix fixed-936.md
```

### Delivery State

Shared report meanings and inputs for matching pull requests and syncing epics.

- A merged pull request no row links is unmatched, and an open one no row links is in flight.
- A row that links a merged pull request while a criterion its Coverage names is unticked is unmet.
- A linked pull request whose title names another epic is a conflict, and it delivers the task once it has merged.
- A linked pull request absent from the given pull requests is reported and does not deliver the task. [Fetch Pull Request](#fetch-pull-request) appends it, and the command is run again.
- `--links` is the file [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) writes for those pull requests, which every call given `--prs` carries.

### Sync Task Issue

Records the pull request that delivered a task issue, ticks its criteria, and reports whether it is closable.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/sync.py issue-637.json --prs prs.json --pr 950 --tick AC1 --fix fixed-637.md
```

### Sync Epic

Links each named task's id to a pull request naming the epic, open or merged, and ticks Done on a row once it is complete.

- It reports [Delivery State](#delivery-state).
- It reports each disagreement between a linked pull request's test plan and the rows it delivers, as the [Work Breakdown Guide](work-breakdown.md#delivery) states under Test plan.
- A row whose id links its task issue links the pull request instead.
- A task is delivered as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- A pull request whose head is an epic base merges that base, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines, and is not matched to a task.
- It takes the epic's task issues, and the issue links from [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links). A linked pull request that does not link a task's issue, and a review pull request that does not link the epic's issue, are reported uncited, as the [Work Breakdown Guide](work-breakdown.md#delivery) states under Issue links.
- A task issue whose id is not a row is reported unplaced, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- When a task has merged into an epic base and the epic is not yet complete, that base is reported draft, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- It reports a review pull request whose References differ from the task pull requests merged into its base, naming both sets, as the [Work Breakdown Guide](work-breakdown.md#review-pull-request) states.
- When every row is delivered and every criterion is ticked, an epic base its pull requests target that has not merged is reported unmerged. A draft pull request is named draft. The epic is closable as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- `--project` is a checkout of the project, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines. Without those names, an epic that would otherwise be closable is not.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/sync.py issue-943.json --prs prs.json --links links.json --tasks issue-637.json --link W01=950,W02=950 --project <checkout> --fix fixed-943.md
```

### Sync Initiative

Reports an initiative's delivery state against its epics, and ticks Done on an epic row whose issue is closed as completed.

- It takes each epic's JSON fetched after closing and reports closable as the [Work Breakdown Guide](work-breakdown.md#delivery) defines.
- An open, missing or cancelled epic keeps its row undelivered, including when all initiative criteria are ticked.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/sync.py issue-936.json --epics issue-943.json issue-937.json
```

### Plan Board Changes

Derives each issue's Status and assignees, and prints the call for each issue to add, item to remove, Status to set and assignee to add or remove.

- Give an issue it reports unresolved with `--others`.
- `--assignee` is the user [Find User](#find-user) prints.
- `--links` is the file [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) writes for those pull requests, and is where the issue a pull request delivers is read. A call without it is refused.
- An open initiative or epic whose criteria are all ticked is In Review. An epic with an open pull request and a criterion unticked is In Progress.
- An initiative or an epic with no open pull request and unticked criteria keeps Ready or Backlog, and keeps In Progress when delivery has started. In Review then becomes In Progress. One not yet on the board is added at Backlog, or at In Progress when delivery has started. [Advance Mode](advance-mode.md#rules) sets the queue.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/board.py issue-936.json --epics issue-943.json issue-937.json --tasks issue-637.json --prs prs.json --links links.json --board users/{owner}/projectsV2/9 --fields fields.json --items items.json --out board/ --assignee m2ux
```

### Find Available Work

Reports each unit of work a theme board makes available, each row a session holds, and each row its dependencies block.

- The rules are [Deliver Mode](deliver-mode.md).
- `--items` is [Fetch Board Items with Status](#fetch-board-items-with-status). `--prs` is [Fetch All Initiative Pull Requests](board.md#fetch-all-initiative-pull-requests).
- Give an issue it reports unresolved with `--others`.
- `--project` is a checkout of the project, as the [Work Breakdown Guide](work-breakdown.md#delivery) defines. A base whose last segment is not one of those names is ignored.
- `--bases` is the list [List Epic Bases](#list-epic-bases) prints for the board's epics, comma-separated.
- A `unit` line names the tasks of one session's work, their coverage, and the record folder, branch, base and worktree their ids and Description give them. One base is `base i07/e00/main`. Several are `bases i07/e00/main i07/e00/workflows`.
- A `hold` line names a row a session holds, and the record it links.
- A `blocked` line names a free row whose dependencies are undelivered, or whose joined task is unavailable.
- A `merge` line names an open pull request whose test plan has passed, and the epic base it targets. [Deliver Mode](deliver-mode.md) merges it on the run.
- `--date` opens the records on another day than today.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/deliver.py --items items.json --prs prs.json --project <checkout> --bases i07/e00/main,i07/e00/workflows
```

### Summarise Progress

Prints the standup from [Fetch Board Items with Status](#fetch-board-items-with-status) and [Fetch All Initiative Pull Requests](board.md#fetch-all-initiative-pull-requests).

- `--links` is the file [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) writes for those pull requests, and is where the issue a pull request delivers is read. A call without it is refused.
- `--since` opens the window on another date than a week before today.
- `--initiative I08` limits it to one initiative, or `owner/repo:I08` where that number names initiatives in several repositories.
- `--initiatives` gives the initiatives off the board, each from [Fetch Issue](#fetch-issue).
- `--summary` gives the paragraph for management.

```bash
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --since 2026-09-21 --initiative I08
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --initiatives issue-946.json
cd <workspace> && <workspace>/scripts/sbx python3 skills/work-planner/scripts/progress.py --items items.json --prs prs.json --links links.json --since 2026-09-21 --initiative I08 --summary summary.txt
```
