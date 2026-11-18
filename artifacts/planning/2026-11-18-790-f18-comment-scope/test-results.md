# Test Results

Results for F18 at `3e611a195` on `f17-convention-scope`, run on 2026-11-18 in a clean checkout of that head.

## T1 Stated Scope

A reading of `AGENTS.md`, section "Docstrings and comments": its first sentence states that the section holds for all code in the repository, and its first rule speaks of a rule the code implements. No other document restates the section. Held.

## T2 Document Checks

`make layout tables links vocabulary` exits 0: layout (4 trees present), tables (20 commands and 8 declarations), links (every reference in 428 documents resolved) and vocabulary (52 contract terms, each defined). Held.
