"""Structural guard for the explicitly controlled qualification dialect."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'scripts'))
from audit_inventory import corpus_files, yaml_sources, canon_inventory

root, engine = map(Path, sys.argv[1:3])
sources = corpus_files(root)
parsed = yaml_sources(sources, engine)
errors = [error for item in parsed.values() for error in item['errors']]
for key, item in parsed.items():
    value = item['value']
    if not isinstance(value, dict) or not isinstance(value.get('id'), str):
        errors.append(key + ': a definition needs its string id')
    elif key.endswith('workflow.yaml'):
        if not isinstance(value.get('graph'), dict) or not value.get('initialActivity'):
            errors.append(key + ': graph and initial activity required')
    elif not isinstance(value.get('steps'), list):
        errors.append(key + ': ordered steps required')
criteria, _ = canon_inventory(sources)
if len(criteria) != 4:
    errors.append('The qualification dialect requires its four criteria')
print(json.dumps({'check': 'controlled qualification structural guard', 'root': str(root),
                  'sources': len(sources), 'criteria': len(criteria), 'errors': errors}, indent=2))
raise SystemExit(bool(errors))
