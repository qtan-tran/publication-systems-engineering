from pathlib import Path
import json, os, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PSE_ROOT']=str(ROOT); ENV['PYTHONPATH']=str(ROOT/'tools')
CLI=[sys.executable,'-m','pse_cli.cli']
def run(args,cwd=None): return subprocess.run(CLI+args,cwd=cwd or ROOT,env=ENV,text=True,capture_output=True)
def main():
  r=[]
  def ck(n,ok,d=''): r.append({'name':n,'status':'pass' if ok else 'fail','detail':d})
  man=json.loads((ROOT/'modules/parallel-text/module.json').read_text())
  ck('existing module extended',man['id']=='parallel-text' and 'alignment-locators' in man['capabilities'] and 'typed-alignment-notes' in man['capabilities'])
  sty=(ROOT/'modules/parallel-text/pse-module-parallel-text.sty').read_text()
  ck('locator api exists','\\PSEParallelAlignmentLocator' in sty)
  ck('typed note api exists','\\PSEParallelNote' in sty)
  ck('translation note compatibility remains','\\PSEParallelTranslationNote' in sty)
  schema=json.loads((ROOT/'schema/bilingual-layout.schema.json').read_text())
  modes=set(schema['properties']['mode']['enum']); expected={'parallel-columns','facing-pages','sequential-blocks','source-dominant','target-dominant'}
  ck('five presentation modes contracted',modes==expected,str(sorted(modes)))
  with tempfile.TemporaryDirectory(prefix='pse-par137-') as td:
    parent=Path(td)
    n=run(['new',str(parent),'--non-interactive','--profile','bilingual-edition','--title','Parallel Modes','--author','Synthetic Editor','--language','en','--publication-year','2027'])
    pr=parent/'parallel-modes'; ck('generator succeeds',n.returncode==0,n.stderr[-300:])
    src=pr/'content/parallel.tex'; text=src.read_text()
    ck('generated source includes stable locator','\\PSEParallelAlignmentLocator{a1}' in text)
    ck('generated source includes typed note','\\PSEParallelNote{a2}{editorial}' in text)
    original=text
    cfgp=pr/'config/bilingual-layout.json'; cfg=json.loads(cfgp.read_text()); ck('generator emits layout schema 1.1',cfg['schema_version']=='1.1')
    for mode in sorted(expected):
      cfg['mode']=mode; cfg['long_segment_policy']='review' if mode=='facing-pages' else 'flow'; cfgp.write_text(json.dumps(cfg,indent=2)+'\n')
      b=run(['build',str(pr)]); ck(f'{mode} builds',b.returncode==0,(b.stdout+b.stderr)[-400:])
      q=run(['check',str(pr)]); ck(f'{mode} QA passes',q.returncode==0,(q.stdout+q.stderr)[-400:])
      ck(f'{mode} leaves semantic source unchanged',src.read_text()==original)
    rep=json.loads((pr/'build/qa-report.json').read_text()); pm=rep.get('metrics',{}).get('parallel_text',{})
    ck('QA inventories locator',pm.get('locators')==1,str(pm))
    ck('QA inventories typed notes',pm.get('notes')==2 and pm.get('translation_notes')==1,str(pm))
    src.write_text(original+'\n\\PSEParallelAlignmentLocator{missing}{x}\n')
    bad=run(['check',str(pr)]); ck('unresolved locator fails closed',bad.returncode==1 and 'parallel_unresolved_locator' in bad.stdout,bad.stdout[-500:])
    src.write_text(original+'\n\\PSEParallelAlignmentLocator{a1}{duplicate}\n')
    bad=run(['check',str(pr)]); ck('duplicate locator fails closed',bad.returncode==1 and 'parallel_duplicate_locator' in bad.stdout,bad.stdout[-500:])
    src.write_text(original+'\n\\PSEParallelNote{a2}{editorial}{duplicate}\n')
    bad=run(['check',str(pr)]); ck('duplicate typed note fails closed',bad.returncode==1 and 'parallel_duplicate_note' in bad.stdout,bad.stdout[-500:])
  report={'audit_kind':'parallel_text_consolidation','status':'pass' if all(x['status']=='pass' for x in r) else 'fail','checks':r}
  (ROOT/'build').mkdir(exist_ok=True); (ROOT/'build/regression-output.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2)); return 0 if report['status']=='pass' else 1
if __name__=='__main__': raise SystemExit(main())
