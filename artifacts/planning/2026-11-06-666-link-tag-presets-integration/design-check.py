import hashlib,json,re,subprocess,sys
from pathlib import Path
project=Path('/home/mike1/projects/dev/md-composer/.worktrees/i10/e07/main')
design=Path('/home/mike1/projects/dev/md-composer/.worktrees/pr/664/artifacts/planning/2026-10-17-prosiform-v1/design.md')
sys.path.insert(0,str(project/'checks'))
import conformance,links,vocabulary
text=design.read_text()
pinned=subprocess.check_output(['git','show','795bbfb67c66b02193f0313138f59f18aa6c5274:artifacts/planning/2026-10-17-prosiform-v1/design.md'],text=True,cwd=project)
assert text==pinned,'design differs from product pin'
codes=subprocess.check_output([str(project/'src/.venv/bin/pf'),'-C'],text=True).splitlines()
report=conformance.report(text,project/'fixtures',codes)
assert not report.failures,report.failures
unresolved,unreached=links.check(design,False)
internal=[one for one in unresolved if not one.startswith(('http://','https://'))]
assert not internal,internal
assert not unreached,unreached
defined,_=vocabulary.glossary_terms((project/'docs/glossary.md').read_text())
terms=vocabulary.marked_terms(text)
undefined=[term for term in terms if not vocabulary.holds(term,defined)]
assert not undefined,undefined
stale=[p for p in [r'Selection by keyword',r'selects its presets by its own heading',r'scope title selects',r'where no keyword matches',r'pf \[OPTIONS\] REF',r'Join the selections',r'Combined selection',r'Resolve positional file'] if re.search(p,text)]
assert not stale,stale
encoded=json.dumps(['checks','draft'],ensure_ascii=False,separators=(',',':')).encode()
assert hashlib.sha256(encoded).hexdigest() in text
assert len(re.findall(r'^```',text,re.M))%2==0
print('Design head: 4e076e6082d86aa74374bee6359f411ecaf89714')
print('Target at review: 905b3a86ca2544c7a795410949c22ddf1109e38a')
print('Exact byte identity with product contract pin795bbfb67c66b02193f0313138f59f18aa6c5274: PASS')
print('Internal links: PASS; existing external links not fetched:',len(unresolved))
print('Vocabulary: PASS;',len(terms),'marked terms; stale operative patterns: 0')
print('Digest and balanced fences: PASS')
print('Conformance: PASS;',len(report.mapping),'clauses;',len(report.uncovered),'uncovered; no nonexistent declarations or code mismatches')
