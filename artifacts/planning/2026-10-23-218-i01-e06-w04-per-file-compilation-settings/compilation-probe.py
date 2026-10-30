import json
import subprocess
import tempfile
from pathlib import Path

workspace=Path('/home/mike1/projects/dev/md-composer')
candidate=workspace/'.worktrees/i01/e06/w04-per-file-compilation-settings/src'
baseline=workspace/'.worktrees/i01/e06/w03-captured-source-settings/src'

def settings(name,depth=2):
    return '---\nmetadata:\n  prosiform-group: '+json.dumps(name)+'\n  prosiform-group-depth: '+json.dumps(str(depth))+'\n---\n'

def invoke(project,root,*args):
    return subprocess.run(['uv','run','--project',str(project),'--frozen','pf','-r',str(root),'-d','json',*args],capture_output=True,text=True)

with tempfile.TemporaryDirectory(prefix='pf-w04-review-') as directory:
    root=Path(directory)
    old=root/'old'; new=root/'new'
    (old/'parts').mkdir(parents=True)
    (new/'x').mkdir(parents=True); (new/'y').mkdir()
    body_a='# A\n\nPreamble A.\n\n## Shared\n\nA text. [B](b.md)\n'
    body_b='# B\n\nPreamble B.\n\n## Shared\n\nB text.\n'
    (old/'parts/a.md').write_text(body_a)
    (old/'parts/b.md').write_text(body_b)
    (new/'x/a.md').write_text(settings('parts')+body_a.replace('(b.md)','(../y/b.md)'))
    (new/'y/b.md').write_text(settings('parts')+body_b)
    before=invoke(baseline,old,'-g','parts:2','parts/a.md')
    after=invoke(candidate,new,'x/a.md')
    assert before.returncode==after.returncode==0,(before.stderr,after.stderr)
    assert before.stdout==after.stdout,(before.stdout,after.stdout)
    for name in ['#','*','a\\b',' spaces ','two words','Parts','parts']:
        (new/'x/a.md').write_text(settings(name)+body_a.replace('(b.md)','(../y/b.md)'))
        (new/'y/b.md').write_text(settings(name)+body_b)
        result=invoke(candidate,new,'x/a.md')
        assert result.returncode==0,(name,result.stderr)
    (new/'x/a.md').write_text(settings('parts')+body_a.replace('(b.md)','(../y/b.md)'))
    (new/'y/b.md').write_text(settings('Parts',3)+body_b)
    result=invoke(candidate,new,'x/a.md')
    assert result.returncode==0,result.stderr
    assert result.stdout.splitlines().count('# Parts')==2,result.stdout
    (new/'plain.md').write_text('# Plain\n\nPlain content.\n')
    (new/'x/a.md').write_text(settings('plain')+'# A\n\n[Plain](../plain.md)\n')
    result=invoke(candidate,new,'x/a.md')
    assert result.returncode==0,result.stderr
    assert result.stdout.splitlines().count('# Plain')==2,result.stdout
    (new/'x/a.md').write_text(settings('same')+body_a.replace('(b.md)','(../y/b.md)'))
    (new/'y/b.md').write_text(settings('same',3)+body_b)
    results=[invoke(candidate,new,*entries) for entries in [('x/a.md','y/b.md'),('y/b.md','x/a.md')]]
    for result in results:
        assert result.returncode==1 and not result.stdout,(result.returncode,result.stderr)
        diagnostic=json.loads(result.stderr.splitlines()[0])
        assert diagnostic['code']=='E_GROUP_DEPTH_CONFLICT',diagnostic
        assert diagnostic['location']['file']=='x/a.md',diagnostic
        assert diagnostic['related'][0]['file']=='y/b.md',diagnostic
    assert results[0].stderr==results[1].stderr
    (new/'x/a.md').write_text(settings('same')+'# A\n\n[¬ Later](../y/b.md)\n')
    result=invoke(candidate,new,'x/a.md')
    assert result.returncode==0,result.stderr
    assert 'B text' not in result.stdout
    output=new/'out.md'; output.write_text('keep me')
    result=invoke(candidate,new,'-o',str(output),'x/a.md','y/b.md')
    assert result.returncode==1 and output.read_text()=='keep me',result.stderr
    result=invoke(candidate,new,'-g','same:2','x/a.md')
    assert result.returncode==2,result.stderr
print('W04 baseline equivalence, group names, deterministic conflicts, deferred selection and atomic output passed')
