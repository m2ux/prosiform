**Component:** main:src/prosiform/__init__.py, main:src/prosiform/source.py, main:src/prosiform/profile.py, main:src/prosiform/marks.py, main:src/prosiform/tags.py, main:src/prosiform/heading.py, main:src/prosiform/limits.py

## Overview

Each module states its own responsibility and names the owner of every rule it relies on.

## Problem

Docstrings and comments restate rules implemented by other units, so one rule has several descriptions that can drift.

## Proposal

Review every docstring and comment in the declared modules against the repository's AGENTS.md. Keep each rule with its narrowest implementing unit, use owner references elsewhere, and retain comments explaining reasons the code cannot express. The diagram-link contract belongs to source.Click. Code, signatures, values and imports remain byte-for-byte equivalent after docstrings and comments are excluded.

## Work Breakdown

| Part | Description |
| --- | --- |
| Analysis | Read every declared module and identify each rule's implementing owner. |
| Plan | Resolve duplicated descriptions to their owning unit. |
| Implementation | Revise docstrings and comments in the declared files. |
| Review | Read all revised prose and verify referenced owners exist. |
| Test | Review all modules for AC1 and diagram references for AC2; compare normalized syntax and all corpus results with the base, then run make check for AC3. |
