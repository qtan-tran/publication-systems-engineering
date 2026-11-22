from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/'tools'
sys.path.insert(0,str(TOOLS))
from pse_cli.release_contract import sha256_file, validate_audit_evidence_bundle_manifest
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(TOOLS)+os.pathsep+str(ROOT); ENV['PYTHONDONTWRITEBYTECODE']='1'
FIX=ROOT/'tests/fixtures/releases'
checks=[]
def add(name,ok,detail=''): checks.append({'name':name,'pass':bool(ok),'detail':str(detail)})
def run(*args): return subprocess.run([sys.executable,'-m','pse_cli.cli',*map(str,args)],cwd=ROOT,env=ENV,text=True,capture_output=True)
def payload(proc):
    try:return json.loads(proc.stdout)
    except:return {}

with tempfile.TemporaryDirectory(prefix='pse-audit-evidence-') as td:
    td=Path(td); collection=td/'collection'; collection.mkdir()
    shutil.copytree(FIX/'schema-0.1',collection/'legacy')
    shutil.copytree(FIX/'schema-0.2',collection/'current')
    record=td/'current-record.json'; index=td/'index.json'
    ar=run('audit-release',collection/'current','--output',record); ai=run('audit-index',collection,'--output',index)
    add('audit_sources_created',ar.returncode==0 and ai.returncode==0 and record.is_file() and index.is_file(),ar.stdout+ar.stderr+ai.stdout+ai.stderr)

    vr=run('verify-audit-record',record); vri=payload(vr)
    add('record_detached_pass',vr.returncode==0 and vri.get('status')=='pass' and vri.get('source_binding')=='not-requested',vr.stdout+vr.stderr)
    vrb=run('verify-audit-record',record,'--release-dir',collection/'current'); vrbp=payload(vrb)
    add('record_bound_pass',vrb.returncode==0 and vrbp.get('source_binding')=='match',vrb.stdout+vrb.stderr)

    vi=run('verify-audit-index',index); vip=payload(vi)
    add('index_detached_pass',vi.returncode==0 and vip.get('status')=='pass',vi.stdout+vi.stderr)
    vib=run('verify-audit-index',index,'--collection-dir',collection); vibp=payload(vib)
    add('index_bound_pass',vib.returncode==0 and vibp.get('source_binding')=='match',vib.stdout+vib.stderr)

    moved=td/'moved'/'collection'; moved.parent.mkdir(); shutil.copytree(collection,moved)
    moved_record=run('verify-audit-record',record,'--release-dir',moved/'current'); mrp=payload(moved_record)
    moved_index=run('verify-audit-index',index,'--collection-dir',moved); mip=payload(moved_index)
    add('record_relocation_safe',moved_record.returncode==0 and mrp.get('source_binding')=='match',moved_record.stdout+moved_record.stderr)
    add('index_relocation_safe',moved_index.returncode==0 and mip.get('source_binding')=='match',moved_index.stdout+moved_index.stderr)

    # Source tamper: detached evidence remains internally valid, source-binding verification fails.
    pdf=moved/'current'/'current-release.pdf'; pdf.write_bytes(pdf.read_bytes()+b'\n% audit-source-tamper\n')
    detached_after=run('verify-audit-record',record); bound_after=run('verify-audit-record',record,'--release-dir',moved/'current')
    add('detached_record_survives_source_tamper',detached_after.returncode==0,payload(detached_after))
    add('bound_record_detects_source_tamper',bound_after.returncode!=0 and payload(bound_after).get('source_binding')=='mismatch',bound_after.stdout+bound_after.stderr)

    # Evidence tamper: portable fingerprint contract catches it.
    tampered=td/'tampered-record.json'; rp=json.loads(record.read_text(encoding='utf-8')); rp['release_fingerprint_inputs']['pdf_sha256']='0'*64
    tampered.write_text(json.dumps(rp,indent=2)+'\n',encoding='utf-8')
    tv=run('verify-audit-record',tampered); add('tampered_record_rejected',tv.returncode!=0 and payload(tv).get('status')=='fail',tv.stdout+tv.stderr)

    z1=td/'bundle-a.zip'; z2=td/'bundle-b.zip'
    e1=run('export-audit-evidence',z1,record,index); e2=run('export-audit-evidence',z2,index,record)
    add('deterministic_export_commands_pass',e1.returncode==0 and e2.returncode==0,e1.stdout+e1.stderr+e2.stdout+e2.stderr)
    add('deterministic_zip_bytes',z1.read_bytes()==z2.read_bytes(),(sha256_file(z1),sha256_file(z2)))
    with zipfile.ZipFile(z1) as zf:
        names=zf.namelist(); infos=zf.infolist(); manifest=json.loads(zf.read('audit-evidence-bundle-manifest.json'))
        add('bundle_contents_evidence_only',set(names)=={'audit-evidence-bundle-manifest.json',record.name,index.name},names)
        add('bundle_fixed_timestamps',all(info.date_time==(1980,1,1,0,0,0) for info in infos),[i.date_time for i in infos])
        add('bundle_manifest_contract',not validate_audit_evidence_bundle_manifest(manifest),validate_audit_evidence_bundle_manifest(manifest))
        add('bundle_declares_no_release_artifacts',manifest.get('contains_publication_release_artifacts') is False)

add('bundle_schema_installed',(ROOT/'schema/audit-evidence-bundle-manifest-0.1.schema.json').is_file())
result={'suite':'audit_evidence_verification','passed':all(c['pass'] for c in checks),'checks':checks}
print(json.dumps(result,indent=2)); raise SystemExit(0 if result['passed'] else 1)
