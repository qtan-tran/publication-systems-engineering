#!/usr/bin/env python3
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PYTHON=sys.executable
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[PYTHON,'-m','pse_cli.cli']
checks=[]
def run(name,args,cwd=None,expect=0):
    p=subprocess.run(args,cwd=cwd or ROOT,env=ENV,text=True,capture_output=True)
    ok=(p.returncode==expect); checks.append({'name':name,'pass':ok,'returncode':p.returncode,'expected':expect,'tail':'\n'.join((p.stdout+'\n'+p.stderr).splitlines()[-8:])}); return p
with tempfile.TemporaryDirectory(prefix='pse-m-') as td:
    base=Path(td)/'base'; shutil.copytree(ROOT/'tests/fixtures/drama-semantic',base,ignore=shutil.ignore_patterns('build','release'))
    run('build',CLI+['build',str(base)])
    run('check',CLI+['check',str(base)])
    report=json.loads((base/'build/qa-report.json').read_text())
    checks.append({'name':'drama-metrics','pass':report.get('metrics',{}).get('drama',{}).get('speaker_registry',{}).get('unused')==[]})
    checks.append({'name':'dramatic-line-complete','pass':report.get('metrics',{}).get('scholarly',{}).get('locator_schemes',{}).get('dramatic-line',{}).get('present')==4})
    # QA-only mutations reuse the known-good build so tests do not compile repeatedly.
    undefined=Path(td)/'undefined-source'; shutil.copytree(base,undefined)
    f=undefined/'content/play.tex'; f.write_text(f.read_text()+"\\begin{PSESpeech}{ghost}Ghost line.\\end{PSESpeech}\n")
    run('undefined-speaker-source-check',CLI+['check',str(undefined)],expect=1)
    unused=Path(td)/'unused'; shutil.copytree(base,unused)
    f=unused/'content/play.tex'; f.write_text(f.read_text().replace('\\PSEDeclareSpeaker{chorus}{Chorus}','\\PSEDeclareSpeaker{chorus}{Chorus}\n\\PSEDeclareSpeaker{silent}{Silent}'))
    run('unused-check',CLI+['check',str(unused)])
    rr=json.loads((unused/'build/qa-report.json').read_text()); checks.append({'name':'unused-is-review','pass':any(x['code']=='unused_drama_speaker' and x['severity']=='review' for x in rr['findings'])})
    miss=Path(td)/'missing-line'; shutil.copytree(base,miss)
    f=miss/'content/play.tex'; f.write_text(f.read_text().replace('\\PSEDramaLine{L3}',''))
    run('missing-line-check',CLI+['check',str(miss)],expect=1)
    # TeX-level registry itself must also fail closed on duplicate IDs.
    dup=Path(td)/'duplicate'; shutil.copytree(ROOT/'tests/fixtures/drama-semantic',dup,ignore=shutil.ignore_patterns('build','release'))
    f=dup/'content/play.tex'; f.write_text(f.read_text().replace('\\PSEDeclareSpeaker{beta}{Beta}','\\PSEDeclareSpeaker{beta}{Beta}\n\\PSEDeclareSpeaker{beta}{Beta Again}'))
    run('duplicate-speaker-build',CLI+['build',str(dup)],expect=1)
summary={'schema_version':'0.1','audit_kind':'drama_semantics','passed':sum(bool(c['pass']) for c in checks),'total':len(checks),'checks':checks}
print(json.dumps(summary,indent=2))
sys.exit(0 if all(c['pass'] for c in checks) else 1)
