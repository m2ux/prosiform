import ast
import io
import json
import re
import tokenize
from pathlib import Path

root = Path('/home/mike1/projects/dev/ghsa-classifier/.worktrees/prosiform-786/src/prosiform')
trees = {p.stem: ast.parse(p.read_text()) for p in sorted(root.glob('*.py'))}
symbols = {}
def collect(node, prefix, names):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            name = prefix + child.name
            names.add(name)
            collect(child, name + '.', names)
        elif isinstance(child, (ast.Assign, ast.AnnAssign)):
            for target in child.targets if isinstance(child, ast.Assign) else [child.target]:
                if isinstance(target, ast.Name):
                    names.add(prefix + target.id)
for module, tree in trees.items():
    symbols[module] = set()
    collect(tree, '', symbols[module])
rows = []
missing = []
for module, tree in trees.items():
    strings = [n for n in ast.walk(tree) if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)]
    comments = [t for t in tokenize.generate_tokens(io.StringIO((root / (module+'.py')).read_text()).readline) if t.type == tokenize.COMMENT]
    refs = set()
    for node in strings:
        for owner, name in re.findall(r'\b([a-z_]+)\.([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)', node.value.value):
            if owner not in trees:
                continue
            refs.add(owner + '.' + name)
            if name not in symbols[owner]:
                missing.append({'file': module+'.py', 'line': node.lineno, 'reference':owner+'.'+name})
    rows.append({'module':module+'.py', 'docstrings_and_attribute_docs':len(strings), 'comments':len(comments), 'references':sorted(refs)})
report = {'modules':rows,'unresolved_references':missing}
Path('/tmp/prosiform-786-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'modules':len(rows),'docstrings_and_attribute_docs':sum(r['docstrings_and_attribute_docs'] for r in rows),'comments':sum(r['comments'] for r in rows),'unresolved_references':missing},indent=2))
