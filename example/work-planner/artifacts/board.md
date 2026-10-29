---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Board

The theme or proposals board, its membership and each item's status.

## Operations

### Select Project Board

The theme or proposals board the request names.

**Inputs:** [Board owner](#board-identity), [Board selection](#board-selection)

**Outputs:** [Selected board](#board-identity)

#### 1. Find the Named Board

Select the command matching the requested board kind. The selection meets [Themes](#themes) or [Proposals](#proposals).

For a theme selection, run this query from the repository checkout using the board owner and requested theme name.

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("<theme-name>: ")) | .number'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title | sub("^\\[P[0-9]+\\] "; "") | startswith("Canon: ")) | .number'
```

For a proposals selection, run this query from the repository checkout using the board owner and configured [proposals title](../configuration.md#proposals-board).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<proposals-board-title>") | .number'
```

#### 2. Report a Missing Board Selection

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return a missing-selection result when neither a theme nor proposals is specified; the caller obtains that choice.

#### 3. Return the Selected Board Number

Return the selected board number, or an absent-board result for [Copy Project Board](#copy-project-board). Work one board at a time.

### Copy Project Board

A missing theme board, or a missing proposals board.

**Inputs:** [Board owner](#board-identity), [Repository](repository-labels.md#repository), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](issue.md#issue-record)

**Outputs:** [Copied board](#board-identity)

#### 1. Create an Absent Proposals Board

When no open board carries the [proposals board](../configuration.md#proposals-board) title, apply [Create Proposals Board](#create-proposals-board). The copy source and the title meet [Proposals](#proposals).

#### 2. Create an Absent Theme Board

When the selected theme board is absent:
- Apply [Create Theme Board](#create-theme-board) with the owner, repository, theme title and originating proposal record when applicable.
- Require the new theme's label and board before an initiative takes that theme.

### Ensure Project Board

The theme or proposals board the request names, created when it is absent.

**Inputs:** [Board owner](#board-identity), [Repository](repository-labels.md#repository), [Board selection](#board-selection), [Theme title](#one-board-per-theme), [Originating proposal](issue.md#issue-record)

**Outputs:** [Board](#board-identity)

#### 1. Select the Requested Board

Apply [Select Project Board](#select-project-board) with the owner and the theme name or proposals selection.
- On a missing-selection result, return it to the caller and stop.
- On a selected board, return its owner and number and stop.

#### 2. Copy an Absent Requested Board

When the board is absent:
- For a theme a proposal derives, apply [Read Tracker Issue](issue.md#read-tracker-issue) for the originating proposal's identity. Return unresolved provenance and stop when it cannot be read.
- Apply [Copy Project Board](#copy-project-board) with the owner, repository, selected board kind, theme title and that proposal record when applicable.

#### 3. Return the Copied Board Number

Return the owner and the board number the copy created.

### Create Proposals Board

A new proposals board linked to the supplied repository.

**Inputs:** [Board owner](#board-identity), [Repository](repository-labels.md#repository)

**Outputs:** [Proposals board](#board-identity)

#### 1. Copy the Proposals Template

Apply [Copy Board Template](#copy-board-template) with the owner, repository, the proposals board's [template title](../configuration.md#board-templates) and the configured [proposals title](../configuration.md#proposals-board) as the copy's title. The copied board meets [Proposals](#proposals).

#### 2. Return the Proposals Board Number

Return the copied board's owner and number.

### Create Theme Board

A new theme board linked to the supplied repository.

**Inputs:** [Board owner](#board-identity), [Repository](repository-labels.md#repository), [Theme title](#one-board-per-theme), [Originating proposal](issue.md#issue-record)

**Outputs:** [Theme board](#board-identity)

#### 1. Require the Originating Proposal

Require the originating proposal record for a proposal-derived board; return a missing-input finding when its designator is unavailable.

#### 2. Copy the Initiative Template

Apply [Copy Board Template](#copy-board-template) with the owner, repository, the theme board's [template title](../configuration.md#board-templates) and the title required by [One Board Per Theme](#one-board-per-theme) as the copy's title. The copy carries the template's theme board [Status options](../configuration.md#status-field).

#### 3. Return the Theme Board Number

Return the copied board's owner and number.

### Copy Board Template

One board copied from an open template board and linked to its repository.

**Inputs:** [Board owner](#board-identity), [Repository](repository-labels.md#repository), [Board title](#one-board-per-theme)

**Outputs:** [Copied board](#board-identity)

#### 1. Find the Template Board

From the repository checkout, find the open template board using the owner and the supplied [template title](../configuration.md#board-templates).

```bash
gh api --paginate "users/<owner>/projectsV2?per_page=100" --jq '.[] | select(.closed | not) | select(.title == "<template-title>") | .number'
```

#### 2. Copy the Template Board

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, copy the returned template number for the owner, using the supplied board title.

- The copy's JSON is one project; `.number` identifies the new board.

```bash
gh project copy '<template-number>' --source-owner '<owner>' --target-owner '<owner>' --title '<board-title>' --format json --jq .number
```

#### 3. Link the Board to the Repository

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, link the new board using its owner, returned number and supplied repository.

```bash
gh project link '<board-number>' --owner '<owner>' --repo '<repo>'
```

#### 4. Return the Copied Board Number

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return the new board number after linking succeeds.

### Place Issue on Board

One issue's membership and initial status.

**Inputs:** [Board](#board-identity), [Repository](repository-labels.md#repository), [Issue](issue.md#issue-record), [Output file](#board-files), [Initial status](../configuration.md#status-field)

**Outputs:** [Board item](#board-items)

#### 1. Read the Issue to Place

Apply [Read Tracker Issue](issue.md#read-tracker-issue) with the repository, issue number and output file for the complete JSON, and take the issue id from it.

#### 2. Fetch the Placement Status Options

From the repository checkout, fetch the supplied board’s fields into the destination file, using its owner and number.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

#### 3. Add the Issue to the Board

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, add the issue using the board owner and number and the returned issue id, not its issue number.

```bash
gh api --method POST 'users/<owner>/projectsV2/<board-number>/items' -f type=Issue -F 'id=<issue-id>' --jq .id
```

**Example:**

```bash
gh api --method POST 'users/<owner>/projectsV2/13/items' -f type=Issue -F id=3040123456 --jq .id
```

#### 4. Set the Placed Item Status

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, set the caller’s selected Status using the board owner and number, returned item id and supplied status-request file.

The input file meets [Status Request](#status-request), with the supplied Status field id as a JSON integer and the selected option id as a JSON string.

**Example payload:** `{"fields":[{"id":419167630,"value":"OPTION"}]}`.

```bash
gh api --method PATCH 'users/<owner>/projectsV2/<board-number>/items/<item-id>' --input '<status-input-file>' --jq .id
```

**Example:**

```bash
gh api --method PATCH 'users/<owner>/projectsV2/13/items/1001' --input status-backlog.json --jq .id
```

#### 5. Confirm the Placed Board Item

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, read the saved item using the board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

#### 6. Return the Placed Board Item

Read the final fetch’s result as [Command result](../conventions.md#command-result) states. Return the confirmed item only when its issue and Status match the intended placement; otherwise return the failure or discrepancy.

### Read Board State

The selected board's items and status fields.

**Inputs:** [Board](#board-identity)

**Outputs:** [Board items](#board-items), [Status field id](#status-field-id), [Repositories](#repositories)

#### 1. Find the Board Status Field

Use the existing board returned by [Select Project Board](#select-project-board) or [Copy Project Board](#copy-project-board), whether the caller ran that operation or carries its result. From the repository checkout, query its owner and number for the configured [Status field](../configuration.md#status-field) name.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" --jq '.[] | select(.name == "<status-field-name>") | .id'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" --jq '.[] | select(.name == "Status") | .id'
```

#### 2. Fetch Board Items with Status

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

From the repository checkout, save the board items using the board owner and number, returned Status field id and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/items?per_page=100&fields=<status-field-id>" > '<board-items-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/items?per_page=100&fields=419167630" > items.json
```

#### 3. Return the Board State

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return the items, Status field, item ids and the board's [Repositories](#repositories) to the caller.

### Read Board Assignee

The authenticated login available for board assignments.

**Inputs:** None

**Outputs:** [Assignee login](#assignees)

#### 1. Find the Board User

From the repository checkout, read the authenticated login.

```bash
gh api user --jq .login
```

#### 2. Return the Assignee Login

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return its login for the caller's assignment decisions.

### Read Board Configuration

One board's field definitions and requested item state.

**Inputs:** [Board](#board-identity), [Output paths](#board-files), [Board item](#board-items)

**Outputs:** [Board fields](#board-fields), [Board item](#board-items)

#### 1. Fetch the Configured Board Fields

From the repository checkout, save the supplied board’s fields using its owner, number and destination file.

```bash
gh api --paginate "users/<owner>/projectsV2/<board-number>/fields?per_page=100" > '<board-fields-file>'
```

**Example:**

```bash
gh api --paginate "users/<owner>/projectsV2/9/fields?per_page=100" > fields.json
```

#### 2. Fetch the Requested Board Item

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

When a single item is requested for [write confirmation](../conventions.md#write-confirmation), read it from the repository checkout using the board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

#### 3. Return the Board Configuration

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return the field definitions and requested current item.

### Update Item Status

One board item with a confirmed status selection applied.

**Inputs:** [Board](#board-identity), [Board item](#board-items), [Status field](#board-fields), [Selected status](../configuration.md#status-field), [Status request](#status-request)

**Outputs:** [Board item](#board-items)

#### 1. Set the Requested Item Status

Require the caller’s confirmed status selection. From the repository checkout, set it using the supplied board owner and number, item id and status-request file.

The input file meets [Status Request](#status-request), with the supplied Status field id as a JSON integer and the selected option id as a JSON string.

**Example payload:** `{"fields":[{"id":419167630,"value":"OPTION"}]}`.

```bash
gh api --method PATCH 'users/<owner>/projectsV2/<board-number>/items/<item-id>' --input '<status-input-file>' --jq .id
```

**Example:**

```bash
gh api --method PATCH 'users/<owner>/projectsV2/13/items/1001' --input status-backlog.json --jq .id
```

#### 2. Re-Read the Updated Board Item

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Read the item as [Write confirmation](../conventions.md#write-confirmation) states.

From the repository checkout, read the item using the supplied board owner and number, item id and Status field id.

```bash
gh api "users/<owner>/projectsV2/<board-number>/items/<item-id>?fields=<status-field-id>"
```

**Example:**

```bash
gh api "users/<owner>/projectsV2/9/items/1001?fields=419167630"
```

#### 3. Return the Confirmed Item Status

Read the result of each command in the preceding step as [Command result](../conventions.md#command-result) states.

Return its confirmed state or a discrepancy for the caller to resolve.

## Fields

### Themes

Every initiative belongs to one theme, and each theme has one project board. Each project names its own themes, with their labels, in [Theme Labels](../configuration.md#theme-labels).

### One Theme

An initiative carries one [theme label](../configuration.md#theme-labels), and each of its epics carries the same one.

### One Board Per Theme

- A proposal-derived board title is the originating proposal's exact `[Pxx]` designator, a space, the theme name, a colon, and its description: `[P03] Canon: Definitions Checked Against the Design Canon`. Preserve the proposal's digits exactly. A board with no originating proposal uses `Name: Description`.
- It is linked to the repository.
- It holds the theme's initiatives, their epics and their task issues.

### Repositories

A board's repositories are those its items' issues live in, read from each item's issue, deduplicated and ordered with the board's own repository first. An item whose issue is unreadable leaves the list incomplete, which is reported rather than filled by assumption.

### Assignees

The user is the login `gh` runs as. An issue at Ready, In Progress, In Review or Done is assigned to the user; one in Backlog has no assignee. An assignee is set on the issue, not on the board item, so the call that changes one acts on the issue.

### Standalone Issues

A standalone issue sits on no board.

### Proposals

- The board carries the [proposals board](../configuration.md#proposals-board) title. It holds proposal issues, the incoming funnel for work that may become an initiative.
- Its copy source is the open board with the proposals board's [template title](../configuration.md#board-templates). That template carries the [Proposals Priority Field](../configuration.md#proposals-priority-field), and its view is a board grouped by Status.
- Its [Status options](../configuration.md#status-field) mean:
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

### Board Identity

A board's owner and number, written `users/<owner>/projectsV2/<number>` for a user's board or `orgs/<owner>/projectsV2/<number>` for an organisation's. The owner is the user's login or organisation name; a board yet to be created has its owner alone.

### Board Selection

One theme's name, as [Theme Labels](../configuration.md#theme-labels) names it, or the proposals board.

### Board Fields

A board's field definitions as JSON: each field's id and name, and the [Status field](../configuration.md#status-field)'s id with its option ids.

### Status Field Id

The numeric identifier of the board's [Status field](../configuration.md#status-field).

### Board Items

A board's items as JSON, each with its item id, its Status and its issue whole. A single board item is one such entry.

### Board Files

The local paths a board read writes its JSON into: an issue file, a board fields file and a board item file.

### Status Request

A JSON file naming the Status field id as an integer and the selected option id as a string: `{"fields":[{"id":<status-field-id>,"value":"<status-option-id>"}]}`.
