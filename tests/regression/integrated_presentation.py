from __future__ import annotations
import json, os, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
FIELDS=('preset','hierarchy','publication_unit_metadata','grid','side_material','apparatus','locator','parallel_text')

def run(args,expect=0,timeout=240):
    p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\n{p.stdout[-4000:]}\n{p.stderr[-4000:]}")
    return p

def main():
    checks=[]
    def ck(n,ok,d=''): checks.append((n,bool(ok),d))
    core=(ROOT/'core/pse-core.sty').read_text()
    ck('core_contract',r'\newcommand{\PSEIntegratedPresentationContractVersion}{1}' in core,'v1')
    for token in ('PSEConfigureIntegratedPresentation','PSEPresentationPreset','PSEPresentationHierarchyMode','PSEPresentationPublicationUnitMode','PSEPresentationGridMode','PSEPresentationSideMaterialMode','PSEPresentationApparatusMode','PSEPresentationLocatorMode','PSEPresentationParallelTextMode'):
        ck('core_'+token,('\\'+token) in core,token)
    ck('schema',(ROOT/'schema/presentation-profile-1.0.schema.json').is_file(),'presentation-profile-1.0')
    descriptors=[]
    for path in sorted((ROOT/'profiles').glob('*/presentation.json')):
        data=json.loads(path.read_text()); descriptors.append(data); pid=data['profile']
        sty=(ROOT/'profiles'/pid/f'pse-profile-{pid}.sty').read_text()
        expected='\\PSEConfigureIntegratedPresentation'+''.join('{'+data[f]+'}' for f in FIELDS)
        ck('binding_'+pid,expected in sty,expected)
    ck('nine_descriptors',len(descriptors)==9,str(len(descriptors)))
    cli_json=json.loads(run(CLI+['profiles','--presentation','--json']).stdout)
    ck('cli_json',len(cli_json.get('presentations',[]))==9 and cli_json.get('presentation_schema_version')=='1.0','9 descriptors')
    text=run(CLI+['profiles','--presentation']).stdout
    ck('cli_human','presentation preset:' in text,'human presentation output')
    ck('tech_doc',(ROOT/'docs/architecture/INTEGRATED-PRESENTATION-SYSTEM.md').is_file(),'doc')
    ck('wiki_stub',(ROOT/'wiki/how-pse-works/presentation-system.md').is_file(),'wiki')
    ck('ia_freeze',(ROOT/'docs/documentation/WIKI-INFORMATION-ARCHITECTURE.md').is_file(),'IA')
    nav=(ROOT/'mkdocs.yml').read_text()
    for label in ('Getting Started','How PSE Works','Book Profiles','Book Features','Workflows','Quality and Release','Customization','Reference'):
        ck('nav_'+label.lower().replace(' ','_'),nav.count(label+':')==1,label)
    with tempfile.TemporaryDirectory(prefix='pse-present-') as td:
        td=Path(td)
        run(CLI+['new',str(td),'--non-interactive','--profile','critical-edition','--title','Presentation Test','--author','Synthetic Author','--language','en','--publication-year','2027','--slug','critical'])
        project=td/'critical'; run(CLI+['build',str(project)])
        qa=json.loads(run(CLI+['check',str(project)]).stdout)
        pm=qa.get('metrics',{}).get('presentation_system',{})
        ck('critical_qa',qa['status']=='pass' and pm.get('preset')=='source-critical' and pm.get('apparatus')=='multi-stream' and pm.get('locator')=='primary-visible',json.dumps(pm))
        sem=project/'config/semantic-modules.json'; data=json.loads(sem.read_text()); data['deactivate']=['apparatus']; sem.write_text(json.dumps(data,indent=2)+'\n')
        # required module deactivation itself fails closed during resolver; presentation never repairs it.
        p=subprocess.run(CLI+['build',str(project)],cwd=ROOT,env=ENV,text=True,capture_output=True)
        ck('no_semantic_repair',p.returncode!=0 and 'required' in (p.stdout+p.stderr).lower(),(p.stdout+p.stderr)[-1200:])
    failed=[x for x in checks if not x[1]]
    print('Integrated presentation regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
