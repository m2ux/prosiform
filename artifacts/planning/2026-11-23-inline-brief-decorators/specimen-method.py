from pathlib import Path
import json
import subprocess

root = Path('/tmp/wp77-brief-inline-specimen-02')
root.mkdir(exist_ok=False)
target = root / 'call.md'
target.write_text('---\nprosiform:\n  default:\n    brief: "#contract"\n---\n# Call\n\n## Contract\n\nCONTRACT_SENTINEL\n\n### Given\n\nINPUT_SENTINEL\n\n### Leaves\n\nOUTPUT_SENTINEL\n\n### Answers\n\nANSWER_SENTINEL\n\n## Implementation\n\nIMPLEMENTATION_SENTINEL\n')
rows = []
for name, label, link in [
    ('dispatch', '⇉ Call', 'call.md'),
    ('inline-section', '↳ Implementation', 'call.md#implementation'),
    ('inline-contract', '↳ Contract', 'call.md#contract'),
    ('inline-document', '↳ Call', 'call.md'),
    ('ordinary-document', 'Call', 'call.md'),
]:
    entry = root / (name + '.md')
    entry.write_text('---\nprosiform: {}\n---\n# Caller\n\n## Graph\n\n' + chr(96)*3 + 'mermaid\nflowchart TD\n    Entry(( )) --> Call(' + label + ')\n    click Call href "' + link + '"\n' + chr(96)*3 + '\n')
    result = subprocess.run(['pf', '-d', 'json', '-o', str(root / name), entry.name], cwd=root, capture_output=True, text=True)
    (root / (name + '.diagnostics.jsonl')).write_text(result.stderr)
    bundles = sorted((root / name).rglob('*.bundle.md'))
    parent = next((p for p in bundles if p.name.startswith(name + '.bundle')), None)
    body = parent.read_text() if parent else ''
    row = {'case': name, 'exit': result.returncode, 'bundle_count': len(bundles), 'parent_contract': 'CONTRACT_SENTINEL' in body, 'parent_implementation': 'IMPLEMENTATION_SENTINEL' in body, 'parent_headings': [line for line in body.splitlines() if line.startswith('#')], 'parent_bundle': str(parent) if parent else None}
    rows.append(row)
expected = [
    ('dispatch', 0, 2, True, False),
    ('inline-section', 0, 1, False, True),
    ('inline-contract', 0, 1, True, False),
    ('inline-document', 1, 0, False, False),
    ('ordinary-document', 0, 1, True, True),
]
for row, (name, code, count, contract, implementation) in zip(rows, expected):
    assert row['case'] == name
    assert row['exit'] == code, row
    assert (row['bundle_count'], row['parent_contract'], row['parent_implementation']) == (count, contract, implementation), row
report = {'compiler': subprocess.check_output(['pf', '--version'], text=True).strip(), 'passed': True, 'cases': rows}
(root / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
