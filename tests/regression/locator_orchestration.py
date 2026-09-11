from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']

def run(args,cwd=ROOT,expect=0,timeout=180):
    p=subprocess.run(args,cwd=cwd,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-5000:]}\nstderr:\n{p.stderr[-5000:]}")
    return p

def main():
    checks=[]
    def ck(n,ok,d=''): checks.append((n,bool(ok),d))

    core=(ROOT/'core/pse-core.sty').read_text()
    ck('core_contract','\\PSELocatorOrchestrationContractVersion' in core and '\\PSEConfigureLocatorOrchestration' in core)
    ck('not_locator_engine','\\PSELocatorNS' not in core and '\\PSEDramaLine' not in core and '\\PSEVerseLine' not in core and '\\PSEParallelAlign' not in core)
    ck('schema',(ROOT/'schema/locator-orchestration-1.0.schema.json').is_file())
    mods=json.loads(run(CLI+['modules','--json']).stdout)['modules']
    ck('no_new_module',len(mods)==14,str([m['id'] for m in mods]))
    owners={'canonical-locators','dramatic-locators','verse-structure','parallel-text'}
    ck('owners_preserved',owners.issubset({m['id'] for m in mods}),str(sorted(owners)))

    from pse_cli.semantic_parser import parse_text
    nodes,errs=parse_text('\\PSEVerseLine{l1}[17]{Synthetic}\n\\PSEVerseLine{l2}{No label}','content/poem.tex')
    verse=[n for n in nodes if n.name=='PSEVerseLine']
    ck('verse_parser',not errs and [n.args[:2] for n in verse]==[('l1','17'),('l2','')],repr([(n.args,errs) for n in verse]))

    expected={
        'critical-edition':('canonical','show'),
        'scholarly-edition':('canonical','show'),
        'drama':('dramatic-line','show'),
        'poetry':('verse-line','source-defined'),
        'bilingual-edition':('parallel-alignment','source-defined'),
    }
    with tempfile.TemporaryDirectory(prefix='pse-locator-orch-') as td:
        td=Path(td)
        projects={}
        for profile,(primary,visibility) in expected.items():
            slug=profile
            run(CLI+['new',str(td),'--non-interactive','--profile',profile,'--title','Synthetic Locator Orchestration','--author','PSE Regression','--language','en','--publication-year','2027','--slug',slug])
            project=td/slug; projects[profile]=project
            cfg=json.loads((project/'config/locator-orchestration.json').read_text())
            ck('generated_'+profile,cfg['primary_namespace']==primary and cfg['visible_numbering']==visibility and cfg['stable_id_policy']=='required',str(cfg))

        # Build/check four different semantic owners in separate project directories.
        for profile,count in [('critical-edition',4),('drama',4),('poetry',6),('bilingual-edition',2)]:
            project=projects[profile]
            run(CLI+['build',str(project)],timeout=220)
            qa=json.loads(run(CLI+['check',str(project)]).stdout)
            lo=qa.get('metrics',{}).get('locator_orchestration',{})
            primary=expected[profile][0]
            ck('qa_'+profile,qa['status']=='pass' and lo.get('primary_namespace')==primary and lo.get('namespaces',{}).get(primary,{}).get('count')==count,json.dumps(lo)[:1000])
            generated=(project/'build/pse-locator-orchestration.tex').read_text()
            ck('generated_bridge_'+profile,primary in generated and '\\PSEConfigureLocatorOrchestration' in generated,generated)

        # A configured namespace whose owner is inactive must fail closed at check time.
        run(CLI+['new',str(td),'--non-interactive','--profile','basic-book','--title','Bad Orchestration','--author','PSE Regression','--language','en','--publication-year','2027','--slug','bad'])
        bad=td/'bad'
        (bad/'config/locator-orchestration.json').write_text(json.dumps({'schema_version':'1.0','primary_namespace':'canonical','secondary_namespaces':[],'visible_numbering':'show','stable_id_policy':'required'},indent=2)+'\n')
        run(CLI+['build',str(bad)])
        p=run(CLI+['check',str(bad)],expect=1)
        q=json.loads(p.stdout); codes={x['code'] for x in q['findings']}
        ck('inactive_namespace_rejected','locator_orchestration_inactive_namespace' in codes,str(codes))

        # Primary namespace may not also be secondary; validation fails before TeX.
        dup=projects['poetry']/'config/locator-orchestration.json'
        data=json.loads(dup.read_text()); data['secondary_namespaces']=['verse-line']; dup.write_text(json.dumps(data,indent=2)+'\n')
        p=subprocess.run(CLI+['build',str(projects['poetry'])],cwd=ROOT,env=ENV,text=True,capture_output=True)
        ck('duplicate_policy_rejected',p.returncode!=0 and 'primary may not also be secondary' in (p.stdout+p.stderr),(p.stdout+p.stderr)[-1000:])

    failed=[x for x in checks if not x[1]]
    print('Locator orchestration regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
