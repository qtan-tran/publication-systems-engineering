from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
def run(args,expect=0,timeout=180):
    p=subprocess.run(args,cwd=REPO,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect: raise AssertionError(f"{args}\n{p.stdout[-4000:]}\n{p.stderr[-4000:]}")
    return p
def main():
    checks=[]
    mods=json.loads(run(CLI+['modules','--json']).stdout)['modules']
    checks.append(('manifest_v11',all(m['schema_version']=='1.1' and m['api_version']=='1' for m in mods),'module API schema 1.1/1'))
    checks.append(('namespaces',len({m['namespace'] for m in mods})==len(mods),'module namespaces unique'))
    app=next(m for m in mods if m['id']=='apparatus')
    checks.append(('capability_dependency','canonical-locators' in app['requires_capabilities'],'apparatus capability dependency declared'))
    checks.append(('schemas',(REPO/'schema/locator-schemes.schema.json').is_file() and (REPO/'schema/semantic-modules.schema.json').is_file(),'Semantic namespace schemas present'))
    with tempfile.TemporaryDirectory(prefix='pse-l-') as td:
        root=Path(td)
        # title-level activation on a non-scholarly profile; resolver must add canonical-locators.
        run(CLI+['new',str(root),'--non-interactive','--profile','basic-book','--title','Module Activation','--author','PSE','--language','en','--publication-year','2027','--slug','basic'])
        basic=root/'basic'; cfg={'schema_version':'1.0','activate':['apparatus'],'config':{}}
        (basic/'config/semantic-modules.json').write_text(json.dumps(cfg),encoding='utf-8')
        run(CLI+['build',str(basic)])
        generated=(basic/'build/pse-modules.tex').read_text()
        checks.append(('title_activation','pse-module-apparatus' in generated,'title module activated'))
        checks.append(('capability_resolution','pse-module-canonical-locators' in generated,'unique provider auto-resolved'))
        checks.append(('basic_qa',json.loads(run(CLI+['check',str(basic)]).stdout)['status']=='pass','title activation preserves QA'))
        # config for inactive title module is rejected.
        bad=root/'badcfg'; shutil.copytree(basic,bad,ignore=shutil.ignore_patterns('build','release'))
        (bad/'config/semantic-modules.json').write_text(json.dumps({'schema_version':'1.0','activate':[],'config':{'apparatus':{}}}),encoding='utf-8')
        p=subprocess.run(CLI+['build',str(bad)],cwd=REPO,env=ENV,text=True,capture_output=True)
        checks.append(('inactive_config_rejected',p.returncode!=0 and 'inactive title module' in (p.stdout+p.stderr),'inactive config fail-closed'))
        # scholarly namespaced locator composition.
        run(CLI+['new',str(root),'--non-interactive','--profile','scholarly-edition','--title','Namespace Edition','--author','PSE','--language','en','--publication-year','2027','--slug','scholarly'])
        sch=root/'scholarly'
        schemes=json.loads((sch/'config/locator-schemes.json').read_text())
        schemes['schemes']['folio']={'id':'synthetic-folio','order':['f1','f2'],'require_complete':True,'strict_order':True}
        (sch/'config/locator-schemes.json').write_text(json.dumps(schemes),encoding='utf-8')
        tp=sch/'content/text.tex'; tp.write_text(tp.read_text()+"\n\\PSELocatorNS{folio}{f1}Folio synthetic one.\n\\PSELocatorNS{folio}{f2}Folio synthetic two.\n",encoding='utf-8')
        run(CLI+['build',str(sch)])
        qa=json.loads(run(CLI+['check',str(sch)]).stdout); sq=qa['metrics']['scholarly']
        checks.append(('multi_namespace',qa['status']=='pass' and sq['locator_schemes']['folio']['present']==2,'two locator namespaces audited'))
        # same identifier may exist in another namespace.
        schemes['schemes']['folio']={'id':'synthetic-folio','order':['A1','f2'],'require_complete':True,'strict_order':True}; (sch/'config/locator-schemes.json').write_text(json.dumps(schemes),encoding='utf-8')
        txt=tp.read_text().replace('{folio}{f1}','{folio}{A1}'); tp.write_text(txt,encoding='utf-8')
        run(CLI+['build',str(sch)]); qa=json.loads(run(CLI+['check',str(sch)]).stdout)
        checks.append(('cross_namespace_identity',qa['status']=='pass','same id allowed across namespaces'))
        # undeclared namespace fails QA.
        und=root/'undeclared'; shutil.copytree(sch,und,ignore=shutil.ignore_patterns('build','release'))
        (und/'content/text.tex').write_text((und/'content/text.tex').read_text()+"\n\\PSELocatorNS{line}{1}Undeclared namespace.\n",encoding='utf-8')
        run(CLI+['build',str(und)])
        p=subprocess.run(CLI+['check',str(und)],cwd=REPO,env=ENV,text=True,capture_output=True); q=json.loads(p.stdout)
        checks.append(('undeclared_namespace_rejected',p.returncode==1 and any(f['code']=='undeclared_locator_namespace' for f in q['findings']),'undeclared namespace error'))
    # declarative hook allow-list: arbitrary executable hooks cannot be introduced.
    tmp=json.loads((REPO/'modules/canonical-locators/module.json').read_text()); tmp['qa_hooks']=['../../evil.py']
    from pse_cli.cli import _validate_module_manifest
    try: _validate_module_manifest(tmp,expected_id='canonical-locators'); hook_ok=False
    except SystemExit: hook_ok=True
    checks.append(('qa_hook_allowlist',hook_ok,'arbitrary QA code path rejected'))
    # wheel carries semantic namespace schema contracts.
    with tempfile.TemporaryDirectory(prefix='pse-l-wheel-') as td:
        wh=Path(td); run([sys.executable,'-m','pip','wheel','--no-build-isolation','--no-deps','-w',str(wh),str(REPO)],timeout=240)
        wheel=next(wh.glob('publication_systems_engineering-*.whl'))
        with zipfile.ZipFile(wheel) as zf:
            names=set(zf.namelist())
            checks.append(('wheel_schemas',any(n.endswith('/schema/locator-schemes.schema.json') for n in names) and any(n.endswith('/schema/semantic-modules.schema.json') for n in names),'Semantic namespace schemas packaged'))
            checks.append(('wheel_module_manifests',any(n.endswith('/modules/apparatus/module.json') for n in names),'module manifest packaged'))
    failed=[x for x in checks if not x[1]]
    print('Semantic namespace and composition regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
