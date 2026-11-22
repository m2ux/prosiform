import sys
from pathlib import Path

root = Path(sys.argv.pop(1))
sys.path.insert(0, str(root / 'src'))
from prosiform.cli import main

raise SystemExit(main())
