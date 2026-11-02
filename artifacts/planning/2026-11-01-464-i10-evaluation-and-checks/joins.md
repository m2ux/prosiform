# Joins

Each pair below has no dependency either way and is not joined. Its tasks ship as separate pull requests because they extend different components, named after the pair.

- E01:W01 E01:W02 — separate components: .github/workflows/checks.yml; checks/links.py
- E01:W02 E01:W03 — separate components: checks/links.py; .github/workflows/checks.yml
- E01:W02 E01:W04 — separate components: checks/links.py; checks.md

The pairs below extend one component and stay split, each with a dependency between its rows.

- E01:W01 E01:W03 — the skipped-run report reads the path set the trigger states, so it lands once the trigger has.
- E02:W01 E02:W02 — the managed-settings read extends the preflight the project-scope row widens, on its own row by the user's decision.
