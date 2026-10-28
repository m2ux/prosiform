# Prosiform

## Dispatch

Hand the named bundle to one sub-agent, with the inputs the invoking step names, to follow from its start, and continue with the result it returns. A dispatched run puts no question to the user: it returns each question, with its context paragraph and options, unanswered. The dispatching session puts each returned question to the user, or returns it in turn when itself dispatched, then dispatches again with the answers.

# Advance Mode

Decides which initiatives and epics on a theme board are underway and which are next, from current recorded delivery.

Follow the [Procedure](#procedure), adhering to [Rules](#rules) and [Conventions](#conventions) and ensure all [Outcomes](#outcomes) are met.

## Procedure

### 1. Select the Board

Apply [Select Project Board](#select-project-board) with the requested theme or board identity.

- Use the returned owner and board number for [2. Sync](#2-sync) and [3. Read the Evidence](#3-read-the-evidence).
- Resolve a pending theme selection before continuing.

### 2. Sync

Follow [Sync Mode](#dispatch-sync-mode) for each open initiative on the selected board, with the allowance the caller supplied.

- Wait for its saved delivery results before [3. Read the Evidence](#3-read-the-evidence).
- Return any blocker that prevents current delivery from being established.

#### Dispatch Sync Mode

Dispatch `modes_sync-mode.bundle.md` to a sub-agent, as [Dispatch](#dispatch) states.

### 3. Read the Evidence

Apply [Read Board Delivery Evidence](#read-board-delivery-evidence) with the selected board owner and number, authenticated access, output paths and destination snapshot files.

- Return incomplete evidence as a blocker.

### 4. Apply the Queue

Apply [Apply Board Queue](#apply-board-queue) with the board identity, the returned board items with Status, initiative pull request records, board fields and assignee login, an output directory such as `board/`, every resolved off-board issue file and every confirmed unplanned initiative identity.

- Return a reference it reports as missing evidence as a blocker; the queue stays pending.
- When it returns pending decisions, settle them in [5. Decide](#5-decide), then return to [3. Read the Evidence](#3-read-the-evidence).

### 5. Decide

For each pending `order` or `ask` line, a re-prioritisation as [Report Lines](#report-lines) states, apply [Settle Plan Change](#settle-plan-change) with the line, the initiatives it names, its [recommended decision](#recommended-decisions), those initiatives' identities, the allowance the caller supplied and the run's [change list](#change-list).

- For each initiative an applied option or answer numbers, apply [Save Tracker Issue](#save-tracker-issue) with its identity and the [priority label](#priority-sets) that number names, with the label's colour and description.
- Add each initiative an `ask` answer leaves with no number to the confirmed unplanned initiative identities.
- A held or unanswered line leaves the queue pending: report it and continue at [6. Report](#6-report).

### 6. Report

Report each move and each `order`, `ask`, `wait` and `next` line using [Report Lines](#report-lines).

- Return the change list with the queue, so the caller reports each decision this mode made and each it held.

## Outcomes

- **A queue.**
  The user has a queue for one theme: which initiatives are underway together, which are next, and which wait.
- **A parallel work map.**
  Initiatives ranked with the same priority run together. One left unordered waits.
- **Epics follow the initiative.**
  On the initiative that is underway, the epics planned to start together can start, and a partly completed epic stays underway.

# Rules

- **Decisions.**
  A question the user must decide is put as an interview, one question at a time. A decision the run's [allowance](#allowance) covers is taken with its recommended option rather than asked. Record each decision in the affected issues and, when there is one, the planning record.
  - A plain-language paragraph before the question gives the context the user needs to answer it.
  - The question offers more than one choice. The recommended choice is marked on its option.
  - Wait for the user's answer. An unanswered question stays pending. A recommendation or elapsed time supplies no answer.
  - The user can select Other and specify a response beyond the options.
  - Use the native tool for presenting the question when one is available.
- **Layers.**
  Modes, protocols, artifacts. A mode aggregates protocol calls, as an application calls services; a protocol applies artifact operations and follows other protocols; an artifact does neither. A call goes down the stack, never up. A mode reaches an artifact operation directly only where no protocol owns that change.
- **Execution.**
  A call passes its named inputs. A protocol is one change that lands in several artifacts together, and is followed whole. Follow another mode, a protocol or a named procedure subsection, and apply an artifact operation, only where the procedure calls for it; finish that call and return its result before continuing. Calls run in order. A step's `⇉` call runs in a sub-agent, and its `⫽` calls run in sub-agents together, as the bundle's Prosiform section states; those together never write to the same object.

# Conventions

- **Session.**
  Once per session, before the first `gh` call, unset `GH_TOKEN` and `GITHUB_TOKEN` so `gh` uses its keyring login. Where shell state does not persist between commands, confirm instead that neither is set in the shell profile.
- **Repository.**
  `gh` resolves `{owner}/{repo}` from the git remote of the directory it runs in, so run `gh` commands inside a checkout of the repository that holds the issues. `{other}` is a further repository the board's issues live in.
- **Bodies.**
  - Bodies and long comments always go through a file (`-F body=@file`), never inline, which avoids quoting.
  - **Example.**  workflow-server's dynamic-shell restrictions deny a body inlined in the command.
  - Keep these files in a working directory outside the repository.
- **Scripts.**
  Scripts run under `sbx`, invoked by its absolute path from `<workspace>`, the checkout holding this skill.
- **Boards.**
  A project board sits under `users/{owner}`, or `orgs/{owner}` when `gh api repos/{owner}/{repo} --jq .owner.type` is `Organization`.
- **Example values.**  Substitute the real ones:
  - `936` an initiative issue, `943` and `937` its epics, `637` a task issue, `874` an orphan, `946` an initiative off the board, `960` a proposal;
  - `950` a pull request, `I07` and `I08` initiative numbers;
  - board `9`, workflow-server's Canon theme, and `419167630` its Status field id;
  - `1` the Initiative Template board, `13` a board copied from it;
  - `14` the Proposals Template, `15` the Proposals board;
  - `m2ux` the user.
  - `<checkout>` any checkout of the project, a linked worktree included.

# Artifacts

## Board

### Operations

#### *Select* Project Board

The theme or proposals board the request names.

**Inputs:** Board owner and either a theme name or the proposals-board selection.

##### 1. Find the Named Board

Run [Find Theme Board](#find-theme-board) for the named theme, or [Find Proposals Board](#find-proposals-board) when the request names proposals. The selection meets [Themes](#themes) or [Proposals](#proposals).

##### 2. Report a Missing Board Selection

Return a missing-selection result when neither a theme nor proposals is specified; the caller obtains that choice.

##### 3. Return the Selected Board Number

Return the selected board number, or an absent-board result for [Copy Project Board](#copy-project-board). Work one board at a time.

#### *Copy* Project Board

A missing theme board, or a missing proposals board.

**Inputs:** Board owner, repository, selected board kind, theme title and originating proposal record when applicable.

##### 1. Create an Absent Proposals Board

When no open board is titled `Proposals`, apply [Create Proposals Board](#create-proposals-board). The copy source and the title meet [Proposals](#proposals).

##### 2. Create an Absent Theme Board

When the selected theme board is absent:

- Apply [Create Theme Board](#create-theme-board) with the owner, repository, theme title and originating proposal record when applicable.
- Require the new theme's label and board before an initiative takes that theme.

#### *Create* Proposals Board

A new proposals board linked to the supplied repository.

**Inputs:** Board owner and repository.

##### 1. Find the Proposals Template

Run [Find Board Template](#find-board-template) with the owner and the exact title `Proposals Template`.

##### 2. Use the Proposals Template as Source

Use the returned number as the copy source.

##### 3. Copy the Proposals Template

Run [Copy Board Template](#copy-board-template) with that template number, the owner and the title `Proposals`.

##### 4. Retain the Proposals Board Number

Retain the new board number. The copy meets [Proposals](#proposals).

##### 5. Link the Proposals Board to the Repository

Run [Link Board to Repository](#link-board-to-repository) with the owner, new board number and repository.

##### 6. Return the Proposals Board Number

Return the new board number after linking succeeds.

#### *Create* Theme Board

A new theme board linked to the supplied repository.

**Inputs:** Board owner, repository, theme title and originating proposal record when applicable.

##### 1. Require the Originating Proposal

Require the originating proposal record for a proposal-derived board; return a missing-input finding when its designator is unavailable.

##### 2. Find the Initiative Template

Run [Find Board Template](#find-board-template) with the owner and the exact title `Initiative Template`.

##### 3. Use the Initiative Template as Source

Use the returned number as the copy source.

##### 4. Copy the Initiative Template

Run [Copy Board Template](#copy-board-template) with that template number, the owner and the title required by [One Board Per Theme](#one-board-per-theme).

##### 5. Retain the Theme Board Number

Retain the new board number. The copy carries the template's Status options: Backlog, Ready, In Progress, In Review and Done.

##### 6. Link the Theme Board to the Repository

Run [Link Board to Repository](#link-board-to-repository) with the owner, new board number and repository.

##### 7. Return the Theme Board Number

Return the new board number after linking succeeds.

#### *Read* Board State

The selected board's items and status fields.

**Inputs:** Existing board owner and number, as [Select Project Board](#select-project-board) or [Copy Project Board](#copy-project-board) returns them, whether the caller ran that operation or carries its result.

##### 1. Find the Board Status Field

Run [Find Status Field](#find-status-field) for the board number.

##### 2. Fetch Board Items with Status

Run [Fetch Board Items with Status](#fetch-board-items-with-status), passing that field id and board number.

##### 3. Return the Board State

Return the items, Status field, item ids and the board's [Repositories](#repositories) to the caller.

#### *Read* Board Assignee

The authenticated login available for board assignments.

**Inputs:** Authenticated repository access.

##### 1. Find the Board User

Run [Find User](#find-user).

##### 2. Return the Assignee Login

Return its login for the caller's assignment decisions.

#### *Read* Board Configuration

One board's field definitions and requested item state.

**Inputs:** Board owner and number, output paths and optional item identity.

##### 1. Fetch the Configured Board Fields

Run [Fetch Board Fields](#fetch-board-fields) for the supplied board.

##### 2. Fetch the Requested Board Item

When a single item is requested for write confirmation, run [Fetch Board Item](#fetch-board-item). A list snapshot may lag a write.

##### 3. Return the Board Configuration

Return the field definitions and requested current item.

### Fields

#### Themes

Every initiative belongs to one theme, and each theme has one project board. Each project names its own themes.

- **Example.**  workflow-server's themes.

| Theme | Label | Description |
| --- | --- | --- |
| Canon | `theme:canon` | Definitions Checked Against the Design Canon |
| Language | `theme:language` | The Definition Language and Its Rules |
| Mechanical | `theme:mechanical` | The Engine That Runs Definitions |
| Delivery | `theme:delivery` | What Reaches Agents and Hosts |

#### One Board Per Theme

- A proposal-derived board title is the originating proposal's exact `[Pxx]` designator, a space, the theme name, a colon, and its description: `[P03] Canon: Definitions Checked Against the Design Canon`. Preserve the proposal's digits exactly. A board with no originating proposal uses `Name: Description`.
- It is linked to the repository.
- It holds the theme's initiatives, their epics and their task issues.

#### Repositories

A board's repositories are those its items' issues live in, read from each item's issue, deduplicated and ordered with the board's own repository first. An item whose issue is unreadable leaves the list incomplete, which is reported rather than filled by assumption.

#### Assignees

An issue at Ready, In Progress, In Review or Done is assigned to the user; one in Backlog has no assignee. An assignee is set on the issue, not on the board item, so the call that changes one acts on the issue.

#### Proposals

- The board is titled `Proposals`. It holds proposal issues, the incoming funnel for work that may become an initiative.
- Its copy source is the open board titled `Proposals Template`. That template carries Priority: High, Medium and Low, and its view is a board grouped by Status.
- **Suggested.**
  Raised, and nobody has taken it up. A new proposal lands here, with no assignee.
- **Considering.**
  Someone is weighing the goal, the evidence and the criteria. That person is the assignee.
- **Approved.**
  Qualified to become an initiative. The assignee is the user.
- **Held.**
  Not now. It stays on the board, with no assignee.
- **Declined.**
  It will not become an initiative. It has no assignee.

### Commands

#### Find Board Template

Prints the number of the open board with the supplied exact template title.

**Inputs:** Board owner and template title.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

#### Copy Board Template

Copies the supplied template into a new open board with the supplied title and prints its number.

**Inputs:** Board owner, template board number and new board title.

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

#### Link Board to Repository

Links one board to the supplied repository.

**Inputs:** Board owner, board number and repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

#### Find Proposals Board

Prints the number of the open board titled `Proposals`.

**Inputs:** Board owner.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "Proposals") | .number'
```

#### Fetch Board Fields

Saves a board's fields.

**Inputs:** Board owner, board number and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

#### Find Theme Board

Prints the number of the open board for one theme, by its theme name after any proposal designator.

**Inputs:** Board owner and theme name.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("<theme-name>: ")) | .number'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("Canon: ")) | .number'
```

#### Find Status Field

Prints the id of a board's Status field.

**Inputs:** Board owner and number.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

#### Fetch Board Items with Status

Saves a board's items with their Status, each carrying its issue whole.

**Inputs:** Board owner and number, Status field id and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/items?per_page=100&fields=<status-field-id>" > '<board-items-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/items?per_page=100&fields=419167630" > items.json
```

#### Fetch Board Item

Reads one board item, including its current Status.

**Inputs:** Board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

#### Find User

Prints the login `gh` runs as, the user assigned to work from Ready on.

**Inputs:** Authenticated repository access.

```bash
gh api user --jq .login
```

## Delivery Evidence

### Operations

#### *Read* Board Delivery Evidence

The board snapshot and pull request records that establish current delivery across one board.

**Inputs:** Board owner and number, authenticated access, output paths and destination snapshot files.

##### 1. Apply the Board Reads

Apply the [board reads](#run-board-reads).

##### 2. Return the Board Delivery Evidence

Return the [board snapshot](#board-snapshot), pull request records and complete issue-link snapshot to the caller, reporting incomplete evidence as a blocker.

##### Run Board Reads

###### 1. Read Board State

Apply [Read Board State](#read-board-state) with the board owner and number for its items, Status field and [repositories](#repositories).

###### 2. Fetch Initiative Pull Requests

Apply [Fetch All Initiative Pull Requests](#fetch-all-initiative-pull-requests) for each repository Read Board State returned, for the pull request records.

###### 3. Fetch Pull Request Issue Links

Apply [Fetch Pull Request Issue Links](#fetch-pull-request-issue-links) with the pull request records Fetch Initiative Pull Requests returned, for the complete issue-link snapshot.

###### 4. Read Board Configuration

Apply [Read Board Configuration](#read-board-configuration) with the board owner and number and output paths for the board fields.

###### 5. Read Board Assignee

Apply [Read Board Assignee](#read-board-assignee) for the assignee login.

### Fields

#### Board Snapshot

The board items with their Status, the Status field, the board fields, the board's [repositories](#repositories) and the assignee login, read together with the board's pull request records and issue-link snapshot.

## Board Queue

### Operations

#### *Plan* Board Queue

Derives the queue from supplied board and delivery snapshots and confirmed decisions.

**Inputs:** Board identity, current board items with Status, initiative pull request records, board fields, assignee login, output directory, resolved off-board issue files and confirmed unplanned initiative identities. The caller supplies the delivery state.

##### 1. Compute the Board Queue

Run [Compute Board Queue](#compute-board-queue) with the snapshots as `--items`, `--prs` and `--fields`, the board as `--board`, the login as `--assignee`, the output directory as `--out`, every resolved issue file as `--others` and every confirmed unplanned initiative as `--unplanned`.

- The queue must meet [Fields](#fields-2).
- Refuse a Status change outside Backlog, Ready and In Progress, identifying the issue. In Review, Done and task issues are outside the write scope.

##### 2. Return the Proposed Queue Calls

Return the proposed Status and assignee calls, report lines and unresolved issue references to the caller.

- Distinguish pending decisions and missing evidence as [Completeness](#completeness) defines.
- Report each [unresolvable dependency](#unresolvable-dependencies) with the row and the entry, and leave that row's epic where it stands.
- The caller supplies further evidence and confirmed decisions for another pass and applies the proposed changes to tracked objects.

#### *Apply* Board Queue

The board's initiative and epic Status and assignees, moved to the queue and confirmed live.

**Inputs:** Board identity, current board items with Status, initiative pull request records, board fields, assignee login, output directory, resolved off-board issue files and confirmed unplanned initiative identities.

##### 1. Plan the Board Queue to Apply

Apply [Plan Board Queue](#plan-board-queue) with the supplied snapshots, board identity, assignee login, output directory, resolved off-board issue files and confirmed unplanned initiative identities.

##### 2. Resolve Off-Board Issue References

For each unresolved issue reference the queue returns:

- Apply [Read Tracker Issue](#read-tracker-issue) into a file.
- Add the returned file to the resolved off-board issue files.
- Apply Plan Board Queue again with the same inputs and every resolved off-board issue file.
- Repeat while references remain unresolved. On an unavailable issue, return the queue with that reference as missing evidence and stop.

##### 3. Return Pending Queue Decisions

When the queue carries an `order` or `ask` line, return the queue with those lines as pending decisions and stop. The caller settles them and applies this operation again with its confirmed priorities saved and each initiative it confirms unplanned.

##### 4. Run the Proposed Queue Calls

Run each proposed Status and assignee call. An assignee call acts on the issue, as [Assignees](#assignees) states.

- For each Status call, apply [Read Board Configuration](#read-board-configuration) with the board identity, output directory and changed item identity to confirm its current status.
- If that item still shows the preceding status:
  - Repeat its write.
  - Repeat the same item read. The item list can lag a write.

##### 5. Re-Read the Queued Board State

Apply [Read Board State](#read-board-state) for the refreshed board items.

- Apply Plan Board Queue with the refreshed board items, the same initiative pull request records, board fields, assignee login, board identity and output directory, and every resolved off-board issue file and confirmed unplanned initiative identity.
- Continue from [2. Resolve Off-Board Issue References](#2-resolve-off-board-issue-references) until the refreshed queue is [complete](#completeness) and contains no further call.

##### 6. Return the Converged Queue

Return each move applied and the converged queue's `wait` and `next` lines.

### Fields

#### Board Identity

The queue belongs to one theme board, identified as `users/{owner}/projectsV2/{id}` or `orgs/{owner}/projectsV2/{id}`. Its source snapshots contain board items with Status, board fields, initiative pull requests and any off-board issues its rows depend on.

#### Priority Sets

A parallel work map assigns a positive integer to each ranked initiative. Every initiative with the same number runs together as one set. One left unordered stays in Backlog.

The epics of one initiative carry their own sets. Every epic with the same number starts together, and a number is compared only with its siblings'.

A priority label is `priority:` and a positive integer. A larger number is higher, with no maximum. Two such labels on one issue count as the larger number. Its colour is `BFD4F2` and its description `Priority set <n>; a larger number starts sooner`, with `<n>` its integer.

#### Initiative Status

- The highest priority set is In Progress, all together. The next set is Ready, all together. Lower sets stay in Backlog. When the highest set leaves In Progress, the Ready set moves to In Progress.
- An initiative in Backlog with no priority label stays there. An initiative in Ready with no priority label moves to Backlog, with its epics.
- An initiative In Progress with no priority label needs a decision: a positive integer keeps it In Progress; none sends it to Backlog once its open pull requests have completed.
- An initiative stays In Progress while an open pull request names one of its epics, `[Ixx:Eyy]`, even when a higher set has started. The highest set moves to In Progress immediately. After the lower set's open pull requests complete, it moves to Ready if it is the next number, or Backlog if a number sits between it and the highest.
- An initiative confirmed unplanned follows the same wait, then moves to Backlog with its epics.
- An initiative In Review or Done remains in that state.

#### Epic Status

- On an initiative In Progress, a partly completed epic is In Progress even with open questions. Partly completed means a delivered task row on an epic that is not closed as completed. Delivery follows [Task Delivery](#task-delivery), using the supplied evidence.
- On that initiative, an unstarted epic can start when every prerequisite epic its initiative row names is closed as completed, all of each prerequisite's bases have merged into their long-lived branches, and the epic's Open Questions section is empty.
- Of the epics that can start, those carrying the highest priority number are next and Ready, all together. The highest counts the epics already In Progress, so an epic of a lower number waits while a higher one runs.
- An epic with no priority label ranks below every number, so it is Ready only when no labelled sibling can start or is running.
- Any other Ready epic of that initiative moves to Backlog.
- An epic In Review or Done remains in that state.
- On an initiative that moves to Backlog, its epics move to Backlog. A Ready epic of an initiative that is not In Progress moves to Backlog.

#### Task Eligibility

A task is Ready only when its epic is Ready or In Progress and every row its Depends on cell names is delivered. A row naming another epic's row waits for that epic to close, since its output reaches this epic's base when that epic's bases merge, and the rows beside it wait for nothing it waits on. The queue contains no task issue changes; task status comes from the supplied delivery state.

#### Proposed Changes

The queue contains calls for Status and assignee changes to initiatives and epics. Status changes are between Backlog, Ready and In Progress. The assignee is the login assigned to work from Ready. Call files occupy the supplied output directory, for example `board/`. They describe proposed changes, not confirmation of live board state.

#### Report Lines

| Line | When It Is Printed | What It Names |
| --- | --- | --- |
| `order` | No open initiative has a priority label | The open initiatives, including any already In Progress, for a parallel work map |
| `ask` | An initiative is In Progress and has no priority label | That initiative, for a positive integer or none |
| `wait` | An open pull request names one of an initiative's epics | That initiative and the pull request |
| `next` | An initiative is In Progress and has epics that are Ready | Those epics |

#### Recommended Decisions

The answer a caller applies where it resolves an `order` or `ask` line on its own.

- For `order`, priority 1 on every open initiative already In Progress or named by an open pull request, and no number on the rest. Where no initiative qualifies, nothing is under way and the line has no recommended answer.
- For `ask`, the number of the highest set already running, so the initiative joins it, or 1 where no initiative carries a priority label.

#### Unresolvable Dependencies

A `Depends on` entry that names no row and links no issue, names an issue the run was not given, or names a row the epic it points to does not carry, cannot resolve. No delivery makes it readable, so it is told apart from a prerequisite that has not landed.

- The report names the row and the entry as written, and a run that met one while deciding a placement exits nonzero.
- The epic that row gates keeps the Status it holds. The run proposes no move for it, so a Ready epic is not returned to Backlog on an entry nobody can read.
- Every entry of a cell is read, so a cell carrying two names both.
- A note raised while reading delivery rather than deciding a placement is reported and leaves the exit status alone.

#### Completeness

An `order` or `ask` line means a decision is pending. An unresolved issue reference means dependency evidence is missing. Either leaves the queue incomplete.

A complete queue may still propose changes. Live board state has converged when a queue derived from refreshed items is complete and contains no further call. `wait` and `next` lines remain reportable at that point.

### Commands

#### Compute Board Queue

Prints proposed Status and assignee calls, `order`, `ask`, `wait` and `next` lines, and unresolved issue references for one board queue. It exits nonzero where an [unresolvable dependency](#unresolvable-dependencies) stopped it placing a row.

**Inputs:** Current board and delivery snapshots, board identity, assignee login, output directory, resolved dependency evidence, confirmed unplanned initiatives and the permitted Status scope.

- `--items` is the board's items with Status.
- `--prs` is the pull requests that name an initiative.
- `--board` is the [board identity](#board-identity).
- `--fields` is the board's fields.
- `--out` is the directory the calls are written to.
- `--assignee` is the login assigned to work from Ready.
- `--others` is an issue file for an issue the rows depend on that is not on the board. Repeatable.
- `--unplanned` is an initiative left with no priority, an issue number or `<owner>/<repo>#<issue-number>`. Repeatable.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board-queue.py --items '<board-items-file>' --prs '<pull-request-records-file>' --board '<board-identity>' --fields '<board-fields-file>' --out '<output-directory>' --assignee '<assignee-login>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/board-queue.py --items items.json --prs prs.json --board 'users/<owner>/projectsV2/9' --fields fields.json --out board/ --assignee m2ux
```

## Plan Change

### Operations

#### *Check* Plan Change Autonomy

One pending change assessed against the run's allowance.

**Inputs:** The pending change, its subject, the option recommended for it, and the allowance the caller was supplied.

##### 1. Match the Plan Change Kind

Match the change to one kind in [Change Kinds](#change-kinds).

##### 2. Return an Automatic Plan Change

Return it as automatic where the supplied allowance names that kind, with the supplied recommendation as the option the caller applies.

##### 3. Return a Held Plan Change

Return it as [held](#held-change) otherwise.

- A change matching no kind is held, as is one matching [Initiative Creation](#initiative-creation).
- An absent allowance holds every change, so a run the user drives decides nothing on their behalf.

#### *Record* Plan Change

One entry in the run's list, for a change it applied or held.

**Inputs:** The change, its kind, the option applied or recommended, the affected issue identities and the run's current list.

##### 1. Add the Plan Change Entry

Add one entry meeting [Entry](#entry) to the supplied [Change List](#change-list), marked applied or held.

##### 2. Return the Updated Change List

Return the updated list for the caller to publish and report.

#### *Settle* Plan Change

One pending change carried to its outcome: applied, held, or answered by the user.

**Inputs:** The pending change, its subject, the option recommended for it, the affected issue identities, the allowance the caller was supplied, and the run's current [Change List](#change-list).

##### 1. Check the Plan Change Autonomy

Apply [Check Plan Change Autonomy](#check-plan-change-autonomy) with the change, its subject, the recommended option and the supplied allowance.

##### 2. Settle by the Autonomy Result

Settle the change by what it returns:

- **Automatic.**
  - Take the recommended option as the applied option.
  - Apply [Record Plan Change](#record-plan-change) with the change, its kind, that option, the affected issue identities and the current list, marked applied.
- **Held, with an allowance supplied.**
  - Leave the change unapplied, meeting [Held Change](#held-change).
  - Apply Record Plan Change with the change, its kind, the recommended option, the affected issue identities and the current list, marked held.
  - Ask nothing, since the work the run was dispatched for does not wait on an answer.
- **Held, with no allowance supplied.**
  - Put the change to the user as an [interview](#rules), with the recommended option marked, and wait for the answer.
  - Where the answer applies a change, apply Record Plan Change with the change, its kind, the option the user chose, the affected issue identities and the current list, marked applied.
  - An answer leaving the work where it is takes no entry, as [Change Kinds](#change-kinds) states.

##### 3. Return the Settled Plan Change

Return the applied option, held, or the user's answer, with the updated change list.

### Fields

#### Allowance

The caller names the change kinds its run applies without asking. A run the user drives directly is supplied none.

#### Change Kinds

| Kind | What It Covers |
| --- | --- |
| Task creation | A new task row, and the task issue that delivers it |
| Epic creation | A new epic, and the initiative row that carries it |
| Migration | Work moved from one issue to another, with the renumbering that move forces |
| Re-prioritisation | A priority label, a queue order or a board status |
| Folded work | Criteria, scope or design added to an existing issue because the work in hand needs it |

An option deciding to leave work where it is changes no plan, so it needs no allowance and takes no entry, unlike a change [held](#held-change) for the user to decide.

#### Initiative Creation

A new initiative is outside every allowance. The work stays where it is, open and unplaced, until the user decides where it belongs.

#### Change List

One list for the run, holding every change it applied and every change it held. It is what the run reports and what its record keeps.

#### Entry

One line: the kind, the issue or row it concerns, and the option applied or recommended. The entry states the change, not the alternatives weighed against it.

#### Held Change

A held change is left unapplied and its subject stays as it stands, so the next run sees the same decision. Its entry carries the recommended option, which is what the user is answering.

## Issue

### Operations

#### *Read* Tracker Issue

The current issue, its saved body and discussion.

**Inputs:** Repository, issue number and output files; whether discussion is needed.

##### 1. Fetch the Tracker Issue

Run [Fetch Tracker Issue](#fetch-tracker-issue) for the complete JSON, or [Fetch Issue Body](#fetch-issue-body) for its body, with the issue number and destination file.

##### 2. Fetch the Issue Comments

Run [Fetch Issue Comments](#fetch-issue-comments) when the request depends on the discussion.

#### *Save* Tracker Issue

One populated body and its metadata, written to the tracker.

**Inputs:** Repository, optional existing issue number, populated body file, title and labels for creation; selected body or metadata changes for an existing issue; each assigned label's colour and description. Optional comment file.

##### 1. Take the Issue Body and Metadata

Take the supplied body and metadata, preserving each field the caller does not change for an existing issue.

##### 2. Ensure the Issue Labels

Apply [Ensure Repository Labels](#ensure-repository-labels) with every label the save assigns and its colour and description.

- Return an unknown label definition to the caller before any write.

##### 3. Create New Issue

For a new issue, run [Create Tracker Issue](#create-tracker-issue) with the body's file, title and labels.

##### 4. Update the Existing Issue

For an existing issue, run [Patch Issue Body](#patch-issue-body), [Retitle Tracker Issue](#retitle-tracker-issue), [Add Issue Labels](#add-issue-labels) or [Remove Issue Label](#remove-issue-label) for the fields being changed.

##### 5. Comment on the Saved Issue

Apply [Comment on Issue](#comment-on-issue) for an answer or a preserved body the caller requires, with the issue number and comment file.

##### 6. Re-Read the Saved Issue

Re-read with [Fetch Tracker Issue](#fetch-tracker-issue).

##### 7. Compare the Saved Issue Fields

Compare the saved fields with the intended body and metadata.

#### *Close* Tracker Issue

Verified completion of an issue and its linked delivery.

**Inputs:** Issue identity, successful normal delivery result, current issue JSON, complete Development snapshot, confirmed repository setting and fresh linked pull request records.

##### 1. Capture the Issue Development

Apply [Capture Issue Development](#capture-issue-development) for the issue's complete links and confirmed repository setting.

##### 2. Take Fresh Pull Request Records

Take the caller's fresh records for every linked pull request, across repositories and states; return missing evidence to the caller.

- Return a repository setting that is unconfirmed or fails [Auto-Close Setting](#auto-close-setting) to the caller as a blocker.
- Take the records only from a fresh destination file, so an earlier snapshot cannot supply membership.
- Use the issue's entire Development field to establish membership. Titles, branch names, body mentions and a list filtered to one initiative do not establish completeness. An explicitly empty field adds no pull request requirement.

##### 3. Run the Closure Check

Run [Check Issue Closure](#check-issue-closure) with `--issue`, `--development`, and `--prs` for those fresh records.

##### 4. Require the Closure Gate

Require normal delivery checks to pass, every criterion to be verified and ticked, and every currently linked pull request to be merged.

- Keep the issue open for an open, draft, closed without merge, or unreadable linked pull request.
- Obtain the user's decision before removing an abandoned or incorrect Development link. A replacement pull request does not remove the requirement on a link still present.

##### 5. Close the Issue as Completed

Apply [Close as Completed](#close-as-completed), which repeats the gate immediately before the write. A changed link set requires another capture and check.

#### *Comment* on Issue

The supplied discussion text saved on one issue.

**Inputs:** Repository, issue number and exact comment text or file; reviewer identity and addressed feedback when replying to a review.

##### 1. Compose the Feedback Reply

When replying to feedback already folded into the body, compose a precise, factual reply addressing each point and mentioning the reviewer, with no thanks or filler. Name what the body now says, by criterion id where one carries it, or the issue that takes the point.

##### 2. Publish the Issue Comment

Publish the supplied comment:

- For a one-line comment, run [Post Inline Comment](#post-inline-comment) with the exact text.
- For a longer comment, run [Post Comment File](#post-comment-file) with the complete file.

##### 3. Return the Comment URL

Return the saved comment URL.

#### *Close* as Completed

An issue closed after its final evidence check.

**Inputs:** Repository, issue number, authenticated access, confirmed repository auto-closing setting, passing normal delivery checks and absolute paths to the current issue, Development and linked pull request evidence.

##### 1. Capture Development Before Closure

Apply [Capture Issue Development](#capture-issue-development) immediately before closure with the issue identity, authenticated access, confirmed repository setting and evidence paths.

##### 2. Compare the Development Links

Compare its links with the supplied fresh pull request records; return a changed link set or missing evidence to the caller for refresh.

##### 3. Run the Completion Gate

Run [Check Issue Closure](#check-issue-closure) with the current issue, Development and linked pull request files, using absolute evidence paths when changing directory.

##### 4. Require the Completion Gate to Pass

Require exit 0 and passing normal delivery checks; a sync report of closable does not permit skipping this gate.

##### 5. Set the Completed State

Immediately after the gate passes, run [Set Completed State](#set-completed-state) with the issue's repository and number and the passing evidence.

##### 6. Return the Completed State

Return the saved state or failure.

#### *Capture* Issue Development

The issue's current content and complete Development snapshot.

**Inputs:** Issue identity, authenticated access, observed repository auto-closing setting and issue and Development output paths.

##### 1. Read the Development Field

Apply [Read Issue Development](#read-issue-development) for the entire field across repositories and states. An inaccessible field returns incomplete evidence; an empty array means the field was checked and empty.

##### 2. Write the Development Snapshot

Run [Write Development Snapshot](#write-development-snapshot) with the issue identity, observed link set, completeness result and repository setting, saving `development-943.json` or the supplied path.

- Set `complete` true only after the full read, and `auto_close_issues` false only after the repository setting is confirmed disabled.

##### 3. Fetch the Issue Snapshot

Run [Fetch Tracker Issue](#fetch-tracker-issue) into `issue-943.json` or the supplied path.

##### 4. Return the Development Files

Return both files and any incomplete evidence. The caller supplies fresh linked pull request records in `development-prs-943.json`.

#### *Read* Issue Development

The Development links observed for one issue through authenticated GitHub.

**Inputs:** Issue identity and authenticated access.

##### 1. Read Every Development Link

Read every page and state, across repositories, recording each linked pull request's identity.

##### 2. Return the Observed Development Links

Return the observed links and whether the entire field was readable.

#### *Confirm* Repository Auto-Close

Whether the repository auto-closes issues whose linked pull requests merge, established for this session.

**Inputs:** Repository and authenticated access.

##### 1. Read the Auto-Close Setting

Read the setting where the authenticated API exposes it, and take a read value as the answer.

##### 2. Ask the User for Auto-Close

Where no API field carries it, put the setting to the user and take their explicit answer, meeting [Auto-Close Setting](#auto-close-setting).

##### 3. Return the Confirmed Auto-Close Setting

Return the confirmed value. An unconfirmed setting is a blocker, and an enabled one leaves the caller to obtain authorization before the repository is reconfigured.

### Fields

#### Auto-Close Setting

GitHub's **Auto-close issues with merged linked pull requests** repository setting, which must be disabled before a delivery pull request is linked or merged, so that closure follows the criteria rather than the merge.

- The setting is confirmed per repository and holds for the session; it is not inferred from an issue that stayed open.
- No REST field and no GraphQL field of `gh` 2.46 carries it, so on such a host the user's explicit answer is the only source.
- An enabled setting closes issues on merge whatever their criteria. Where it cannot be disabled, each affected issue's state is read after every merge and reopened where its criteria are unmet.

### Commands

#### Create Tracker Issue

Creates an issue from a body file, with its title and labels, and prints its number.

**Inputs:** Repository, populated body file, title and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F 'body=@<body-file>' -f 'labels[]=<label>' --jq .number
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues' -f title='<title>' -F body=@body.md -f 'labels[]=<label>' --jq .number
```

#### Patch Issue Body

Replaces an issue's body from a file.

**Inputs:** Repository, issue number and complete populated body file.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -F 'body=@<body-file>' --jq .number
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -F body=@body.md --jq .number
```

#### Fetch Issue Body

Saves an issue's body alone.

**Inputs:** Repository, issue number and destination file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' --jq .body > '<output-body-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' --jq .body > live-943.md
```

#### Retitle Tracker Issue

Replaces an issue's title.

**Inputs:** Repository, issue number and complete title.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f title='<title>' --jq .title
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f title='<title>' --jq .title
```

#### Add Issue Labels

Adds labels to an issue.

**Inputs:** Repository, issue number and existing label names.

Repeat `-f 'labels[]=<label>'` for each supplied label.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/labels' -f 'labels[]=<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/943/labels' -f 'labels[]=<label>' --jq '.[].name'
```

#### Remove Issue Label

Removes one label from an issue.

**Inputs:** Repository, issue number and label name.

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/<issue-number>/labels/<label>' --jq '.[].name'
```

**Example:**

```bash
gh api --method DELETE 'repos/<owner>/<repo>/issues/943/labels/<label>' --jq '.[].name'
```

#### Fetch Issue Comments

Prints an issue's comments.

**Inputs:** Repository and issue number.

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/<issue-number>/comments'
```

**Example:**

```bash
gh api --paginate 'repos/<owner>/<repo>/issues/874/comments'
```

#### Fetch Tracker Issue

Saves an issue whole, as JSON, for the scripts that read issues.

**Inputs:** Repository, issue number and destination JSON file.

```bash
gh api 'repos/<owner>/<repo>/issues/<issue-number>' > '<issue-json-file>'
```

**Example:**

```bash
gh api 'repos/<owner>/<repo>/issues/943' > issue-943.json
```

#### Check Issue Closure

Checks the issue criteria, the complete link snapshot and every linked pull request.

**Inputs:** Current issue JSON, complete Development snapshot and fresh linked pull request records.

- `--issue`, `--development`, and `--prs` are the fresh issue JSON, Development snapshot, and linked pull request records.
- Exit 0 means the closure gate passes; normal delivery checks must also pass. Exit 1 reports blockers. The command performs no network calls or writes.

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue '<issue-json-file>' --development '<development-snapshot-file>' --prs '<linked-pull-request-records-file>'
```

**Example:**

```bash
cd "<workspace>" && "<workspace>/scripts/sbx" python3 skills/work-planner/scripts/closure.py --issue issue-943.json --development development-943.json --prs development-prs-943.json
```

#### Post Inline Comment

Posts one line of exact comment text and returns its URL.

**Inputs:** Repository, issue number and one-line comment text.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -f body='<comment-text>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/637/comments' -f body='Delivered by #950.' --jq .html_url
```

#### Post Comment File

Posts a complete comment file and returns its URL.

**Inputs:** Repository, issue number and exact comment file.

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/<issue-number>/comments' -F 'body=@<comment-file>' --jq .html_url
```

**Example:**

```bash
gh api --method POST 'repos/<owner>/<repo>/issues/874/comments' -F body=@comment-874.md --jq .html_url
```

#### Set Completed State

Sets an issue to closed with the completed reason and returns its state.

**Inputs:** Repository, issue number, passing normal delivery checks and an immediately preceding successful closure gate on current evidence.

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/<issue-number>' -f state=closed -f state_reason=completed --jq .state
```

**Example:**

```bash
gh api --method PATCH 'repos/<owner>/<repo>/issues/943' -f state=closed -f state_reason=completed --jq .state
```

#### Write Development Snapshot

Saves an observed Development field and repository setting as JSON.

**Inputs:** Repository and issue number, observed links, completeness result, confirmed or unknown auto-closing setting and destination file.

Write the supplied values in this shape. Substitute the issue number as a JSON integer, completeness as a boolean, and the auto-closing setting as a boolean or `null` when unknown. Supply every observed pull request URL, or an empty array when there are none. Preserve incomplete evidence as incomplete.

```text
{
  "repo": "<owner>/<repo>",
  "number": <issue-number>,
  "complete": <complete>,
  "auto_close_issues": <auto-close-issues>,
  "pull_requests": ["<pull-request-url>"]
}
```

**Example payload:**

```json
{
  "repo": "owner/repo",
  "number": 943,
  "complete": true,
  "auto_close_issues": false,
  "pull_requests": ["https://github.com/owner/repo/pull/980"]
}
```

## Pull Request

### Operations

#### *Access* Development Links

The observed or updated Development relation for a pull request.

**Inputs:** Pull request identity, authenticated access and requested relation read or write; for an edit, the issue identity, confirmed repository prerequisite and any user decision authorizing removal of an abandoned or incorrect link, meeting the applicable preconditions in [Close Tracker Issue](#close-tracker-issue).

##### 1. Read the Pull Request Development Links

Run [Read Development Links](#read-development-links) for the actual field, including every page and state. A missing tool or inaccessible field is a blocker, not an empty link set.

##### 2. Return the Read-Only Relation

Return the complete relation for a read-only request.

##### 3. Edit the Development Links

For a link edit:

- Take the supplied repository prerequisite from [Confirm Repository Auto-Close](#confirm-repository-auto-close); an unconfirmed setting blocks the edit.
- For an addition, run [Set Development Link](#set-development-link) with the pull request and issue identities.
- For removal of an abandoned or incorrect link:
  - Require the supplied user decision.
  - Run [Remove Development Link](#remove-development-link) with those identities.

##### 4. Re-Read the Pull Request Development Links

Run [Read Development Links](#read-development-links) again for the same pull request.

##### 5. Compare the Field with the Edit

Compare the field with the intended edit.

##### 6. Return the Verified Link Relation

Return the verified relation or discrepancy.

#### *Fetch* Pull Request Issue Links

The complete issue-link snapshot for a supplied set of pull requests.

**Inputs:** Current pull request records, authenticated access and destination link-snapshot file.

##### 1. Read Links for Each Pull Request

For every pull request in `prs.json`, apply [Access Development Links](#access-development-links) with a read-only request and its identity. An observed empty field supplies an empty array; an unreadable field leaves the fetch incomplete.

##### 2. Re-Read Links After a Change

Repeat that read after a link changes.

##### 3. Return an Incomplete Link Fetch

If any relation is unreadable, return the incomplete result.

##### 4. Write the Links Snapshot

Run [Write Pull Request Links](#write-pull-request-links) with the observed complete relations and destination `links.json`, including one entry per pull request and every linked issue's repository and number.

##### 5. Return the Links Snapshot

Return the snapshot for the scripts' `--links` input.

#### *Fetch* All Initiative Pull Requests

The pull request collection covering every supplied board repository.

**Inputs:** Ordered repository list and destination JSON-lines file.

##### 1. Fetch the First Repository Pull Requests

Run [Fetch Repository Initiative Pull Requests](#fetch-repository-initiative-pull-requests) for the first repository and destination `prs.json`. This replaces the destination with a fresh collection.

##### 2. Stop on a First Fetch Failure

Stop on failure.

##### 3. Append Further Repository Pull Requests

Run [Append Repository Initiative Pull Requests](#append-repository-initiative-pull-requests) for each further repository, passing the same destination.

##### 4. Return Incomplete Pull Request Evidence

If any fetch failed, return incomplete evidence.

##### 5. Return the Complete Pull Request Collection

Return the complete collection only after every fetch succeeds.

### Fields

#### Issue Links

- GitHub shows the link in the pull request's Development field and in the issue's Linked pull requests field, which the project board reads.
- A task pull request links the task's issue, and a review pull request links its epic's issue.
- The link is addressed by issue, so a pull request whose work carries no issue links nothing. A task pull request delivering rows that have no issue of their own is the whole of what stays unlinked.
- The link is stored on the pull request. It holds on any base branch and on a pull request that has merged, and a later body edit leaves it standing.
- A linked issue remains open until its criteria and delivery requirements hold and every Development-linked pull request is merged.
- The field is the whole of the relation: neither body links the other. The pull request's References carry its sources, and the issue it delivers is not among them.
- A pull request with a delivery issue but no Development link is uncited.

### Commands

#### Read Development Links

Returns the complete Development relation through authenticated GitHub or an available supported tool.

**Inputs:** Pull request identity and authenticated access.

Read the actual field across every page and state, recording repository and number for each linked issue. Return the links and whether the field was fully readable.

#### Set Development Link

Adds one pull request to an issue's Development relation.

**Inputs:** Pull request identity, issue identity, authenticated access and confirmed repository prerequisite.

Use [GitHub's sidebar linking procedure](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue): in the issue's Development selector, select the pull request's repository and pull request, including a different repository when required. Return the edit result.

#### Remove Development Link

Removes one selected Development relation.

**Inputs:** Pull request and issue identities, authenticated access and the user's decision authorizing removal of the abandoned or incorrect link.

Deselect the supplied relation in the authenticated Development selector and save the edit. Return the edit result.

#### Write Pull Request Links

Saves complete observed Development-linked issues as a JSON array.

**Inputs:** One complete relation per pull request, with all repository and number pairs, and destination link-snapshot file.

Write the supplied relations in this shape. Substitute numbers as JSON integers. Include each pull request and all its linked issues; use an empty array for a complete relation with no linked issues. Each repository is the one belonging to that pull request or issue.

```text
[
  {
    "repo": "<pull-request-owner>/<pull-request-repo>",
    "number": <pull-request-number>,
    "closingIssuesReferences": [{"repo": "<issue-owner>/<issue-repo>", "number": <issue-number>}]
  }
]
```

**Example payload:**

```json
[
  {
    "repo": "owner/repo",
    "number": 950,
    "closingIssuesReferences": [{"repo": "owner/repo", "number": 637}]
  }
]
```

#### Fetch Repository Initiative Pull Requests

Starts a collection with all initiative-prefixed pull requests from one repository.

**Inputs:** Repository and destination JSON-lines file.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' > prs.json
```

#### Append Repository Initiative Pull Requests

Appends all initiative-prefixed pull requests from one further repository.

**Inputs:** Repository and existing destination JSON-lines file.

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> '<pull-request-records-file>'
```

**Example:**

```bash
gh api --paginate "repos/<owner>/<repo>/pulls?state=all&per_page=100" --jq '.[] | select(.title | startswith("[I"))' >> prs.json
```

## Epic Issue Body

### Fields

#### Task Delivery

- **Holds.**
  - A unit's record exists and its rows link it before its session starts.
  - A row another session holds is not dispatched.
  - A held row stays held while its session plans and implements. The pull request's link replaces the record's link, which frees the row.
- **Task ids.**
  - An unreserved task awaiting its pull request links its file in the planning record: `[W01](…/w01.md)`. The file name is the task id in lower case.
  - Every link on a task row names that row's id, and the row carries one delivery per long-lived branch its unit changes. A reserved task links only its planning folder: `[W01](…/2026-10-06-943-i07-e00-w01-queue-plan/)`. The folder's README links the work-item file. Releasing the reservation points the row to that file.
  - Once a pull request is open, its link replaces the planning link: `[W01](…/pull/950)`. A unit changing two long-lived branches links the pull request on each: `[W01](…/pull/950), [W01](…/pull/951)`. Further delivery work on one of those branches gets another task row under Task grain. Joined rows each link their shared pull request.
  - The task is delivered when a linked pull request has merged, or its id links a commit.
  - A link to an open pull request does not deliver the task.
  - A linked pull request whose title names another epic delivers the task once it has merged. The mismatch is reported, and the row stays open while a criterion its Coverage names is unticked.
- **Tasks with their own issue.**
  - A task issue belongs to one epic. Its title carries that epic's prefix.
  - When that epic's table has no row for its id, the issue is unplaced. Once the row exists, that epic's planning manages the issue.
  - The row links the pull request, not the issue.
  - The pull request's Development field links the issue as [Issue Links](#issue-links) state.
  - A completed task issue has all criteria verified and every Development-linked pull request merged.
- **Issues backing several tasks.**
  An issue backing several tasks, such as an investigation, is a reference: the epic cites it under References, no row id links it, and its title carries no agent-engineering prefix.
- **Work another issue takes.**
  It leaves the table. Its criteria go with it, or to another row that delivers them.

## Repository Labels

### Operations

#### *Ensure* Repository Labels

The required label definitions available for issue publication.

**Inputs:** Repository and required label names, colours and descriptions.

##### 1. List the Repository Labels

Run [List Labels](#list-labels) for the repository.

##### 2. Compare Required Label Names

Compare the returned labels with the supplied required names.

##### 3. Create Absent Required Labels

Run [Create Label](#create-label) for each absent required definition.

##### 4. Return the Available Labels

Return the available labels; an unknown definition is a finding for the caller to resolve before publication.

### Commands

#### List Labels

Lists the labels that exist in the repository.

**Inputs:** Repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

#### Create Label

Creates the label specified by its name, colour and description.

**Inputs:** Repository, label name, colour and description.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```
