"""A native-shaped app-server for bridge tests, with no model connection."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def emit(value: dict[str, Any]) -> None:
    print(json.dumps(value), flush=True)


for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    identifier = request["id"]
    method = request.get("method")
    if method == "initialize":
        emit({"id": identifier, "result": {}})
    elif method == "config/read":
        emit(
            {
                "id": identifier,
                "result": {
                    "config": {
                        "features": {
                            name: False
                            for name in (
                                "apps",
                                "plugins",
                                "remote_plugin",
                                "memories",
                                "hooks",
                                "shell_tool",
                            )
                        }
                        | {"skip_host_skill_discovery": True},
                        "project_doc_max_bytes": 0,
                    },
                    "layers": [
                        {
                            "name": {
                                "type": "packagedDefaults",
                                "file": "/synthetic/default",
                            },
                            "config": {"fixture": "configuration-content-sentinel"},
                            "version": "1",
                            "disabledReason": None,
                        }
                    ],
                },
            }
        )
    elif method == "thread/start":
        Path("thread-request.json").write_text(json.dumps(request["params"]))
        emit(
            {
                "id": identifier,
                "result": {
                    "thread": {"id": "root"},
                    "model": "gpt-6.1-sol",
                    "instructionSources": [],
                },
            }
        )
    elif method == "turn/start":
        Path("turn-request.json").write_text(json.dumps(request["params"]))
        emit({"id": identifier, "result": {"turn": {"id": "t"}}})
        emit(
            {
                "id": 100,
                "method": "item/tool/call",
                "params": {
                    "threadId": "root",
                    "turnId": "t",
                    "callId": "pf-1",
                    "tool": "pf",
                    "arguments": {
                        "args": json.loads(os.environ.get("STUB_CODEX_PF_ARGS", "[]")),
                        "cwd": os.environ.get("STUB_CODEX_PF_CWD"),
                        "stdout": os.environ.get("STUB_CODEX_PF_STDOUT", "guide.txt"),
                        "stderr": None,
                        "append": False,
                        "stderr_to_stdout": True,
                    },
                },
            }
        )
    elif method == "command/exec":
        Path("command-request.json").write_text(json.dumps(request["params"]))
        ran = subprocess.run(
            request["params"]["command"],
            cwd=request["params"]["cwd"],
            capture_output=True,
            text=True,
            check=False,
        )
        emit(
            {
                "id": identifier,
                "result": {
                    "exitCode": ran.returncode,
                    "stdout": ran.stdout,
                    "stderr": ran.stderr,
                },
            }
        )
    elif identifier == 100:
        emit(
            {
                "method": "thread/tokenUsage/updated",
                "params": {
                    "threadId": "root",
                    "turnId": "t",
                    "tokenUsage": {"total": {"totalTokens": 120}},
                },
            }
        )
        emit(
            {
                "method": "item/completed",
                "params": {
                    "threadId": "root",
                    "turnId": "t",
                    "item": {
                        "type": "agentMessage",
                        "phase": "final_answer",
                        "text": "Done.",
                    },
                },
            }
        )
        emit(
            {
                "method": "turn/completed",
                "params": {
                    "threadId": "root",
                    "turn": {"id": "t", "status": "completed", "error": None},
                },
            }
        )
