from __future__ import annotations
import os, re, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']
ROLES=(
 'PSETypographyBodyRole','PSETypographyDisplayRole','PSETypographyChapterTitleRole',
 'PSETypographySectionHeadingRole','PSETypographySubsectionHeadingRole',
 'PSETypographyMetadataLabelRole','PSETypographyMetadataValueRole',
 'PSETypographyRunningHeadRole','PSETypographyCaptionRole','PSETypographyApparatusRole')

def run(args,timeout=240):
 p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
 if p.returncode: raise AssertionError(f"{args}\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}")
 return p

def main():
 checks=[]
 core=(ROOT/'core/pse-core.sty').read_text()
 checks.append(('contract_version',r'\newcommand{\PSETypographyRoleContractVersion}{1}' in core,'v1'))
 for role in ROLES:
  checks.append((f'core_owns_{role}',fr'\newcommand{{\{role}}}' in core,role))
 for sty in sorted((ROOT/'profiles').glob('*/pse-profile-*.sty')):
  text=sty.read_text(); pid=sty.parent.name
  checks.append((f'{pid}_uses_contract',r'\renewcommand{\PSETypographyChapterTitleRole}' in text and r'\renewcommand{\PSETypographyRunningHeadRole}' in text,'profile overrides'))
 # Semantic modules may consume roles but cannot redefine them.
 bad=[]
 for sty in sorted((ROOT/'modules').glob('*/*.sty')):
  text=sty.read_text()
  for role in ROLES:
   if re.search(r'\\(?:newcommand|renewcommand|providecommand)\{\\'+re.escape(role)+r'\}',text): bad.append(f'{sty.relative_to(ROOT)}:{role}')
 checks.append(('modules_do_not_own_roles',not bad,str(bad)))
 apparatus=(ROOT/'modules/apparatus/pse-module-apparatus.sty').read_text()
 checks.append(('apparatus_consumes_role',r'\PSETypographyApparatusRole' in apparatus,'apparatus role consumed'))
 checks.append(('technical_contract',(ROOT/'docs/architecture/TYPOGRAPHY-ROLE-SYSTEM.md').is_file(),'doc present'))
 checks.append(('wiki_stub',(ROOT/'wiki/customization/typography.md').is_file(),'stub present'))
 # Local title override must compile without changing profile or manuscript semantics.
 with tempfile.TemporaryDirectory(prefix='pse-type-role-') as td:
  parent=Path(td)
  run(CLI+['new',str(parent),'--non-interactive','--profile','basic-book','--title','Role Test','--author','Synthetic Author','--language','en','--publication-year','2027','--slug','book'])
  project=parent/'book'
  local=project/'config/pse-local.tex'
  local.write_text(r'\renewcommand{\PSETypographySectionHeadingRole}{\rmfamily\normalsize\bfseries\upshape}'+'\n')
  run(CLI+['build',str(project)])
  checks.append(('title_local_override_builds',(project/'build/book.pdf').is_file(),'PDF produced'))
 failed=[x for x in checks if not x[1]]
 print('Typography role regression')
 for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
