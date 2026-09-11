from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']

def run(args,expect=0,timeout=180):
 p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
 if p.returncode!=expect: raise AssertionError(f"{args}\nstdout={p.stdout[-4000:]}\nstderr={p.stderr[-4000:]}")
 return p

def main():
 c=[]
 sty=(ROOT/'modules/apparatus/pse-module-apparatus.sty').read_text()
 man=json.loads((ROOT/'modules/apparatus/module.json').read_text())
 streams=['textual','editorial','translation','commentary','source']
 c.append(('module_capability','multi-stream-apparatus' in man['capabilities'],'multi-stream capability'))
 c.append(('stream_entry_api',r'\PSEApparatusStreamEntry' in sty,'stream entry command'))
 c.append(('stream_range_api',r'\PSEApparatusStreamRangeEntry' in sty,'stream range command'))
 c.append(('presentation_label_api',r'\PSESetApparatusStreamPresentationLabel' in sty,'presentation labels separate'))
 c.append(('legacy_entry_kept',r'\PSEApparatusEntry' in sty,'legacy entry retained'))
 c.append(('legacy_range_kept',r'\PSEApparatusRangeEntry' in sty,'legacy range retained'))
 c.append(('five_streams',all(x in sty for x in streams),'five canonical streams'))
 expected={
  'academic-monograph':('optional',False),'basic-book':('discouraged',False),'bilingual-edition':('recommended',False),
  'critical-edition':('required',True),'drama':('recommended',False),'edited-collection':('optional',False),
  'literary-fiction':('discouraged',False),'poetry':('optional',False),'scholarly-edition':('required',True)}
 for pid,(status,default) in expected.items():
  d=json.loads((ROOT/'profiles'/pid/'profile.json').read_text()); r=d['module_policy']['apparatus']
  c.append((f'policy_{pid}',r=={'status':status,'default_enabled':default},str(r)))
 with tempfile.TemporaryDirectory(prefix='pse-apparatus-') as td:
  parent=Path(td)
  run(CLI+['new',str(parent),'--non-interactive','--profile','critical-edition','--title','Synthetic Multi Stream Edition','--author','PSE Regression','--language','en','--publication-year','2027','--slug','edition'])
  project=parent/'edition'
  src=(project/'content/apparatus.tex').read_text()
  c.append(('generator_textual',r'\PSEApparatusStreamEntry{textual}' in src,'textual stream example'))
  c.append(('generator_editorial_range',r'\PSEApparatusStreamRangeEntry{editorial}' in src,'editorial range example'))
  c.append(('generator_source',r'\PSEApparatusStreamEntry{source}' in src,'source stream example'))
  run(CLI+['build',str(project)])
  qa=json.loads(run(CLI+['check',str(project)]).stdout); sm=qa.get('metrics',{}).get('scholarly',{}).get('apparatus_streams',{})
  c.append(('qa_no_errors',qa.get('summary',{}).get('error',0)==0,'generated critical has no QA errors'))
  c.append(('stream_inventory',sm.get('used')==['textual','editorial','source'],str(sm.get('used'))))
  c.append(('stream_counts',sm.get('counts',{}).get('textual')==1 and sm.get('counts',{}).get('editorial')==1 and sm.get('counts',{}).get('source')==1,str(sm.get('counts'))))
  bad=project/'content/apparatus.tex'; bad.write_text(src.replace('{textual}{1.1}','{witness}{1.1}'))
  p=subprocess.run(CLI+['check',str(project)],cwd=ROOT,env=ENV,text=True,capture_output=True)
  q=json.loads(p.stdout); codes={x['code'] for x in q['findings']}
  c.append(('unknown_stream_rejected',p.returncode==1 and 'unknown_apparatus_stream' in codes,str(codes)))
 # semantic parser ownership
 parser=(ROOT/'tools/pse_cli/semantic_parser.py').read_text()
 c.append(('parser_entry_arity','"PSEApparatusStreamEntry": 4' in parser,'entry arity'))
 c.append(('parser_range_arity','"PSEApparatusStreamRangeEntry": 5' in parser,'range arity'))
 failed=[x for x in c if not x[1]]
 print('Multi-stream apparatus regression')
 for n,ok,d in c: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(c)-len(failed)}/{len(c)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
