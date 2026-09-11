from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']

def run(args,cwd=REPO,expect=0,timeout=180):
    p=subprocess.run(args,cwd=cwd,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-5000:]}\nstderr:\n{p.stderr[-5000:]}")
    return p

def qacheck(project:Path):
    return json.loads(run(CLI+['check',str(project)]).stdout)

def main():
    checks=[]
    # Runtime contract files.
    checks.append(('locator_schema',(REPO/'schema/locator-scheme.schema.json').is_file(),'schema present'))
    mods=json.loads(run(CLI+['modules','--json']).stdout)['modules']
    apparatus=next(m for m in mods if m['id']=='apparatus')
    checks.append(('module_dependency','canonical-locators' in apparatus.get('depends_on',[]),'apparatus depends on locators'))
    doctor=json.loads(run(CLI+['doctor','--profile','scholarly-edition','--json']).stdout)
    checks.append(('scholarly_doctor',doctor['summary']['required_failures']==0,'profile dependencies pass'))

    with tempfile.TemporaryDirectory(prefix='pse-k-') as td:
        parent=Path(td)
        run(CLI+['new',str(parent),'--non-interactive','--profile','scholarly-edition','--title','Synthetic Locator Edition','--author','PSE Regression','--language','en','--publication-year','2027','--slug','edition'])
        project=parent/'edition'
        checks.append(('scheme_generated',(project/'config/locator-scheme.json').is_file(),'generator emits locator scheme'))
        run(CLI+['build',str(project)])
        qa=qacheck(project)
        sq=qa.get('metrics',{}).get('scholarly',{})
        checks.append(('scholarly_qa_pass',qa['status']=='pass' and sq.get('locator_scheme',{}).get('present')==3,'3/3 canonical locators'))
        checks.append(('bibliography_index',(project/'build/book.bbl').is_file() and (project/'build/book.ind').is_file(),'auxiliary outputs'))
        # Range macro should compile and be inventoried.
        observed_ranges=[{'start':x['start'],'end':x['end'],'file':x['file']} for x in (sq.get('locator_ranges') or [])]
        checks.append(('range_inventory',observed_ranges==[{'start':'A1','end':'A2','file':'content/apparatus.tex'}],'apparatus range inventoried'))
        # Recipient proof inherits the security backbone.
        run(CLI+['proof',str(project),'--recipient','Scholarly Reviewer'])
        checks.append(('scholarly_proof',bool(list((project/'build/proofs').glob('*.pdf'))),'proof generated'))

        # Missing canonical locator must be an error under require_complete.
        missing=parent/'missing'; shutil.copytree(project,missing,ignore=shutil.ignore_patterns('build','release'))
        tp=missing/'content/text.tex'; txt=tp.read_text(); txt=txt.replace('\\PSELocator{A2}','') ; tp.write_text(txt)
        p=subprocess.run(CLI+['check',str(missing)],cwd=REPO,env=ENV,text=True,capture_output=True)
        q=json.loads(p.stdout); codes={f['code'] for f in q['findings']}
        checks.append(('missing_rejected',p.returncode==1 and 'missing_canonical_locators' in codes,'missing locator error'))

        # Out of order locator must be an error.
        oo=parent/'outoforder'; shutil.copytree(project,oo,ignore=shutil.ignore_patterns('build','release'))
        tp=oo/'content/text.tex'; txt=tp.read_text(); txt=txt.replace('\\PSELocator{A1}','\\PSELocator{ZZ}').replace('\\PSELocator{A2}','\\PSELocator{A1}').replace('\\PSELocator{ZZ}','\\PSELocator{A2}'); tp.write_text(txt)
        p=subprocess.run(CLI+['check',str(oo)],cwd=REPO,env=ENV,text=True,capture_output=True)
        q=json.loads(p.stdout); codes={f['code'] for f in q['findings']}
        checks.append(('order_rejected',p.returncode==1 and 'canonical_locator_out_of_order' in codes,'out-of-order error'))

        # Reversed range must be an error.
        rr=parent/'range'; shutil.copytree(project,rr,ignore=shutil.ignore_patterns('build','release'))
        ap=rr/'content/apparatus.tex'; ap.write_text(ap.read_text().replace('\\PSEApparatusStreamRangeEntry{editorial}{A1}{A2}','\\PSEApparatusStreamRangeEntry{editorial}{A2}{A1}'))
        p=subprocess.run(CLI+['check',str(rr)],cwd=REPO,env=ENV,text=True,capture_output=True)
        q=json.loads(p.stdout); codes={f['code'] for f in q['findings']}
        checks.append(('range_rejected',p.returncode==1 and 'invalid_locator_range' in codes,'reversed range error'))

    # Wheel must ship new schema and scholarly contracts.
    with tempfile.TemporaryDirectory(prefix='pse-k-wheel-') as td:
        root=Path(td); wh=root/'wh'; wh.mkdir()
        run([sys.executable,'-m','pip','wheel','--no-build-isolation','--no-deps','-w',str(wh),str(REPO)],cwd=root,timeout=240)
        wheel=next(wh.glob('publication_systems_engineering-*.whl'))
        with zipfile.ZipFile(wheel) as zf:
            names=set(zf.namelist())
            checks.append(('wheel_locator_schema',any(n.endswith('/schema/locator-scheme.schema.json') for n in names),'locator schema packaged'))
            checks.append(('wheel_scholarly_modules',any(n.endswith('/modules/canonical-locators/pse-module-canonical-locators.sty') for n in names) and any(n.endswith('/modules/apparatus/pse-module-apparatus.sty') for n in names),'range-capable modules packaged'))

    failed=[x for x in checks if not x[1]]
    print('Scholarly QA and locator contract regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
