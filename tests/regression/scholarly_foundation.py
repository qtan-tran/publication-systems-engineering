from __future__ import annotations
import json, os, subprocess, sys, tempfile, shutil, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
MODULES={'canonical-locators','apparatus','multilingual','bibliography','index','scholarly-matter'}

def run(args,cwd=REPO,expect=0,timeout=120):
    p=subprocess.run(args,cwd=cwd,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-5000:]}\nstderr:\n{p.stderr[-5000:]}")
    return p

def main():
    checks=[]
    mods=json.loads(run(CLI+['modules','--json']).stdout)
    ids={m['id'] for m in mods['modules']}
    checks.append(('module_registry',MODULES.issubset(ids),str(sorted(ids))))
    profs=json.loads(run(CLI+['profiles','--json']).stdout)
    scholarly=next((p for p in profs['profiles'] if p['id']=='scholarly-edition'),None)
    checks.append(('scholarly_profile',bool(scholarly) and MODULES.issubset(set(scholarly.get('module_policy',{}))),'semantic modules declared'))
    checks.append(('module_schema',(REPO/'schema/module.schema.json').is_file(),'module schema present'))

    with tempfile.TemporaryDirectory(prefix='pse-j-') as td:
        parent=Path(td)
        run(CLI+['new',str(parent),'--non-interactive','--profile','scholarly-edition','--title','Synthetic Scholarly Edition','--author','PSE Regression','--language','en','--publication-year','2027','--slug','edition'])
        project=parent/'edition'
        run(CLI+['build',str(project)],timeout=180)
        q=json.loads(run(CLI+['check',str(project)]).stdout)
        checks.append(('build_qa',q['status']=='pass' and q['summary']['error']==0,'machine QA pass'))
        checks.append(('biber_output',(project/'build/book.bbl').is_file(),'bibliography built'))
        checks.append(('index_output',(project/'build/book.ind').is_file(),'index built'))
        log=(project/'build/book.log').read_text(errors='replace')
        checks.append(('greek_glyphs','Missing character:' not in log,'polytonic Greek rendered'))
        aux=(project/'build/book.aux').read_text(errors='replace')
        checks.append(('locator_persistence','pse-loc:canonical:A1' in aux and 'pse-loc:canonical:B1' in aux,'canonical labels persisted'))
        pr=run(CLI+['proof',str(project),'--recipient','Synthetic Reviewer'],timeout=180)
        checks.append(('proof_pipeline','proof:' in pr.stdout and any((project/'build/proofs').glob('*.pdf')),'recipient proof'))
        checks.append(('release_inheritance','release semantics remain backbone-owned and covered by release-engineering regression','not duplicated in scholarly-foundation regression'))


        # Duplicate canonical identifiers must fail closed.
        dup=parent/'dup'; shutil.copytree(project,dup,ignore=shutil.ignore_patterns('build','release'))
        text=dup/'content/text.tex'; content=text.read_text(); text.write_text(content+'\n\\PSELocator{A1}Duplicate locator synthetic failure.\n')
        p=subprocess.run(CLI+['build',str(dup)],cwd=REPO,env=ENV,text=True,capture_output=True,timeout=120)
        checks.append(('duplicate_locator_rejected',p.returncode!=0 and 'pse-module-canonical-locators Error' in (p.stdout+p.stderr),'fail closed'))

    # Installed wheel must ship profile, modules, and schemas.
    with tempfile.TemporaryDirectory(prefix='pse-j-wheel-') as td:
        root=Path(td); wh=root/'wh'; wh.mkdir()
        run([sys.executable,'-m','pip','wheel','--no-build-isolation','--no-deps','-w',str(wh),str(REPO)],cwd=root,timeout=180)
        wheel=next(wh.glob('publication_systems_engineering-*.whl'))
        with zipfile.ZipFile(wheel) as zf:
            names=set(zf.namelist())
            checks.append(('wheel_profile',any(n.endswith('/profiles/scholarly-edition/profile.json') for n in names),'scholarly profile packaged'))
            for m in MODULES:
                checks.append((f'wheel_module_{m}',any(n.endswith(f'/modules/{m}/module.json') for n in names) and any(n.endswith(f'/modules/{m}/pse-module-{m}.sty') for n in names),'module packaged'))
            checks.append(('wheel_module_schema',any(n.endswith('/schema/module.schema.json') for n in names),'module schema packaged'))

    failed=[x for x in checks if not x[1]]
    print('Scholarly semantic foundation regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
