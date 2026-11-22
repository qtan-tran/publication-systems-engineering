from pathlib import Path
import re, yaml
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'wiki/workflows'; Q=ROOT/'wiki/quality-release'; CLI=(ROOT/'tools/pse_cli/cli.py').read_text()
checks=[]
def add(name,ok,detail=''): checks.append((name,bool(ok),detail))
workflow_pages=['index.md','edit-build-check.md','clean-build.md','human-review.md','recipient-proofs.md','publication-release.md','after-release.md']
quality_pages=['index.md','quality-model.md','artifact-boundaries.md','output-inspection.md','release-verification.md','audit-evidence.md','historical-releases.md','release-checklist.md']
for f in workflow_pages: add('workflow_page_'+f,(W/f).is_file(),f)
for f in quality_pages: add('quality_page_'+f,(Q/f).is_file(),f)
whole='\n'.join(p.read_text() for p in [*(W/f for f in workflow_pages),*(Q/f for f in quality_pages)])
# Bind public handbook commands to the actual CLI parser surface.
commands=['build','check','clean','proof','release','verify-release','inspect-output','contracts','release-migration','audit-release','audit-index','verify-audit-record','verify-audit-index','export-audit-evidence']
for cmd in commands:
    add('cli_command_'+cmd, f'add_parser("{cmd}"' in CLI or f'("{cmd}",' in CLI, cmd)
    add('handbook_command_'+cmd, f'pse {cmd}' in whole, cmd)
flags=['--human','--recipient','--email','--proof-id','--acknowledge-review','--source-date-epoch','--expected-language','--output','--release-dir','--collection-dir']
for flag in flags: add('cli_flag_'+flag,flag in CLI,flag)
# Bind lifecycle artifact paths and core distinction.
art=(Q/'artifact-boundaries.md').read_text()
for token in ['`build/book.pdf`','`build/proofs/`','`release/<release-id>/`']:
    add('artifact_'+re.sub(r'\W+','_',token),token in art,token)
add('three_artifacts',all(x in art for x in ['Working PDF','Recipient proof','Publication release']))
add('release_not_proof','not** “the proof without a watermark,”' in art or 'not** “the proof without a watermark”' in art)
# QA severity taxonomy.
qm=(Q/'quality-model.md').read_text()
for level in ['`error`','`warning`','`review`','`info`']: add('severity_'+level,level in qm,level)
# Output inspection limits and current release binding.
oi=(Q/'output-inspection.md').read_text()
for term in ['tagged-PDF','reading order','PDF/UA','WCAG','archival conformance','legal accessibility compliance']:
    add('inspection_boundary_'+re.sub(r'\W+','_',term),term in oi,term)
add('inspection_schema_binding','schema `0.2`' in oi and '`output-inspection.json`' in oi and 'SHA-256' in oi)
# Release contract and verification guardrails.
rel=(W/'publication-release.md').read_text(); ver=(Q/'release-verification.md').read_text()
for token in ['schema `0.2`','`output-inspection.json`','`SHA256SUMS.txt`','mandatory attribution evidence']:
    add('release_contract_'+re.sub(r'\W+','_',token),token in rel,token)
add('verify_immediately','pse verify-release release/<release-id>' in rel)
add('no_hash_refresh_workaround','manually refreshing hashes' in ver)
# Audit evidence remains detached and evidence-only.
aud=(Q/'audit-evidence.md').read_text()
for cmd in ['pse audit-release','pse verify-audit-record','pse audit-index','pse verify-audit-index','pse export-audit-evidence']:
    add('audit_'+re.sub(r'\W+','_',cmd),cmd in aud,cmd)
add('audit_detached','outside the audited release' in aud)
add('audit_no_pdf','does not contain publication PDFs' in aud)
for term in ['digital signature','PKI assertion','trusted timestamp','notarization service']:
    add('audit_trust_boundary_'+re.sub(r'\W+','_',term),term in aud,term)
# Historical evidence must not be rewritten or invented.
hist=(Q/'historical-releases.md').read_text()
for token in ['schema `0.1`','verification-only','pse release-migration','does not infer missing historical inspection evidence','new release from source']:
    add('historical_'+re.sub(r'\W+','_',token),token in hist,token)
# Workflows must preserve source/generated distinction and human review.
ew=(W/'edit-build-check.md').read_text(); hr=(W/'human-review.md').read_text(); proof=(W/'recipient-proofs.md').read_text()
add('canonical_source_boundary','canonical source' in ew and 'Do not correct a typo by editing a generated PDF' in ew)
add('human_review_not_zero_error','zero-error machine report is not a visual proofread' in hr)
add('ack_review_guard','must not be used to bypass `error` findings' in hr)
add('proof_watermark_limit','does not claim it is unremovable DRM' in proof)
add('proof_personal_data','personal data' in proof and 'private storage' in proof)
# Navigation exposes the full handbook.
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text()); nav=str(cfg.get('nav',[]))
for f in workflow_pages: add('nav_workflow_'+f,f'workflows/{f}' in nav,f)
for f in quality_pages: add('nav_quality_'+f,f'quality-release/{f}' in nav,f)
# No stale stub wording remains in either section.
add('no_stale_stub','scheduled after' not in whole.lower() and 'this section will document' not in whole.lower() and 'this section will explain' not in whole.lower())
failed=[x for x in checks if not x[1]]
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
raise SystemExit(1 if failed else 0)
