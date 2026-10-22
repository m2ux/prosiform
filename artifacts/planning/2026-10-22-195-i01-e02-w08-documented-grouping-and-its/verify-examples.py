"""Execute the documented examples and compare their text and diagram headings."""
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve()
build = os.environ['PROSIFORM_BUILD']
outputs = []
count = 0
for name in ['README.md', 'invocation.md', 'example/README.md']:
    for block in re.findall(r'```bash\n(.*?)```', (root / name).read_text(), re.S):
        block = block.replace('\\\n', ' ')
        for line in block.splitlines():
            if not line.startswith('prosiform '):
                continue
            args = shlex.split(line)[1:]
            cwd = root / 'example' if '--root' in args and args[args.index('--root') + 1] == 'my-skill' else root
            result = subprocess.run(shlex.split(build) + args, cwd=cwd, text=True, capture_output=True)
            assert result.returncode == 0, (line, result.stderr)
            out = result.stdout
            if '--output' in args:
                path = cwd / args[args.index('--output') + 1]
                out = path.read_text()
                path.unlink()
            outputs.append(out)
            count += 1
            print('PASS command:', line)

fixtures = 0
for path in sorted((root / 'fixtures/usage-example').glob('*/manifest.toml')):
    manifest = tomllib.loads(path.read_text())
    inv = manifest['invocation']
    result = subprocess.run(shlex.split(build) + ['--root', inv['root']] + inv['arguments'], cwd=path.parent, capture_output=True, text=True)
    assert result.returncode == manifest['expected']['exit_status']
    assert result.stdout == (path.parent / manifest['expected']['stdout']).read_text(), path
    outputs.append(result.stdout)
    fixtures += 1

sources = [p.read_text() for p in (root / 'example/work-tracker').rglob('*.md')]
excerpts = 0
for name in ['invocation.md', 'example/README.md']:
    for excerpt in re.findall(r'```markdown\n(.*?)```', (root / name).read_text(), re.S):
        assert any(excerpt.rstrip() in text for text in outputs + sources), (name, excerpt)
        excerpts += 1

ns = {'s': 'http://www.w3.org/2000/svg'}
expected = {'compilation.svg': ['Procedure', 'Rules/Agents', 'Rules/Common', 'Tips'], 'agent-rules.svg': ['Rules/Agents', 'Rules/Codex', 'Rules/Claude']}
retained = root.parents[1] / '.engineering/artifacts/planning/2026-10-21-readme-compilation-diagram'
for name, headings in expected.items():
    svg = root / 'docs/images' / name
    assert svg.read_bytes() == (retained / name).read_bytes()
    texts = [node.text for node in ET.parse(svg).findall('.//s:text', ns) if int(node.attrib.get('font-size', '0')) >= 32]
    assert texts == headings, (name, texts)
    for heading in headings:
        assert any('\n# ' + heading + '\n' in out for out in outputs), heading
    print('PASS diagram:', name, ', '.join(headings))
print(f'PASS: {count} documented commands, {fixtures} exact fixture outputs, {excerpts} exact excerpts, 2 diagram heading lists and retained SVG copies')
