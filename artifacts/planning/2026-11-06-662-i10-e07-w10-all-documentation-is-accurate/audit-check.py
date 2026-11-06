"""Check the recorded documentation inventory against the exact checkout under test.

The human claim review lives in audit.md. This instrument observes inventory
completeness and explicit classifications; executable examples are a separate
pytest instrument, not a string-presence claim about semantic correctness.
"""
import subprocess
from collections import Counter
from pathlib import Path

record = Path(__file__).resolve().parent
root = Path.cwd()
paths = subprocess.check_output(
    ["git", "ls-files", "*.md", "*.txt", "*.rst"], text=True
).splitlines()
assert paths == (record / "inventory.txt").read_text().splitlines()
audit = (record / "audit.md").read_text()
counts = Counter()
for name in paths:
    if name.startswith("fixtures/") and name != "fixtures/README.md":
        category = "corpus specimens"
    elif name.startswith("evals/diagram-following/workflows/"):
        category = "executable workflow material"
    elif name in {
        "evals/diagram-following/report.md", "evals/diagram-following/mvp-proof.md"
    }:
        category = "historical live reports"
    else:
        category = "primary maintained guidance"
        assert name in audit or (
            name.startswith("evals/diagram-following/instruction")
            and "instruction*.md" in audit
        ), f"No primary review disposition: {name}"
    assert (root / name).is_file() or (root / name).is_symlink(), name
    counts[category] += 1
assert "## Contract-to-Documentation Coverage" in audit
assert "## Exclusions and Unverified Claims" in audit
for category, count in sorted(counts.items()):
    print(f"{category}: {count}")
print(f"Inventory matches exact checkout: {len(paths)} documented paths; no unclassified paths")
print("Semantic claim review is recorded in audit.md; this check does not automate prose truth")
