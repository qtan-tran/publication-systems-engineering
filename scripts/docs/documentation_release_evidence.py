#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, subprocess
from pathlib import Path
from urllib.parse import urljoin

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser(); p.add_argument('--site-dir',default='site'); p.add_argument('--site-url',required=True); p.add_argument('--output',default='build/documentation-release-evidence.json'); p.add_argument('--version',required=True); p.add_argument('--source-revision',default='') ; a=p.parse_args()
 root=Path(a.site_dir).resolve(); out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
 files=[]
 for f in sorted(x for x in root.rglob('*') if x.is_file()):
  files.append({'path':f.relative_to(root).as_posix(),'sha256':sha(f),'bytes':f.stat().st_size})
 revision=a.source_revision or os.environ.get('GITHUB_SHA','') or 'unbound-local-source'
 payload={'schema_version':'0.1','artifact_kind':'pse-documentation-release-evidence','pse_version':a.version,'source_revision':revision,'site_url':a.site_url.rstrip('/')+'/', 'file_count':len(files),'files':files,'claims':{'generated_site_integrity':'sha256-file-inventory','live_deployment_verified':False,'external_timestamp':False,'signature_or_pki':False}}
 out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(out)
 return 0
if __name__=='__main__': raise SystemExit(main())
