"""Compare the declared representative corpus with frozen main output bytes.

Run from the candidate checkout with its locked Python environment and explicit
PROSIFORM_BUILD. The baseline oracle comes from git, never from candidate output.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASELINE = "cd3d8e635b8db500ceb7230b26209bdd37f637da"
root = Path.cwd()
sys.path.insert(0, str(root / "checks"))
from manifests import read  # noqa: E402
from runner import run_fixture  # noqa: E402

selected = sorted((root / "fixtures/grouping").glob("*/manifest.toml"))
selected += [root / "fixtures" / name / "manifest.toml" for name in (
    "delivery/an-entry-destination-under-a-grouping-rule",
    "depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth",
    "usage-example/every-document-under-a-directory-merged",
)]
records = []
for manifest_path in selected:
    fixture = manifest_path.parent
    manifest = read(manifest_path)
    output = fixture / manifest["expected"]["stdout"]
    relative = output.relative_to(root).as_posix()
    frozen = subprocess.run(["git", "show", f"{BASELINE}:{relative}"], capture_output=True)
    if frozen.returncode:
        assert fixture.name == "conflicting-member-depths", frozen.stderr
        continue
    result = run_fixture(fixture)
    assert result.passed, result.report()
    assert result.stdout == frozen.stdout, relative
    assert output.read_bytes() == frozen.stdout, relative
    records.append({"fixture": fixture.relative_to(root / "fixtures").as_posix(),
                    "exit_status": result.exit_status, "bytes": len(result.stdout),
                    "sha256": hashlib.sha256(result.stdout).hexdigest(),
                    "result": "pass"})
print(json.dumps({"baseline": BASELINE, "candidate": subprocess.check_output(
    ["git", "rev-parse", "HEAD"], text=True).strip(), "comparisons": records}, indent=2))
