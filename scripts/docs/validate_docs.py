#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, sys, yaml
ROOT=Path(__file__).resolve().parents[2]; WIKI=ROOT/'wiki'
LINK=re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
IMG=re.compile(r'!\[[^\]]*\]\(([^)]+)\)')

def nav_files(nav):
 out=[]
 if isinstance(nav,str): out.append(nav)
 elif isinstance(nav,list):
  for x in nav: out.extend(nav_files(x))
 elif isinstance(nav,dict):
  for x in nav.values(): out.extend(nav_files(x))
 return out

def local_target(source:Path, raw:str):
 raw=raw.split('#',1)[0].strip()
 if not raw or raw.startswith(('http://','https://','mailto:','#')): return None
 return (source.parent/raw).resolve()

def main():
 cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
 checks=[]
 nav=set(nav_files(cfg.get('nav',[])))
 for rel in nav: checks.append((f'nav:{rel}',(WIKI/rel).is_file()))
 md_files={p.relative_to(WIKI).as_posix() for p in WIKI.rglob('*.md')}
 exempt={'DOCUMENTATION-STATUS.md','404.md'}
 for rel in sorted(md_files-nav-exempt): checks.append((f'orphan:{rel}',False))
 for p in WIKI.rglob('*.md'):
  text=p.read_text(errors='replace')
  for raw in LINK.findall(text)+IMG.findall(text):
   t=local_target(p,raw)
   if t is not None: checks.append((f'link:{p.relative_to(WIKI)}->{raw}',t.exists()))
 private=''.join(map(chr,[99,111,110,102,105,100,101,110,116,105,97,108]))+'/'
 public='\n'.join(p.read_text(errors='replace') for p in WIKI.rglob('*.md'))
 checks.append(('private-boundary',private not in public))
 checks.append(('material-theme',cfg.get('theme',{}).get('name')=='material'))
 checks.append(('search-plugin','search' in cfg.get('plugins',[])))
 checks.append(('no-static-site-url','site_url' not in cfg))
 failed=[n for n,ok in checks if not ok]
 for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
 print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
