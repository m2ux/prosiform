"""Render authored proposed-output cases; record current compiler observations separately."""
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

HERE = Path(__file__).resolve().parent
FONT = 'IBM Plex Mono'
BG, CARD, BORDER = '#0d1117', '#161b22', '#303b49'
TEXT, MUTED, LINK, AMBER = '#e6edf3', '#b1c6df', '#58a6ff', '#e3b341'


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
    command='prosiform --root my-skill '+shlex.join(case['args'])
    header=[txt(32,48,case['id']+' · '+case['title'],29),txt(32,90,'PROPOSED OUTPUT · issues #194 and #195 · not produced by the current compiler',20,AMBER)]
    y=126
    for part in textwrap.wrap(command,132,break_long_words=False):
        header.append(txt(32,y,part,20,LINK));y+=30
    for part in textwrap.wrap(case['focus'],145,break_long_words=False):
        header.append(txt(32,y,part,18,MUTED));y+=27
    if case['notes']:
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
        block,h=card(466,at,690,path,(HERE/'my-skill'/path).read_text())
        blocks.append(block);at+=h+22
    expected=case['expected_body'] if case['outcome']=='bundle' else 'Command rejected.\n\nNo bundle is published.\n\nExact diagnostic wording is not specified by the issue.'
    outblock,outh=card(1230,top,880,'Expected bundle body' if case['outcome']=='bundle' else 'Expected CLI result',expected,True)
    blocks.append(outblock)
    middle=top+100
    blocks.append(f'<path d="M1172 {middle} H1190 V{middle-12} L1218 {middle+16} L1190 {middle+44} V{middle+32} H1172Z" fill="{LINK}"/>')
    height=max(at,top+outh,top+treeheight)+65
    footer='Bundle body shown in full; generated entry preamble omitted. Exact Markdown and link destinations: adjacent .expected.md.'
    blocks.append(txt(32,height-25,footer,17,MUTED))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="2142" height="{height}" viewBox="0 0 2142 {height}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(case["title"])}</title><desc id="desc">{html.escape(case["focus"])} Proposed output, not compiler evidence.</desc><rect width="2142" height="{height}" fill="{BG}"/><g font-family="{FONT}" xml:space="preserve">'+''.join(header+blocks)+'</g></svg>\n'


