from pathlib import Path
import re, yaml
ROOT=Path(__file__).resolve().parents[2]
def main():
 checks=[]; cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text()); checks.append(('docs_dir',cfg.get('docs_dir')=='wiki',str(cfg.get('docs_dir'))))
 files=['wiki/index.md','wiki/getting-started/what-is-pse.md','wiki/how-pse-works/architecture-overview.md','wiki/profiles/index.md','wiki/book-features/index.md','wiki/DOCUMENTATION-STATUS.md','.github/workflows/docs-pages.yml','requirements/docs.txt','wiki/assets/stylesheets/pse.css','scripts/docs/validate_docs.py','scripts/docs/prepare_mkdocs_config.py','docs/documentation/DOCUMENTATION-PLATFORM.md','wiki/404.md']
 for f in files: checks.append(('exists_'+f,(ROOT/f).is_file(),f))
 nav=[]
 def walk(x):
  if isinstance(x,str): nav.append(x)
  elif isinstance(x,list):
   for y in x: walk(y)
  elif isinstance(x,dict):
   for y in x.values(): walk(y)
 walk(cfg.get('nav',[]))
 for f in nav: checks.append(('nav_'+f,(ROOT/'wiki'/f).is_file(),f))
 public='\n'.join(p.read_text(errors='replace') for p in (ROOT/'wiki').rglob('*.md'))
 private_root=''.join(chr(x) for x in (99,111,110,102,105,100,101,110,116,105,97,108))+'/'
 checks.append(('no_private_root_reference',private_root not in public,'wiki sanitised'))
 failed=[x for x in checks if not x[1]]
 for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
 print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
