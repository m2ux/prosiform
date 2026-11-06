import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

main=Path('/home/mike1/projects/dev/md-composer/.worktrees/i10/e07/main')
candidate=Path('/home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w00-the-design-states-explicit/artifacts/planning/2026-10-17-prosiform-v1/design.md')
sys.path.insert(0,str(main/'checks'))
import conformance
import links
import vocabulary

text=candidate.read_text()
ref,path=vocabulary.design_reference()
pinned=vocabulary.git_show(vocabulary.git_ref(ref),path)
codes=subprocess.run(['/home/mike1/projects/dev/md-composer/.worktrees/i10/e00/main/src/.venv/bin/pf','-C'],check=True,capture_output=True,text=True).stdout.splitlines()
report=conformance.report(text,main/'fixtures',codes)
Path('/tmp/i10-e07-w00-candidate-conformance.txt').write_text(conformance.render(report)+'\n'.join(report.failures)+'\n')
unresolved,unreached=links.check(candidate,False)
internal=[one for one in unresolved if not one.startswith(('https://','http://'))]
assert not internal,internal
assert not unreached,unreached
before=vocabulary.marked_terms(pinned);after=vocabulary.marked_terms(text)
defined,avoided=vocabulary.glossary_terms((main/'docs/glossary.md').read_text())
undefined=[term for term in after if not vocabulary.holds(term,defined)]
assert not undefined,undefined
stale=[pattern for pattern in [r'Selection by keyword',r'selects its presets by its own heading',r'scope title selects',r'where no keyword matches',r'pf \[OPTIONS\] REF',r'Join the selections',r'Combined selection',r'Resolve positional file'] if re.search(pattern,text)]
assert not stale,stale
serialization=json.dumps(sorted({'checks','draft'}),ensure_ascii=False,separators=(',',':'))
digest=hashlib.sha256(serialization.encode()).hexdigest()
assert digest=='13c9f40cda0225cb29b9fa2332a291e8950291238a73b75fed0cd1521986f6e8'
assert digest in text
assert len(re.findall(r'^```',text,re.M))%2==0
print('Internal-link failures:',len(internal))
print('Existing remote references not fetched:',len(unresolved))
print('Marked contract terms:',len(after),'undefined:',len(undefined))
print('Pinned terms absent from candidate:',sorted(set(before)-set(after)))
print('Candidate terms absent from pin:',sorted(set(after)-set(before)))
print('Stale operative selection/CLI claims:',len(stale))
print('Canonical preset digest:',serialization,digest)
print('Candidate clauses:',len(report.mapping),'uncovered:',len(report.uncovered),'old fixture clause declarations needing migration:',len(report.unnamed))
print('Candidate code mismatches:',len(report.unreported),len(report.surplus))
for failure in report.failures:print('Expected fixture migration:',failure)
