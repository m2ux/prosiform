import hashlib
import re
import sys
import subprocess
from pathlib import Path
base=Path('/home/mike1/projects/dev/md-composer/.worktrees/i01-e06-w01-baseline')
candidate=Path('/home/mike1/projects/dev/md-composer/.worktrees/i01-e06-w01/artifacts/planning/2026-10-17-prosiform-v1/design.md')
sys.path.insert(0,str(base/'checks'))
import vocabulary
import links
s=candidate.read_text()
print('candidate sha256:',hashlib.sha256(candidate.read_bytes()).hexdigest())
terms=vocabulary.marked_terms(s)
defined,avoided=vocabulary.glossary_terms((base/'docs/glossary.md').read_text())
missing=[t for t in terms if not vocabulary.holds(t,defined) or vocabulary.holds(t,avoided)]
assert not missing,missing
print('PASS vocabulary:',len(terms),'marked terms remain defined; semantic glossary migration remains compiler consumer work')
failures,unreached=links.check(candidate,False)
remote=[f for f in failures if 'remote, and --online was not given' in f]
failures=[f for f in failures if f not in remote]
assert not failures,failures
print('PASS local links:',len(links.references(s)),'references inventoried;',len(remote)+len(unreached),'existing external references not reached')
old=subprocess.check_output(['git','show','38ca14e:artifacts/planning/2026-10-17-prosiform-v1/design.md'],cwd=base,text=True)
codes=lambda t:set(re.findall(r'\b[EW]_[A-Z_]+\b',t))
added=codes(s)-codes(old)
retired=codes(old)-codes(s)
assert added=={'E_INVALID_FRONTMATTER','E_INVALID_CONVERSION_METADATA','E_GROUP_DEPTH_CONFLICT'},added
assert retired=={'E_INVALID_GROUP_RULE','W_EMPTY_GROUP_RULE'},retired
print('PASS diagnostic inventory: added',','.join(sorted(added)),'; retired',','.join(sorted(retired)))
for stale in ['without parsing or executing YAML','Discard metadata','merged directory','directory slug','E_INVALID_GROUP_RULE','W_EMPTY_GROUP_RULE','not opened, parsed or bundled','| `-g SLUG:DEPTH`']:
    assert stale not in s,stale
print('PASS stale contract wording audit')
for clause in ['### Conversion metadata','### Metadata failures','### Metadata conformance cases','**Source-language handoff:**']:
    assert clause in s,clause
print('PASS contract clause inventory; behavioral coverage is reviewed separately')
