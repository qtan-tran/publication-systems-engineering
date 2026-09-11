#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import yaml, sys
ROOT=Path(__file__).resolve().parents[2]
BASELINE=ROOT/'docs/documentation/STABLE-URLS-1.46.txt'
def nav_files(v):
 out=[]
 if isinstance(v,str): out.append(v)
 elif isinstance(v,list):
  for x in v: out += nav_files(x)
 elif isinstance(v,dict):
  for x in v.values(): out += nav_files(x)
 return out
def url_for(md):
 if md=='index.md': return '/'
 if md.endswith('/index.md'): return '/'+md[:-8]
 return '/'+md[:-3]+'/'
def main():
 cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
 current={url_for(x) for x in nav_files(cfg.get('nav',[]))}
 expected={x.strip() for x in BASELINE.read_text().splitlines() if x.strip() and not x.startswith('#')}
 missing=sorted(expected-current); dup=len(nav_files(cfg.get('nav',[])))!=len(set(nav_files(cfg.get('nav',[]))))
 print('PASS baseline_exists' if BASELINE.is_file() else 'FAIL baseline_exists')
 print(('PASS' if not missing else 'FAIL'),'published_urls_preserved',','.join(missing))
 print(('PASS' if not dup else 'FAIL'),'nav_targets_unique')
 print(f'current_urls: {len(current)} baseline_urls: {len(expected)}')
 return 1 if missing or dup or not BASELINE.is_file() else 0
if __name__=='__main__': raise SystemExit(main())
