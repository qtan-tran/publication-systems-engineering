from __future__ import annotations
import os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
EXPECTED={
 'academic-monograph':('19mm','21mm','recommended'), 'basic-book':('18mm','22mm','optional'),
 'bilingual-edition':('18mm','20mm','recommended'), 'critical-edition':('19mm','24mm','required'),
 'drama':('18mm','22mm','recommended'), 'edited-collection':('19mm','21mm','optional'),
 'literary-fiction':('18mm','22mm','optional'), 'poetry':('20mm','22mm','optional'),
 'scholarly-edition':('19mm','23mm','required')}
def run(a,timeout=240):
 p=subprocess.run(a,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
 if p.returncode: raise AssertionError(f'{a}\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}')
 return p
def main():
 c=[]; core=(ROOT/'core/pse-core.sty').read_text()
 c.append(('contract_v1',r'\newcommand{\PSEPageGridContractVersion}{1}' in core,'v1'))
 for token in ('PSEConfigurePageGrid','PSEApplyPageGrid','PSEGridInnerGutter','PSEGridOuterMarginZone','PSEGridPrimaryTextMeasure','PSEGridHeaderHeight','PSEGridFooterSeparation','PSEGridApparatusZone'):
  c.append((f'core_{token}',('\\'+token) in core,token))
 c.append(('core_apparatus_zero',r'\newcommand\pse@gridapparatus{0mm}' in core,'0mm baseline'))
 for pid,(inner,outer,policy) in EXPECTED.items():
  text=(ROOT/'profiles'/pid/f'pse-profile-{pid}.sty').read_text()
  c.append((f'{pid}_shared_grid',r'\PSEConfigurePageGrid' in text and r'\PSEApplyPageGrid' in text and r'\geometry{' not in text,f'{inner}/{outer}'))
 doc=(ROOT/'docs/architecture/ASYMMETRIC-SCHOLARLY-GRID.md').read_text()
 c.append(('policy_matrix',all(f'| {pid.replace("-"," ").title()} | {pol} |' in doc for pid,(_,_,pol) in EXPECTED.items()),'9 profiles'))
 c.append(('wiki_stub',(ROOT/'wiki/customization/page-layout.md').is_file(),'page layout'))
 c.append(('no_dynamic_semantic_geometry',all(r'\geometry{' not in p.read_text() for p in (ROOT/'modules').glob('*/*.sty')),'modules do not own geometry'))
 with tempfile.TemporaryDirectory(prefix='pse-grid-') as td:
  parent=Path(td); run(CLI+['new',str(parent),'--non-interactive','--profile','critical-edition','--title','Grid Test','--author','Synthetic Author','--language','en','--publication-year','2027','--slug','book'])
  run(CLI+['build',str(parent/'book')]); c.append(('critical_build',(parent/'book/build/book.pdf').is_file(),'PDF'))
 failed=[x for x in c if not x[1]]
 print('Asymmetric grid regression')
 for n,ok,d in c: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(c)-len(failed)}/{len(c)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
