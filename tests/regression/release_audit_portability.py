from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
TOOLS=ROOT/'tools'
sys.path.insert(0,str(TOOLS))
from pse_cli.release_contract import validate_release_audit_record, validate_release_audit_index
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(TOOLS)+os.pathsep+str(ROOT); ENV['PYTHONDONTWRITEBYTECODE']='1'
FIX=ROOT/'tests/fixtures/releases'
checks=[]
def add(name,ok,detail=''): checks.append({'name':name,'pass':bool(ok),'detail':str(detail)})
def run(*args): return subprocess.run([sys.executable,'-m','pse_cli.cli',*map(str,args)],cwd=ROOT,env=ENV,text=True,capture_output=True)
def payload(proc):
    try:return json.loads(proc.stdout)
    except:return {}

# Individual fingerprint stability after relocation.
for schema in ('schema-0.1','schema-0.2'):
    base=run('audit-release',FIX/schema); a=payload(base)
    with tempfile.TemporaryDirectory(prefix='pse-moved-release-') as td:
        moved=Path(td)/('renamed-'+schema)
        shutil.copytree(FIX/schema,moved)
        proc=run('audit-release',moved); b=payload(proc)
        add(schema+'_audit_current_schema',a.get('schema_version')=='0.2' and b.get('schema_version')=='0.2')
        add(schema+'_record_contract',not validate_release_audit_record(a),validate_release_audit_record(a))
        add(schema+'_fingerprint_stable',a.get('release_fingerprint')==b.get('release_fingerprint'),(a.get('release_fingerprint'),b.get('release_fingerprint')))
        add(schema+'_path_changes_only',a.get('source_release_dir')!=b.get('source_release_dir'))

# Batch collection stability after relocation.
with tempfile.TemporaryDirectory(prefix='pse-audit-index-') as td:
    td=Path(td); c1=td/'collection-a'; c1.mkdir()
    shutil.copytree(FIX/'schema-0.1',c1/'legacy')
    shutil.copytree(FIX/'schema-0.2',c1/'current')
    out1=td/'index-a.json'; p1=run('audit-index',c1,'--output',out1); i1=payload(p1)
    c2=td/'elsewhere'/'collection-b'; c2.parent.mkdir(); shutil.copytree(c1,c2)
    out2=td/'index-b.json'; p2=run('audit-index',c2,'--output',out2); i2=payload(p2)
    add('batch_audit_pass',p1.returncode==0 and p2.returncode==0 and i1.get('batch_status')=='pass')
    add('batch_contract',not validate_release_audit_index(i1),validate_release_audit_index(i1))
    add('batch_count_two',i1.get('release_count')==2)
    add('batch_fingerprint_stable',i1.get('batch_fingerprint')==i2.get('batch_fingerprint'))
    fps1=sorted(e['release_fingerprint'] for e in i1.get('entries',[])); fps2=sorted(e['release_fingerprint'] for e in i2.get('entries',[]))
    add('entry_fingerprints_stable',fps1==fps2)
    add('collection_paths_informational',i1.get('collection_dir')!=i2.get('collection_dir'))
    add('external_index_written',out1.is_file() and out2.is_file())
    blocked=c1/'legacy'/'batch-index.json'; pb=run('audit-index',c1,'--output',blocked)
    add('index_inside_release_blocked',pb.returncode!=0 and not blocked.exists(),pb.stdout+pb.stderr)
    # Tamper one copied PDF: index must fail, not repair.
    bad=c2/'current'/'current-release.pdf'; before=bad.read_bytes(); bad.write_bytes(before+b'\n% portable-audit-tamper\n')
    pout=td/'bad-index.json'; pf=run('audit-index',c2,'--output',pout); fi=payload(pf)
    add('tampered_batch_fails',pf.returncode!=0 and fi.get('batch_status')=='fail',pf.stdout+pf.stderr)
    add('tampered_file_preserved',bad.read_bytes().endswith(b'% portable-audit-tamper\n'))

add('audit_record_02_schema_installed',(ROOT/'schema/release-audit-record-0.2.schema.json').is_file())
add('audit_index_schema_installed',(ROOT/'schema/release-audit-index-0.1.schema.json').is_file())
result={'suite':'release_audit_portability','passed':all(c['pass'] for c in checks),'checks':checks}
print(json.dumps(result,indent=2)); raise SystemExit(0 if result['passed'] else 1)
