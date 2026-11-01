# Joins

Each pair below has no dependency either way and is not joined. Its tasks ship as separate pull requests because they extend different components, named after the pair.

- E01:W01 E01:W02 — separate components: .github/workflows/checks.yml; checks/links.py
- E01:W02 E01:W03 — separate components: checks/links.py; .github/workflows/checks.yml
- E01:W02 E01:W04 — separate components: checks/links.py; checks.md
