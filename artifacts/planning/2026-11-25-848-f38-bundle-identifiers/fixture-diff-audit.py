from pathlib import Path
from itertools import combinations
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import quote
from ruamel.yaml import YAML

root = Path(sys.argv[1]).resolve()
base = '86fcbad07cf279db2b2886265b5404c038b4d37e'
def git(*args):
    return subprocess.check_output(['git', *args], cwd=root)
paths = git('ls-tree', '-rz', '--name-only', base, 'fixtures', 'example', 'docs/images/lifecycle-waterfall.svg').decode().rstrip('\0').split('\0')
blobs = {}
mapping = {}
for name in paths:
    raw = git('show', base + ':' + name)
    try:
        text = raw.decode()
    except UnicodeDecodeError:
        continue
    blobs[name] = text
    front = re.match(r'\A---\r?\n(.*?)\r?\n---', text, re.S)
    if not front:
        continue
    try:
        data = YAML(typ='safe').load(front[1])
    except Exception:
        continue
    presets = data.get('prosiform') if isinstance(data, dict) else None
    if not isinstance(presets, dict):
        continue
    names = sorted(n for n in presets if isinstance(n, str) and n.casefold() != 'default')
    assert len(names) <= 16
    for count in range(1, len(names) + 1):
        for selected in combinations(names, count):
            digest = hashlib.sha256(json.dumps(selected, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()
            mapping[digest] = '-' + '+'.join(quote(n, safe='') for n in selected)
pattern = re.compile(r'--p-([0-9a-f]{64})')
renamed = changed = 0
for name, text in blobs.items():
    expected_name = pattern.sub(lambda m: mapping[m[1]], name)
    expected_text = pattern.sub(lambda m: mapping[m[1]], text)
    if name.endswith('.md'):
        expected_text = re.sub(r'(?<=\]\()([^\s)]+)', lambda m: m[0].replace('+', '%2B'), expected_text)
    actual = root / expected_name
    if actual.is_symlink():
        continue
    assert actual.read_bytes().decode() == expected_text, expected_name
    renamed += expected_name != name
    changed += expected_text != text
added = git('diff', '-z', '--name-only', '--diff-filter=A', '--no-renames', base, 'HEAD', '--', 'fixtures', 'example', 'docs/images/lifecycle-waterfall.svg').decode().rstrip('\0').split('\0')
expected_paths = {pattern.sub(lambda m: mapping[m[1]], name) for name in paths}
assert set(added) <= expected_paths
print(json.dumps({'base': base, 'head': git('rev-parse', 'HEAD').decode().strip(), 'inspected_text_files': len(blobs), 'renamed_paths': renamed, 'rewritten_contents': changed, 'only_naming_changes': True}, indent=2))
