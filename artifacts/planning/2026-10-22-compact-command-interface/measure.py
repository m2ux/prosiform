# /// script
# requires-python = ">=3.13"
# dependencies = ["tiktoken==0.12.0"]
# ///
"""Count the retained UTF-8 inputs with one pinned tokenizer."""

import hashlib
import importlib.metadata
import json
import re
from pathlib import Path

import tiktoken

ROOT = Path(__file__).resolve().parent
ENCODING = "o200k_base"
VERSION = "0.12.0"


def main():
    assert importlib.metadata.version("tiktoken") == VERSION
    encoding = tiktoken.get_encoding(ENCODING)
    inputs = {}
    for path in sorted((ROOT / "measurement-inputs").iterdir()):
        data = path.read_bytes()
        inputs[path.name] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "tokens": len(encoding.encode(data.decode("utf-8"))),
        }
    comparisons = {}
    for kind in ("invocation.md", "commands.txt", "help.txt"):
        before = inputs[f"baseline-{kind}"]["tokens"]
        after = inputs[f"candidate-{kind}"]["tokens"]
        comparisons[kind] = {
            "baseline": before,
            "candidate": after,
            "saved": before - after,
            "percent_saved": round(100 * (before - after) / before, 2),
        }
    original = (ROOT / "measurement-inputs/baseline-invocation.md").read_text()
    examples = original.split("## Examples\n", 1)[1].split("## Bundling rules", 1)[0]
    baseline = re.findall(r"```bash\n(.*?)```", examples, re.S)
    candidate = [command.replace("prosiform", "pf").replace("--root", "-r").replace("--group", "-g").replace("--check", "-c") for command in baseline]
    commands = {}
    for side, samples in (("baseline", baseline), ("candidate", candidate)):
        assert "\n\n".join(samples) == (ROOT / "measurement-inputs" / f"{side}-commands.txt").read_text()
        commands[side] = [len(encoding.encode(command)) for command in samples]
    assert len(commands["baseline"]) == len(commands["candidate"]) == 4
    assert comparisons["invocation.md"]["saved"] > 0
    assert comparisons["commands.txt"]["saved"] > 0
    print(json.dumps({
        "tokenizer": "tiktoken",
        "version": VERSION,
        "encoding": ENCODING,
        "baseline_revision": "9e11aedb062d8afdaffe111e6af9af454a1b8a68",
        "inputs": inputs,
        "comparisons": comparisons,
        "per_command_tokens": commands,
        "command_token_sums": {side: sum(counts) for side, counts in commands.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
