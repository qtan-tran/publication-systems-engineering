#!/usr/bin/env python3
"""Create an ephemeral MkDocs config with the deployment URL bound explicitly."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--site-url', required=True)
    p.add_argument('--output', default='build/mkdocs.deployment.yml')
    args = p.parse_args()
    url = args.site_url.strip()
    if not (url.startswith('https://') or url.startswith('http://')):
        raise SystemExit('site URL must be absolute http(s) URL')
    if not url.endswith('/'):
        url += '/'
    cfg = yaml.safe_load((ROOT/'mkdocs.yml').read_text(encoding='utf-8'))
    cfg['site_url'] = url
    out = ROOT/args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding='utf-8')
    print(out.relative_to(ROOT))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
