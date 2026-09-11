from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
POLICY={
 'academic-monograph':('recommended',False),'basic-book':('optional',False),
 'bilingual-edition':('recommended',False),'critical-edition':('recommended',True),
 'drama':('recommended',False),'edited-collection':('optional',False),
 'literary-fiction':('optional',False),'poetry':('optional',False),
 'scholarly-edition':('recommended',True)}
def run(a,timeout=240,ok=True):
 p=subprocess.run(a,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
 if ok and p.returncode: raise AssertionError(f'{a}\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}')
 return p
def main():
 c=[]
 m=json.loads((ROOT/'modules/margin-objects/module.json').read_text()); sty=(ROOT/'modules/margin-objects/pse-module-margin-objects.sty').read_text(); core=(ROOT/'core/pse-core.sty').read_text()
 c.append(('registered','margin-objects' in json.loads((ROOT/'runtime/pse-runtime.json').read_text())['modules'],'runtime'))
 c.append(('types',all(x in m['capabilities'] for x in ['marginal-notes','side-captions','apparatus-anchors','locator-markers','running-side-objects']),'5 object classes'))
 c.append(('stable_id_api',r'\PSEDeclareMarginObject' in sty and 'Duplicate margin object id' in sty,'declare/duplicate guard'))
 c.append(('unknown_guard','Unknown margin object id' in sty,'render guard'))
 c.append(('fallback_contract',r'\PSEMarginObjectPresentationContractVersion}{1}' in core and r'\PSEMarginObjectMode}{fallback}' in core,'core v1 fallback'))
 c.append(('outer_margin_contract',r'\PSEUseOuterMarginObjects' in core and r'\marginpar' in core,'profile placement'))
 c.append(('semantic_no_geometry',r'\geometry{' not in sty and r'\newgeometry' not in sty,'module cannot resize grid'))
 for pid,want in POLICY.items():
  got=json.loads((ROOT/'profiles'/pid/'profile.json').read_text())['module_policy']['margin-objects']
  c.append((f'policy_{pid}',(got['status'],got['default_enabled'])==want,str(want)))
 for pid in ['critical-edition','scholarly-edition','bilingual-edition','academic-monograph','drama']:
  txt=(ROOT/'profiles'/pid/f'pse-profile-{pid}.sty').read_text()
  c.append((f'outer_{pid}',r'\PSEUseOuterMarginObjects' in txt,'fixed outer-margin presentation'))
 with tempfile.TemporaryDirectory(prefix='pse-margin-') as td:
  parent=Path(td); run(CLI+['new',str(parent),'--non-interactive','--profile','critical-edition','--title','Margin Test','--author','Synthetic Author','--language','en','--publication-year','2027','--slug','book'])
  main=parent/'book/main.tex'; s=main.read_text(); marker='\\end{document}'; s=s.replace(marker,'\\PSEMarginalNote{mn-test}{Synthetic marginal context.}\n'+marker); main.write_text(s)
  run(CLI+['build',str(parent/'book')]); c.append(('critical_margin_build',(parent/'book/build/book.pdf').is_file(),'PDF'))
 failed=[x for x in c if not x[1]]
 print('Margin objects regression')
 for n,ok,d in c: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(c)-len(failed)}/{len(c)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
