"""Run the four retained example commands against two supplied checkouts."""

import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("baseline", type=Path)
parser.add_argument("candidate", type=Path)
args = parser.parse_args()
record = Path(__file__).resolve().parent
text = (record / "measurement-inputs/baseline-invocation.md").read_text()
examples = text.split("## Examples\n", 1)[1].split("## Bundling rules", 1)[0]
commands = re.findall(r"```bash\n(.*?)```", examples, re.S)
results = []
for number, command in enumerate(commands, 1):
    baseline = shlex.split(command.replace("\\\n", ""))
    candidate = [dict(prosiform="pf", **{"--root": "-r", "--group": "-g", "--check": "-c"}).get(value, value) for value in baseline]
    runs = []
    for checkout, words in ((args.baseline, baseline), (args.candidate, candidate)):
        runs.append(subprocess.run([str(checkout.resolve() / "src/.venv/bin" / words[0]), *words[1:]], cwd=checkout, capture_output=True, check=False))
    before, after = runs
    assert before.returncode == after.returncode == 0, number
    assert before.stdout == after.stdout, number
    assert before.stderr == after.stderr, number
    results.append({"example": number, "status": after.returncode, "stdout_bytes": len(after.stdout), "stderr_bytes": len(after.stderr), "identical": True})
print(json.dumps(results, indent=2))
