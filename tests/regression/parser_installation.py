from __future__ import annotations
import json, os, subprocess, sys, tempfile, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
checks=[]
def ck(name,ok,detail=''): checks.append({'name':name,'pass':bool(ok),'detail':detail})

def run(cmd,**kwargs):
    return subprocess.run(cmd,text=True,capture_output=True,check=False,**kwargs)

with tempfile.TemporaryDirectory(prefix='pse-r-wheel-') as td:
    td=Path(td); wh=td/'wheel'; wh.mkdir(); target=td/'target'; target.mkdir()
    proc=run([sys.executable,'-m','pip','wheel','--no-build-isolation','--no-deps','-w',str(wh),str(ROOT)],cwd=td,timeout=240)
    wheels=list(wh.glob('*.whl'))
    ck('wheel_build',proc.returncode==0 and len(wheels)==1,(proc.stdout+'\n'+proc.stderr)[-1000:])
    if wheels:
        with zipfile.ZipFile(wheels[0]) as z:
            names=set(z.namelist())
        ck('wheel_contains_parser',any(n.endswith('pse_cli/semantic_parser.py') for n in names))
        ck('wheel_contains_ir_schema',any(n.endswith('schema/semantic-ir.schema.json') for n in names))
        ck('wheel_contains_attribution_asset',any(n.endswith('core/pse-attribution-banner.png') for n in names))
        proc=run([sys.executable,'-m','pip','install','--no-deps','--target',str(target),str(wheels[0])],cwd=td,timeout=180)
        ck('wheel_install',proc.returncode==0,(proc.stdout+'\n'+proc.stderr)[-800:])
        env=os.environ.copy(); env['PYTHONPATH']=str(target)
        code='''from pse_cli.semantic_parser import parse_text\nn,e=parse_text("\\\\PSEStageDirection{nested {installed}}","installed.tex")\nassert not e and n[0].args[0]=="nested {installed}" and n[0].loc.line==1\nprint("installed-parser-ok")'''
        proc=run([sys.executable,'-c',code],cwd=td,env=env,timeout=60)
        ck('installed_parser_runtime',proc.returncode==0 and 'installed-parser-ok' in proc.stdout,(proc.stdout+'\n'+proc.stderr)[-800:])

payload={'audit_kind':'parser_installation','checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks)}
print(json.dumps(payload,indent=2))
raise SystemExit(0 if checks and all(x['pass'] for x in checks) else 1)
