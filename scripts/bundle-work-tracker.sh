#!/usr/bin/env bash
# Bundle the work-tracker planning procedure into the current directory.
set -euo pipefail

caller="$(pwd)"
repo="$(cd "$(dirname "$0")/.." && pwd)"

cd "$repo"
exec pf -o "$caller/modes_plan-mode.bundle.md" example/work-tracker/modes/plan-mode.md