def verify(case):
    for name in case['inputs']:
        assert (HERE/'my-skill'/name).is_file(), name
    if case['outcome']!='bundle': return
    def visible(line):
        return re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',line).strip()
    expected_lines=[visible(line) for line in case['expected_body'].splitlines()]
    for name in case['inputs']:
        for line in (HERE/'my-skill'/name).read_text().splitlines():
            if line.strip() and not line.startswith('#'):
                assert visible(line) in expected_lines,(case['id'],'missing source content',name,line)
    slugs=set();counts={}
    for line in case['expected_body'].splitlines():
        if re.match(r'^#{1,6} ',line):
            name=line.split(' ',1)[1].lower()
            slug=re.sub(r'[^\w\- ]','',name).replace(' ','-')
            n=counts.get(slug,0);counts[slug]=n+1
            slugs.add(slug+('-'+str(n) if n else ''))
    for fragment in re.findall(r'\]\(#([^)]+)\)',case['expected_body']):
        assert fragment in slugs,(case['id'],fragment,slugs)
    for destination in re.findall(r'\]\((?!#)([^)]+)\)',case['expected_body']):
        assert (HERE/'my-skill'/destination).is_file(),(case['id'],destination)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--compiler',type=Path,help='Optional current prosiform executable; observations never define expected output')
    args=parser.parse_args()
    cases=json.loads((HERE/'cases.json').read_text())
    covered={criterion for case in cases for criterion in case['coverage']}
    required={f'195 AC{i}' for i in range(1,9)}|{'194 AC1','194 AC2'}
    assert required<=covered,required-covered
    generated=HERE/'cases';generated.mkdir(exist_ok=True)
    observations=HERE/'current-observations';observations.mkdir(exist_ok=True)
    summary=[]
    for case in cases:
        verify(case)
        base=generated/case['id']
        base.with_suffix('.svg').write_text(svg(case))
        base.with_suffix('.expected.md').write_text(case['expected_body'] if case['outcome']=='bundle' else '# Expected CLI rejection\n\nNo bundle is published. Exact diagnostic wording is not specified.\n')
        base.with_suffix('.command.txt').write_text('prosiform --root my-skill '+shlex.join(case['args'])+'\n')
        if args.compiler:
            # The proposed syntax is run literally. Legacy comparison is separate.
            for mode in ['proposed-command','legacy-comparison']:
                command=list(case['args'])
                if mode=='legacy-comparison':
                    for i,token in enumerate(command[:-1]):
                        if token=='--group' and ':' not in command[i+1]: command[i+1]+=':1'
                run=subprocess.run([str(args.compiler),'--root',str(HERE/'my-skill'),*command],capture_output=True,text=True)
                stem=observations/(case['id']+'.'+mode)
                Path(str(stem)+'.stdout.md').write_text(run.stdout)
                Path(str(stem)+'.stderr.txt').write_text(run.stderr)
                summary.append(dict(case=case['id'],mode=mode,args=command,exit_code=run.returncode))
    if args.compiler:
        (observations/'runs.json').write_text(json.dumps(summary,indent=2)+'\n')
    hashes={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'my-skill').rglob('*.md'))}
    (HERE/'source-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
    review=['# My-skill visual review — issues #194 and #195',
      '', '**Proposed output, not current compiler output.** These images show what the tool would generate after the current issue designs are applied. The current compiler still requires `--group SLUG:DEPTH`; the proposed commands use `--group SLUG`.',
      '', 'Each image includes its participating file tree, rendered source fragments, and the complete proposed bundle body. Only the generated entry preamble is omitted. Click the SVG link to zoom; the adjacent Markdown contains exact heading levels and link destinations.',
      '', 'Generated headings use the existing title convention: capitalize the first character of each word, preserve the rest (including HTTP), turn hyphens into spaces, and retain path separators in ungrouped document names. Authored headings retain their spelling.',
      '', '**Review assumptions:** member order follows source paths; nested grouping retains deepest-folder membership; CLI rejections specify no exact diagnostic wording. These boundary cases are labeled in their images. This suite covers the current issue bodies, not the historical section-group/folder-group proposal preserved in issue comments.',
      '', '[Source layout, coverage, and reproduction](README.md) · [Case definitions](cases.json) · [Current compiler observations](current-observations/runs.json)',
      '', '## Contents', '']
    for case in cases:
        review.append(f'- [{case["id"]}: {case["title"]}](#case-{case["id"]})')
    for case in cases:
        stem='cases/'+case['id']
        review+=['',f'## Case {case["id"]}', '',case['title'], '', '**Review:** '+case['focus'], '', '**Coverage:** '+', '.join(case['coverage']), '', '```bash', 'prosiform --root my-skill '+shlex.join(case['args']), '```']
        if case['notes']: review+=['','**Review note:** '+case['notes']]
        review+=['',f'[Open SVG]({stem}.svg) · [Exact expected Markdown]({stem}.expected.md) · [Back to contents](#contents)', '', f'![{case["title"]} — proposed output]({stem}.svg)']
    (HERE/'REVIEW.md').write_text('\n'.join(review)+'\n')
    readme=['# My-skill visual validation', '', '**Start here: [all 30 proposed-output images on one page](REVIEW.md).**', '',
      'This review suite interprets the current [#194](https://github.com/m2ux/prosiform/issues/194) and [#195](https://github.com/m2ux/prosiform/issues/195) bodies as read on 2026-10-22: folder-only grouping, one intact section per member, own-title absorption, distinct member destinations, and consistent generated title casing.', '',
      'Expected Markdown is authored from those requirements. The renderer does not derive expected output from the current compiler. These are reviewable predictions, not evidence that the issues are implemented or their acceptance criteria pass.', '',
      '## Layout', '', '```text', 'my-skill/']
    for path in sorted((HERE/'my-skill').rglob('*.md')):
        readme.append('  '+str(path.relative_to(HERE/'my-skill')))
    readme+=['```', '', 'The source snapshot matches `example/my-skill/` on main (excluding its visual-case navigation page). Existing README entry points are preserved; additional cases are selected explicitly. [SHA-256 manifest](source-sha256.json) pins every input.', '',
      '## Coverage', '', '| Case | Issue criteria | Review focus |', '| --- | --- | --- |']
    for case in cases:
        readme.append(f'| [{case["id"]}](cases/{case["id"]}.svg) | {", ".join(case["coverage"])} | {case["focus"]} |')
    readme+=['', 'The six own-title cases cover every supported source heading level (H1–H6). The CLI rows cover folder-only syntax, multiple distinct groups, rejected depth syntax, and duplicate group declarations. Nested selection is an explicitly labeled retained-behavior assumption.', '',
      '## Reproduce the visuals', '', 'From this directory:', '', '```bash', 'python3 render.py', '```', '',
      'This regenerates `REVIEW.md`, each SVG, expected body, command file, and the source manifest from [cases.json](cases.json). It validates all expected internal fragments and deferred file destinations. IBM Plex Mono is the preferred font; SVG text remains selectable.', '',
      'For a raster preview:', '', '```bash', 'QT_QPA_PLATFORM=offscreen ksvgtopng 2142 936 cases/05-shared-section-names.svg /tmp/shared-sections.png', '```', '',
      '## Current-tool evidence', '', 'The observed compiler revision is `7ba5fe9f44ade4a19b843619aeea37abf2c7f4b1`. [Run records](current-observations/runs.json) include exit codes and exact arguments. Each case has raw stdout and stderr for the proposed command and, separately, the closest legacy `--group SLUG:1` comparison. Neither observation is used to create the proposed images.', '',
      'To refresh observations with an explicitly chosen compiler:', '', '```bash', 'python3 render.py --compiler /absolute/path/to/prosiform', '```', '',
      '## Review decisions', '',
      '- Member ordering follows root-relative paths, consistent with the current arrangement; issues do not request a new order.',
      '- A source heading retains its text when nested beneath a member; a leading own-name title is absorbed at every tested level.',
      '- Nested matching groups retain deepest-directory membership (case 29).',
      '- Exact rejection diagnostics are unspecified. Rejection images promise no bundle, not particular wording.',
      '- Expected files contain the complete bundle body. The generated entry preamble is omitted from the visual contract; member and section links are shown with exact destinations in the Markdown.',
      '- Historical section-group/folder-group proposals in issue comments are outside this suite: the current #195 body specifies one folder-only `--group` option.', '',
      'These images cover the finite permutations above; they are not a substitute for the implementation’s full corpus, destination, and preservation tests.']
    (HERE/'README.md').write_text('\n'.join(readme)+'\n')
    print(f'Validated and rendered {len(cases)} proposed-output SVGs; {len(summary)} current-compiler observations.')


if __name__=='__main__': main()
