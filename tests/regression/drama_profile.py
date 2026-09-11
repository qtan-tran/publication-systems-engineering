#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, tempfile, zipfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]; PYTHON=sys.executable
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH',''); CLI=[PYTHON,'-m','pse_cli.cli']; checks=[]
def run(name,args,cwd=None,expect=0):
 p=subprocess.run(args,cwd=cwd or ROOT,env=ENV,text=True,capture_output=True); checks.append({'name':name,'pass':p.returncode==expect,'returncode':p.returncode,'expected':expect,'tail':'\n'.join((p.stdout+'\n'+p.stderr).splitlines()[-8:])}); return p
with tempfile.TemporaryDirectory(prefix='pse-n-') as td:
 td=Path(td); parent=td/'projects'; parent.mkdir()
 run('generate-drama',CLI+['new',str(parent),'--non-interactive','--title','Synthetic Drama','--author','Example Editor','--language','en','--publication-year','2027','--slug','synthetic-drama','--profile','drama'])
 proj=parent/'synthetic-drama'; meta=yaml.safe_load((proj/'book.yml').read_text()); checks.append({'name':'profile-selected','pass':meta.get('profile')=='drama'})
 run('build',CLI+['build',str(proj)]); run('check',CLI+['check',str(proj)])
 qr=json.loads((proj/'build/qa-report.json').read_text())
 checks.append({'name':'drama-speakers-clean','pass':qr.get('metrics',{}).get('drama',{}).get('speaker_registry',{}).get('unused')==[]})
 checks.append({'name':'dramatic-lines-complete','pass':qr.get('metrics',{}).get('scholarly',{}).get('locator_schemes',{}).get('dramatic-line',{}).get('present')==4})
 run('proof',CLI+['proof',str(proj),'--recipient','Synthetic Proofreader'])
 dist=td/'dist'; dist.mkdir(); run('wheel',[PYTHON,'-m','pip','wheel','.', '--no-deps','--no-build-isolation','-w',str(dist)])
 whl=next(dist.glob('*.whl')); names=zipfile.ZipFile(whl).namelist(); checks.append({'name':'wheel-drama-profile','pass':any('profiles/drama/pse-profile-drama.sty' in x for x in names) and any('profiles/drama/profile.json' in x for x in names)})
summary={'schema_version':'0.1','audit_kind':'drama_profile','passed':sum(bool(c['pass']) for c in checks),'total':len(checks),'checks':checks}; print(json.dumps(summary,indent=2)); sys.exit(0 if all(c['pass'] for c in checks) else 1)
