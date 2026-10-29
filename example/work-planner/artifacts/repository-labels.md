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

From the repository checkout, list its labels using the supplied owner and repository.

```bash
gh api "repos/<owner>/<repo>/labels?per_page=100" --jq '.[].name'
```

#### 2. Compare Required Label Names

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Compare the returned labels with the supplied required names.

#### 3. Create Absent Required Labels

From the repository checkout, create each absent required label using its supplied name, colour and description. Read each creation’s exit code and output before the next label; return a failure immediately.

```bash
gh api --method POST 'repos/<owner>/<repo>/labels' -f name='<label>' -f color='<hex-colour>' -f description='<description>' --jq .name
```

#### 4. Return the Available Labels

Read the exit code and output of each command executed in the preceding step; return an execution error or refusal before continuing.

Return the observed existing labels and successful creations. When every required label already exists, return that observed set. An unknown definition is a finding for the caller to resolve before publication.

## Fields

### Repository

One repository, written `<owner>/<repo>`.

### Label Identity

Each label has a name, colour and description. Issue assignments use labels that exist in the repository.
