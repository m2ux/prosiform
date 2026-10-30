import sys,tempfile,json
from pathlib import Path
sys.path.insert(0,str(Path('checks').resolve()))
import smoke
with tempfile.TemporaryDirectory(prefix='pf-w04-installed-') as directory:
    workspace=Path(directory); wheel=smoke.build(workspace); env=smoke.install(workspace,wheel)
    elsewhere=workspace/'elsewhere'; elsewhere.mkdir(); sources=workspace/'sources'; sources.mkdir()
    (sources/'a.md').write_text('---\nmetadata:\n  prosiform-group: declared\n  prosiform-group-depth: "2"\n---\n# A\n\n## Run\n\nContent.\n')
    args=['-r',str(sources),'-d','json']
    run=smoke.invoke(env,elsewhere,*args,'a.md'); assert run.returncode==0,run.stderr
    assert '# Declared\n' in run.stdout and 'Content.' in run.stdout
    for option in ['-g','-gdeclared:2','--group']:
        run=smoke.invoke(env,elsewhere,*args,option,'declared:2','a.md')
        assert run.returncode==2 and not run.stdout
        assert json.loads(run.stderr)['code']=='E_INVALID_USAGE'
    output=elsewhere/'out.md'; output.write_text('preserved\n')
    run=smoke.invoke(env,elsewhere,*args,'-c','-o',str(output),'a.md#run')
    assert run.returncode==0 and not run.stdout and output.read_text()=='preserved\n',run.stderr
    run=smoke.invoke(env,elsewhere,*args,'-o',str(output),'-f','a.md','#run')
    assert run.returncode==0 and not run.stdout and 'Content.' in output.read_text(),run.stderr
    run=smoke.invoke(env,elsewhere,*args,'-B','1','a.md')
    assert run.returncode==1 and json.loads(run.stderr)['code']=='E_RESOURCE_LIMIT'
    help_run=smoke.invoke(env,elsewhere,'-h'); assert help_run.returncode==0 and '-g ' not in help_run.stdout
    print('Installed wheel: metadata grouping, retired flags, help, roots, entries, referrer, JSON diagnostics, check, output and byte limit passed.')
