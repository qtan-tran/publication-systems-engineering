from pathlib import Path
import json, os, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PSE_ROOT']=str(ROOT); ENV['PYTHONPATH']=str(ROOT/'tools')
CLI=[sys.executable,'-m','pse_cli.cli']
def run(args,cwd=None): return subprocess.run(CLI+args,cwd=cwd or ROOT,env=ENV,text=True,capture_output=True)
def main():
  results=[]
  def ck(name,ok,detail=''): results.append({'name':name,'status':'pass' if ok else 'fail','detail':detail})
  with tempfile.TemporaryDirectory(prefix='pse-p-') as td:
    parent=Path(td)
    n=run(['new',str(parent),'--non-interactive','--profile','bilingual-edition','--title','Synthetic Parallel Edition','--author','Example Editor','--language','en','--publication-year','2027'])
    pr=parent/'synthetic-parallel-edition'; ck('generator creates bilingual project',n.returncode==0,n.stderr[-300:])
    ck('parallel config exists',(pr/'config/parallel-text.json').is_file())
    ck('bilingual layout config exists',(pr/'config/bilingual-layout.json').is_file())
    b=run(['build',str(pr)]); ck('parallel-columns build passes',b.returncode==0,b.stderr[-400:])
    q=run(['check',str(pr)]); ck('parallel-columns QA passes',q.returncode==0,q.stderr[-400:])
    rep=json.loads((pr/'build/qa-report.json').read_text()); ck('parallel inventory remains semantic',rep.get('metrics',{}).get('parallel_text',{}).get('alignments')==2)
    cfg=pr/'config/bilingual-layout.json'; d=json.loads(cfg.read_text()); d['mode']='facing-pages'; d['long_segment_policy']='review'; cfg.write_text(json.dumps(d,indent=2)+'\n')
    b2=run(['build',str(pr)]); ck('facing-pages build passes',b2.returncode==0,b2.stderr[-400:])
    q2=run(['check',str(pr)]); ck('facing-pages QA passes',q2.returncode==0,q2.stderr[-400:])
    source=(pr/'content/parallel.tex').read_text(); ck('layout switch does not rewrite semantic source','PSEParallelAlign{a2}' in source and 'facing-pages' not in source)
    d['mode']='invalid'; cfg.write_text(json.dumps(d)); bad=run(['build',str(pr)]); ck('invalid layout mode fails closed',bad.returncode!=0 and 'bilingual-layout mode' in (bad.stderr+bad.stdout))
  report={'audit_kind':'bilingual_profile','status':'pass' if all(x['status']=='pass' for x in results) else 'fail','checks':results}
  out=ROOT/'build/regression-output.json'; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2)); return 0 if report['status']=='pass' else 1
if __name__=='__main__': raise SystemExit(main())
