from __future__ import annotations
import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; checks=[]
def add(n,ok,d=''): checks.append((n,bool(ok),d))
add('contract',(ROOT/'docs/documentation/DOCUMENTATION-RELEASE-ENGINEERING.md').is_file())
add('mirror_decision',(ROOT/'docs/documentation/GITHUB-WIKI-MIRROR-DECISION.md').is_file())
add('evidence_schema',(ROOT/'schema/documentation-release-evidence-0.1.schema.json').is_file())
for s in ['scripts/docs/validate_generated_site.py','scripts/docs/documentation_release_evidence.py'] : add('script:'+s,(ROOT/s).is_file())
wf=(ROOT/'.github/workflows/docs-pages.yml').read_text()
for token in ['Validate generated documentation','Create documentation release evidence','documentation-release-evidence','validate_generated_site.py','documentation_release_evidence.py'] : add('workflow:'+token,token in wf)
contract=(ROOT/'docs/documentation/DOCUMENTATION-RELEASE-ENGINEERING.md').read_text()
for token in ['/wiki','schema `0.1`','SHA-256','not a digital signature','does **not** enable a GitHub Wiki mirror'] : add('contract:'+token,token in contract)
# Synthetic generated-site validation/evidence without requiring MkDocs locally.
with tempfile.TemporaryDirectory() as td:
 d=Path(td); (d/'guide').mkdir(); base='https://docs.example.test/pse/'
 (d/'index.html').write_text(f'<html><head><title>Home</title><link rel="canonical" href="{base}"></head></html>')
 (d/'guide/index.html').write_text(f'<html><head><title>Guide</title><link rel="canonical" href="{base}guide/"></head></html>')
 (d/'sitemap.xml').write_text(f'<urlset><url><loc>{base}</loc></url></urlset>')
 v=subprocess.run([sys.executable,str(ROOT/'scripts/docs/validate_generated_site.py'),'--site-dir',str(d),'--site-url',base],capture_output=True,text=True); add('synthetic_site_validation',v.returncode==0,v.stdout[-300:])
 out=d/'evidence.json'; e=subprocess.run([sys.executable,str(ROOT/'scripts/docs/documentation_release_evidence.py'),'--site-dir',str(d),'--site-url',base,'--version','1.47.0-alpha','--source-revision','deadbeef','--output',str(out)],capture_output=True,text=True); add('evidence_generated',e.returncode==0 and out.is_file(),e.stderr)
 if out.is_file():
  j=json.loads(out.read_text()); add('evidence_contract',j.get('schema_version')=='0.1' and j.get('source_revision')=='deadbeef' and j.get('file_count')>=3 and j['claims']['live_deployment_verified'] is False)
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
failed=[x for x in checks if not x[1]]; print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass'); raise SystemExit(1 if failed else 0)
