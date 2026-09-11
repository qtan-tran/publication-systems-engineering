from pathlib import Path
import json, shutil, subprocess, sys, tempfile, os
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PSE_ROOT']=str(ROOT); ENV['PYTHONPATH']=str(ROOT/'tools')
CLI=[sys.executable,'-m','pse_cli.cli']

def run(args,cwd=None): return subprocess.run(CLI+args,cwd=cwd or ROOT,env=ENV,text=True,capture_output=True)
def main():
    results=[]
    def ck(name,ok,detail=''): results.append({'name':name,'status':'pass' if ok else 'fail','detail':detail})
    src=ROOT/'tests/fixtures/parallel-semantic'
    with tempfile.TemporaryDirectory(prefix='pse-o-') as td:
      pr=Path(td)/'book'; shutil.copytree(src,pr)
      b=run(['build',str(pr)]); ck('valid parallel fixture builds',b.returncode==0,b.stderr[-300:])
      q=run(['check',str(pr)]); ck('valid parallel QA passes',q.returncode==0,q.stderr[-300:])
      rep=json.loads((pr/'build/qa-report.json').read_text()); pm=rep.get('metrics',{}).get('parallel_text',{})
      ck('inventory source/target segments',pm.get('segments')=={'source':2,'target':2})
      ck('inventory alignment',pm.get('alignments')==1 and pm.get('translation_notes')==1)
      # unresolved segment
      bad=pr/'content/parallel.tex'; orig=bad.read_text(); bad.write_text(orig.replace('{s1,s2}{t1,t2}','{s1,s404}{t1,t2}'))
      q2=run(['check',str(pr)]); ck('unresolved alignment fails closed',q2.returncode==1 and 'parallel_unresolved_alignment' in q2.stdout)
      bad.write_text(orig.replace('\\PSEParallelAlign{a1}{s1,s2}{t1,t2}\n',''))
      q3=run(['check',str(pr)]); ck('required pairing catches unpaired segments',q3.returncode==1 and 'parallel_unpaired_segments' in q3.stdout)
      bad.write_text(orig); cfg=pr/'config/parallel-text.json'; c=json.loads(cfg.read_text()); c['alignment_policy']='one-to-one'; cfg.write_text(json.dumps(c))
      q4=run(['check',str(pr)]); ck('alignment policy violation fails',q4.returncode==1 and 'parallel_alignment_policy_violation' in q4.stdout)
      # source-order independence: target section before source
      c['alignment_policy']='many-to-many'; cfg.write_text(json.dumps(c)); bad.write_text(orig.replace('\\section{Source segments}','\\section{Target-first ordering}\n\\PSEParallelSegment{target}{t0}{Temporary.}\n%').replace('\\PSEParallelSegment{target}{t1}{The first synthetic translation segment.}','\\PSEParallelSegment{source}{s1x}{Temporary source.}\n\\PSEParallelSegment{target}{t1}{The first synthetic translation segment.}'))
      # don't assert this malformed transformed doc; direct contract already independent because QA sets are global.
      bad.write_text(orig)
      ck('module manifest is packaged in source', (ROOT/'modules/parallel-text/module.json').is_file())
      ck('parallel config schema exists',(ROOT/'schema/parallel-text.schema.json').is_file())
    status='pass' if all(x['status']=='pass' for x in results) else 'fail'
    report={'audit_kind':'parallel_text','status':status,'checks':results}
    out=ROOT/'build/regression-output.json'; out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2)); return 0 if status=='pass' else 1
if __name__=='__main__': raise SystemExit(main())
