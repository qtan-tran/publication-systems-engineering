from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
UNIT_POLICY={'edited-collection':('required',True),'academic-monograph':('recommended',False),'scholarly-edition':('recommended',False),'critical-edition':('optional',False),'basic-book':('optional',False),'bilingual-edition':('optional',False),'drama':('discouraged',False),'poetry':('discouraged',False),'literary-fiction':('discouraged',False)}
CONTRIB_REQUIRED={'edited-collection','bilingual-edition','scholarly-edition','critical-edition'}
def run(args,expect=0,timeout=180):
 p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
 if p.returncode!=expect: raise AssertionError(f'{args}\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}')
 return p
def main():
 checks=[]
 m=json.loads((ROOT/'modules/publication-unit-metadata/module.json').read_text())
 checks.append(('module_dependency',m.get('depends_on')==['contributor-metadata'] and m.get('requires_capabilities')==['contributors'],str(m)))
 for pid,(status,default) in UNIT_POLICY.items():
  d=json.loads((ROOT/'profiles'/pid/'profile.json').read_text()); rule=d['module_policy']['publication-unit-metadata']
  checks.append((pid+'_unit_policy',rule=={'status':status,'default_enabled':default},str(rule)))
  cr=d['module_policy']['contributor-metadata']
  if pid in CONTRIB_REQUIRED: checks.append((pid+'_contributors_required',cr['status']=='required' and cr['default_enabled'] is True,str(cr)))
 with tempfile.TemporaryDirectory(prefix='pse-unit-') as td:
  parent=Path(td); run(CLI+['new',str(parent),'--non-interactive','--profile','edited-collection','--title','Unit Metadata Test','--author','Synthetic Editor','--language','en','--publication-year','2027','--slug','book'])
  pr=parent/'book'; main=(pr/'content/chapter-01.tex').read_text()
  checks.append(('generator_uses_unit_api','PSEDeclarePublicationUnit' in main and 'PSEPublicationUnitAbstract' in main and 'PSEOpenPublicationUnit' in main,'starter API'))
  run(CLI+['build',str(pr)],timeout=240)
  checks.append(('edited_collection_build',(pr/'build/book.pdf').is_file(),'PDF'))
 failed=[x for x in checks if not x[1]]
 for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
