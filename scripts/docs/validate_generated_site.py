#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
from urllib.parse import urlparse

CANON=re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)',re.I)
TITLE=re.compile(r'<title>\s*(.*?)\s*</title>',re.I|re.S)

def main():
 p=argparse.ArgumentParser(); p.add_argument('--site-dir',default='site'); p.add_argument('--site-url',required=True); a=p.parse_args()
 root=Path(a.site_dir).resolve(); base=a.site_url.rstrip('/')+'/'
 checks=[]
 html=sorted(root.rglob('*.html')) if root.is_dir() else []
 checks.append(('site_exists',root.is_dir()))
 checks.append(('html_exists',bool(html)))
 for f in html:
  text=f.read_text(encoding='utf-8',errors='replace')
  rel=f.relative_to(root).as_posix()
  t=TITLE.search(text); checks.append((f'title:{rel}',bool(t and t.group(1).strip())))
  c=CANON.search(text); checks.append((f'canonical:{rel}',bool(c and c.group(1).startswith(base))))
 sitemap=root/'sitemap.xml'; checks.append(('sitemap_exists',sitemap.is_file()))
 if sitemap.is_file():
  s=sitemap.read_text(encoding='utf-8',errors='replace'); checks.append(('sitemap_uses_site_url',base in s))
 robots=root/'robots.txt'
 if robots.exists(): checks.append(('robots_no_block_all','Disallow: /' not in robots.read_text(errors='replace')))
 failed=[n for n,ok in checks if not ok]
 for n,ok in checks: print(('PASS' if ok else 'FAIL'),n)
 print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
 return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
