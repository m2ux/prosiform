---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Repository Labels

The labels available for issue metadata in one repository.

## Operations

### Ensure Repository Labels

The required label definitions available for issue publication.

**Inputs:** [Repository](#repository), [Required labels](#label-identity)

**Outputs:** [Available labels](#label-identity)

#### 1. List the Repository Labels

Run [List Labels](#list-labels) for the repository.

#### 2. Compare Required Label Names

Compare the returned labels with the supplied required names.

#### 3. Create Absent Required Labels

Run [Create Label](#create-label) for each absent required definition.

#### 4. Return the Available Labels

Return the available labels; an unknown definition is a finding for the caller to resolve before publication.

## Fields

### Repository

One repository, written `<owner>/<repo>`.

### Label Identity

Each label has a name, colour and description. Issue assignments use labels that exist in the repository.

## Commands

### List Labels

Lists the labels that exist in the repository.

**Inputs:** Repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

### Create Label

Creates the label specified by its name, colour and description.

**Inputs:** Repository, label name, colour and description.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```
