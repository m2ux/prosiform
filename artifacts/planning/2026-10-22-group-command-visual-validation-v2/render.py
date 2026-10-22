"""Render pinned compiler outputs alongside their source cases."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shlex
import subprocess
import textwrap
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
FONT = 'IBM Plex Mono'
BG, CARD, BORDER = '#0d1117', '#161b22', '#303b49'
TEXT, MUTED, LINK, AMBER = '#e6edf3', '#b1c6df', '#58a6ff', '#e3b341'

REVISION = '08a8c0317924e69d5377464ee6961bbc948be85b'


def txt(x, y, value, size=20, color=TEXT, weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'


def lines(body, width):
    """Render Markdown headings, paragraphs, lists and link labels without clipping."""
    rows=[]
    for raw in body.splitlines():
        if not raw:
            rows.append(('', 13, 18, 0, False, False)); continue
        heading=re.match(r'^(#{1,6}) (.*)', raw)
        level=len(heading[1]) if heading else 0
        value=heading[2] if heading else raw
        value=re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', value)
        value=re.sub(r'^- ', '• ', value)
        size=30 if level==1 else 26 if level==2 else 23 if level else 20
        available=max(20, int((width-50-level*14)/(size*0.62)))
        for i,part in enumerate(textwrap.wrap(value, available, break_long_words=False, break_on_hyphens=False) or ['']):
            rows.append((part, size+17, size, level, '[' in raw, i==0 and bool(level)))
    return rows


def card(x,y,width,title,body,output=False):
    rows=lines(body,width)
    height=72+sum(r[1] for r in rows)+20
    result=[f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{CARD}" stroke="{BORDER}" stroke-width="2"/>',txt(x+24,y+36,title,21,MUTED)]
    result.append(f'<path d="M{x} {y+54} H{x+width}" stroke="{BORDER}"/>')
    at=y+74
    for value,step,size,level,islink,label in rows:
        at+=step
        if value:
            if label: result.append(txt(x+12,at,'H'+str(level),11,MUTED))
            color=AMBER if '¬' in value else LINK if islink else TEXT
            result.append(txt(x+38+level*12,at,value,size,color,500 if level else 400))
    return '\n'.join(result),height


def svg(case):
    blocks=[]
    command='prosiform --root sources/'+case['id']+'/my-skill '+shlex.join(case['args'])
    header=[txt(32,48,case['id']+' · '+case['title'],29),txt(32,90,'ACTUAL COMPILER OUTPUT · main 08a8c0317924 · group command review',20,AMBER)]
    y=126
    for part in textwrap.wrap(command,132,break_long_words=False):
        header.append(txt(32,y,part,20,LINK));y+=30
    for part in textwrap.wrap(case['focus'],145,break_long_words=False):
        header.append(txt(32,y,part,18,MUTED));y+=27
    if case.get('notes'):
        for part in textwrap.wrap('Review note: '+case['notes'],145,break_long_words=False):
            header.append(txt(32,y,part,18,AMBER));y+=27
    top=y+25
    # Only files participating in this case appear; the complete tree is in README.md.
    nodes={}
    for path in sorted(case['inputs']):
        node=nodes
        for part in path.split('/'):
            node=node.setdefault(part,{})
    tree_rows=['my-skill/']
    def branch(node,prefix=''):
        for i,(name,children) in enumerate(node.items()):
            last=i==len(node)-1
            tree_rows.append(prefix+('└─ ' if last else '├─ ')+name+('/' if children else ''))
            branch(children,prefix+('   ' if last else '│  '))
    branch(nodes)
    tree='\n'.join(tree_rows)
    treeblock,treeheight=card(32,top,410,'Participating files',tree)
    blocks.append(treeblock)
    at=top
    for path in case['inputs']:
        block,h=card(466,at,690,path,(HERE/'sources'/case['id']/'my-skill'/path).read_text())
        blocks.append(block);at+=h+22
    expected = case['stdout'] or 'No bundle published.'
    if case['stderr']:
        expected += '\n\nDiagnostics (stderr):\n' + case['stderr']
    outblock,outh=card(1230,top,880,'Compiler output · exit '+str(case['actual_exit']),expected,True)
    blocks.append(outblock)
    middle=top+100
    blocks.append(f'<path d="M1172 {middle} H1190 V{middle-12} L1218 {middle+16} L1190 {middle+44} V{middle+32} H1172Z" fill="{LINK}"/>')
    height=max(at,top+outh,top+treeheight)+65
    footer='Full output shown. Exact Markdown, link destinations and diagnostics are in the adjacent stdout.md and stderr.txt files.'
    blocks.append(txt(32,height-25,footer,17,MUTED))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="2142" height="{height}" viewBox="0 0 2142 {height}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(case["title"])}</title><desc id="desc">{html.escape(case["focus"])} Observed output from the pinned compiler.</desc><rect width="2142" height="{height}" fill="{BG}"/><g font-family="{FONT}" xml:space="preserve">'+''.join(header+blocks)+'</g></svg>\n'
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compiler', type=Path, required=True)
    parser.add_argument('--checkout', type=Path, required=True)
    args = parser.parse_args()
    revision = subprocess.check_output(['git', '-C', str(args.checkout), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == REVISION, (revision, REVISION)
    assert not subprocess.check_output(['git', '-C', str(args.checkout), 'status', '--porcelain', '--untracked-files=no'], text=True).strip(), 'Compiler checkout must be clean'
    cases = json.loads((HERE/'cases.json').read_text())
    assert len(cases) == 36
    output = HERE/'cases'
    output.mkdir(exist_ok=True)
    records = []
    fence = chr(96)*3
    review = ['# Group command visual review', '', '**36 diagrams of actual compiler output.**', '',
              'Source revision: ['+REVISION[:12]+'](https://github.com/m2ux/prosiform/commit/'+REVISION+').', '',
              'Each diagram shows its participating source files and complete output, including the entry preamble. Deferred targets are shown as inputs but contribute no body. Blue text indicates links; amber text indicates deferred links. Exact destinations are in the adjacent Markdown.', '',
              '[Coverage and reproduction](README.md) · [Case definitions](cases.json) · [Run records](runs.json)', '', '## Contents', '']
    for case in cases:
        review.append('- ['+case['id']+': '+case['title']+'](#case-'+case['id']+')')
    for case in cases:
        root = 'sources/'+case['id']+'/my-skill'
        command = [str(args.compiler.resolve()), '--root', root, *case['args']]
        run = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
        assert run.returncode == case['exit_code'], (case['id'],run.returncode,run.stderr)
        assert bool(run.stdout) == (run.returncode == 0), (case['id'], 'publication')
        for value in case['contains']:
            assert value in run.stdout, (case['id'],'missing',value,run.stdout)
        for value in case['absent']:
            assert value not in run.stdout, (case['id'],'unexpected',value)
        if case['diagnostic']:
            assert case['diagnostic'] in run.stderr, (case['id'],run.stderr)
        case.update(stdout=run.stdout, stderr=run.stderr, actual_exit=run.returncode)
        rendered = svg(case)
        ET.fromstring(rendered)
        stem = output/case['id']
        stem.with_suffix('.svg').write_text(rendered)
        stem.with_suffix('.stdout.md').write_text(run.stdout)
        stem.with_suffix('.stderr.txt').write_text(run.stderr)
        display = shlex.join(['prosiform','--root',root,*case['args']])
        stem.with_suffix('.command.txt').write_text(display+'\n')
        records.append(dict(case=case['id'],command=display,exit_code=run.returncode,stdout_sha256=hashlib.sha256(run.stdout.encode()).hexdigest(),stderr_sha256=hashlib.sha256(run.stderr.encode()).hexdigest()))
        rel = 'cases/'+case['id']
        review.extend(['','## Case '+case['id'],'',case['focus'],'','Area: '+case['area']+' · Exit status: '+str(run.returncode),'',fence+'bash',display,fence,'',
                       '[Open SVG]('+rel+'.svg) · [Exact stdout]('+rel+'.stdout.md) · [Diagnostics]('+rel+'.stderr.txt) · [Contents](#contents)','',
                       '!['+case['title']+']('+rel+'.svg)'])
    (HERE/'REVIEW.md').write_text('\n'.join(review)+'\n')
    (HERE/'runs.json').write_text(json.dumps(dict(compiler_revision=revision,cases=records),indent=2)+'\n')
    hashes = {str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'sources').rglob('*.md'))}
    (HERE/'source-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    readme = ['# Group command visual validation v2','','**[Review all 36 diagrams](REVIEW.md).**','',
              'This set covers 36 distinct review scenarios for the group command at main revision '+REVISION+'. Depths 1 and 2 demonstrate different arrangements; this is a behavioral review matrix, not a Cartesian product of every depth, source tree, and option. Invalid depth 7 appears as a rejection case.','',
              'The compiler uses --group SLUG:DEPTH. Matching source sections are pooled, members retain distinct destinations, and Overview appears when member subsections accompany pooled sections. Generated names use title case and distinguish members after display transformations.','',
              '## Coverage','','| Area | Cases |','| --- | ---: |']
    for area in dict.fromkeys(c['area'] for c in cases):
        readme.append('| '+area+' | '+str(sum(c['area']==area for c in cases))+' |')
    readme += ['| **Total** | **36** |','','## Case index','','| Case | Review focus |','| --- | --- |']
    for case in cases:
        readme.append('| ['+case['id']+'](cases/'+case['id']+'.svg) | '+case['focus']+' |')
    readme += ['','## Sources and evidence','',
               'Each case has an isolated my-skill source tree under sources/. These small authored examples isolate the approved behaviors; they are not copies of the full example skill. The source-sha256.json manifest pins every input. Cases 26 and 27 include deferred target files for validation without including their contents in the bundle.','',
               'The SVG layout derives from the [original visual validation renderer](../2026-10-22-my-skill-visual-validation/render.py). Images display observed compiler output, with complete stdout and stderr stored beside each image. They support review of current behavior, not independent proof that every requirement is correct.','',
               '## Reproduce','',
               'Check out the pinned revision, install its locked dependencies with uv sync --frozen --no-dev from src/, then run from this folder:','',fence+'bash',
               'python3 render.py --compiler /path/to/prosiform/src/.venv/bin/prosiform --checkout /path/to/prosiform',fence,'',
               'The renderer checks the compiler revision and clean tracked files, all 36 exit statuses, publication or nonpublication, targeted content expectations and diagnostic codes, and SVG XML validity. Each successful compiler run also performs its own candidate and destination validation. Reproduction requires the compiler environment; SVG viewing needs no dependencies.','']
    (HERE/'README.md').write_text('\n'.join(readme))
    print('Validated and rendered '+str(len(cases))+' diagrams.')


if __name__ == '__main__':
    main()
