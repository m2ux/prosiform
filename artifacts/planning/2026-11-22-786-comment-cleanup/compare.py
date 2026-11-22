import ast
import hashlib
import json
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path

base = Path('/home/mike1/projects/dev/ghsa-classifier/.worktrees/prosiform-786-base')
candidate = Path('/home/mike1/projects/dev/ghsa-classifier/.worktrees/prosiform-786')
sys.path.insert(0, str(base / 'checks'))
import manifests
import runner

class WithoutDocs(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return None
        return self.generic_visit(node)

syntax = []
for path in sorted((base / 'src/prosiform').glob('*.py')):
    relative = path.relative_to(base)
    old = WithoutDocs().visit(ast.parse(path.read_text()))
    new = WithoutDocs().visit(ast.parse((candidate / relative).read_text()))
    assert ast.dump(old) == ast.dump(new), str(relative)
    syntax.append(str(relative))
print(f'Executable syntax identical across {len(syntax)} modules', flush=True)

held = threading.local()
compare = runner.compare_bundles
def capture(fixture, declared, written):
    held.written = tuple((one.folder, one.name, one.data) for one in written)
    return compare(fixture, declared, written)
runner.compare_bundles = capture

# The source selector lives in each subprocess's argv; both builds read the
# same pristine fixture paths and their output is collected by the real runner.
def command():
    return [sys.executable, '/tmp/prosiform-786-invoke.py', str(held.root)]
runner.build_under_test = command

def one(fixture):
    held.root = base
    held.written = ()
    old = runner.run_fixture(fixture)
    old_files = held.written
    held.root = candidate
    held.written = ()
    new = runner.run_fixture(fixture)
    new_files = held.written
    assert old_files == new_files, f'Bundle bytes differ: {old.fixture}'
    assert old.exit_status == new.exit_status, f'Exit status differs: {old.fixture}'
    assert old.passed == new.passed, f'Fixture verdict differs: {old.fixture}'
    return {
        'fixture': old.fixture,
        'bundle_files': [{'folder': folder, 'name': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for folder, name, data in old_files],
        'exit_status': old.exit_status,
        'baseline_passed': old.passed,
        'candidate_passed': new.passed,
        'baseline_differences': [asdict(d) for d in old.differences],
        'candidate_differences': [asdict(d) for d in new.differences],
    }

fixtures = list(manifests.fixtures())
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(one, fixtures))
report = {
    'base': 'e2dde5e569800e5584797bb194bb989f8fb2843b',
    'candidate': subprocess.check_output(['git', '-C', str(candidate), 'rev-parse', 'HEAD'], text=True).strip(),
    'modules_with_identical_executable_syntax': syntax,
    'fixtures': len(results),
    'bundle_files': sum(len(r['bundle_files']) for r in results),
    'bundle_bytes': sum(f['bytes'] for r in results for f in r['bundle_files']),
    'all_bundle_bytes_identical': True,
    'results': results,
}
Path('/tmp/prosiform-786-comparison.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('results', 'modules_with_identical_executable_syntax')}, indent=2), flush=True)
print('Baseline failures:', sum(not r['baseline_passed'] for r in results), flush=True)
