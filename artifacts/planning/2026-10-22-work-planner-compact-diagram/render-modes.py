"""Render each Modes link in the copied SKILL.md as a separate compact bundle."""

import argparse
import json
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from markdown_it import MarkdownIt


HERE = Path(__file__).resolve().parent


def modes():
    tokens = MarkdownIt('commonmark').parse((HERE/'work-planner/SKILL.md').read_text())
    selected = False
    found = []
    for index, token in enumerate(tokens):
        if token.type == 'heading_open' and int(token.tag[1:]) <= 2:
            selected = tokens[index+1].content == 'Modes'
        if not selected or token.type != 'inline':
            continue
        children = iter(token.children or [])
        for child in children:
            if child.type != 'link_open':
                continue
            label = []
            for part in children:
                if part.type == 'link_close':
                    break
                label.append(part.content)
            target = urlsplit(str(child.attrGet('href')))
            assert not target.scheme and not target.netloc
            path = Path(unquote(target.path))
            assert path.parts[0] == 'modes' and '..' not in path.parts
            assert (HERE/'work-planner'/path).is_file()
            found.append(dict(name=''.join(label), path=path.as_posix(), fragment=unquote(target.fragment), slug=path.stem.removesuffix('-mode')))
    assert found and len({mode['slug'] for mode in found}) == len(found)
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler-checkout', type=Path, required=True)
    options = parser.parse_args()
    checkout = options.compiler_checkout.resolve()
    revision = subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    renderer = checkout/'scripts/render-diagram.py'
    python = checkout/'src/.venv/bin/python'
    selected = modes()
    overview = ['# Work Planner Mode Diagrams', '',
                'Each mode linked from the copied SKILL.md is compiled separately. Artifacts and protocols pool their canonical H2 sections. Compact images retain headings and links; body content is represented by ….', '',
                'Compiler: main '+revision, '', '## Modes', '']
    overview.extend('- ['+mode['name']+'](#'+mode['slug']+')' for mode in selected)
    records = []
    for mode in selected:
        prefix = 'diagrams/'+mode['slug']
        command = [str(python),str(renderer),'work-planner/'+mode['path'],
                   '--root','work-planner','--compact','--group','artifacts:2',
                   '--group','protocols:2','--max-output-bytes','1048576',
                   '--revision',revision,'--output',prefix]
        if mode['fragment']:
            command += ['--section',mode['fragment']]
        run = subprocess.run(command,cwd=HERE,capture_output=True,text=True)
        assert run.returncode == 0, (mode['name'],run.stdout,run.stderr,(HERE/(prefix+'.stderr.txt')).read_text())
        record = json.loads((HERE/(prefix+'.run.json')).read_text())
        assert record['compact'] and record['exit_code'] == 0
        assert record['command'].endswith(mode['path']+('#'+mode['fragment'] if mode['fragment'] else ''))
        ET.parse(HERE/(prefix+'.svg'))
        review = (HERE/(prefix+'.review.md')).read_text()
        image_at = review.index('![Source documents and compiled bundle]')
        section = review[image_at:].replace(']('+mode['slug']+'.', ']('+prefix+'.')
        overview += ['', '## '+mode['name'], '',
                     'Entry document: ['+mode['path']+'](work-planner/'+mode['path']+').', '',section.rstrip()]
        records.append(dict(mode=mode['name'],entry=mode['path'],fragment=mode['fragment'],output=prefix,exit_code=record['exit_code'],opened_files=len(record['sources']),bundle_bytes=(HERE/(prefix+'.stdout.md')).stat().st_size))
        print(mode['name']+': rendered '+str(len(record['sources']))+' opened documents',flush=True)
    (HERE/'work-planner-compact.review.md').write_text('\n'.join(overview)+'\n')
    (HERE/'mode-runs.json').write_text(json.dumps(dict(compiler_revision=revision,groups=['artifacts:2','protocols:2'],modes=records),indent=2)+'\n')
    print('Rendered '+str(len(records))+' mode diagrams.')


if __name__ == '__main__':
    main()
