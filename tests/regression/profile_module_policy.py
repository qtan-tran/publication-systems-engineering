from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(ROOT/'tools')+os.pathsep+ENV.get('PYTHONPATH','')
CLI=[sys.executable,'-m','pse_cli.cli']

EXPECTED_INDEX={
    'academic-monograph':('recommended',True),
    'basic-book':('recommended',True),
    'bilingual-edition':('recommended',True),
    'critical-edition':('recommended',True),
    'drama':('recommended',True),
    'edited-collection':('recommended',True),
    'literary-fiction':('discouraged',False),
    'poetry':('optional',False),
    'scholarly-edition':('recommended',True),
}

def run(args, expect=0, timeout=180):
    p=subprocess.run(args,cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-4000:]}\nstderr:\n{p.stderr[-4000:]}")
    return p

def main():
    checks=[]
    manifests={}
    for path in sorted((ROOT/'profiles').glob('*/profile.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        manifests[data['id']]=data
        checks.append((f"{data['id']}_schema_1_1",data.get('schema_version')=='1.1',str(data.get('schema_version'))))
        checks.append((f"{data['id']}_policy_present",isinstance(data.get('module_policy'),dict),'module_policy'))
    for pid,(status,default) in EXPECTED_INDEX.items():
        rule=manifests[pid]['module_policy'].get('index',{})
        checks.append((f'{pid}_index_policy',rule.get('status')==status and rule.get('default_enabled') is default,str(rule)))
    # Existing semantic ownership remains required.
    required={
      'bilingual-edition':{'parallel-text','contributor-metadata'},
      'critical-edition':{'canonical-locators','apparatus','multilingual','bibliography','scholarly-matter','contributor-metadata'},
      'drama':{'drama-structure','dramatic-locators'},
      'edited-collection':{'contributor-metadata','publication-unit-metadata','structural-hierarchy'},
      'poetry':{'verse-structure'},
      'scholarly-edition':{'canonical-locators','apparatus','multilingual','bibliography','scholarly-matter','contributor-metadata'},
    }
    for pid, mids in required.items():
        got={mid for mid,rule in manifests[pid]['module_policy'].items() if rule['status']=='required'}
        checks.append((f'{pid}_required_semantics',got==mids,str(sorted(got))))
    # CLI exposes the policy in human output.
    out=run(CLI+['profiles','--modules']).stdout
    checks.append(('profiles_modules_surface','edited-collection' in out and 'recommended: index [default]' in out and 'optional: index' in out and 'discouraged: index' in out,'human policy surface'))
    # Deactivation can remove recommended/default index, but not a required module.
    with tempfile.TemporaryDirectory(prefix='pse-policy-') as td:
        parent=Path(td)
        run(CLI+['new',str(parent),'--non-interactive','--profile','edited-collection','--title','Policy Test','--author','Synthetic Editor','--language','en','--publication-year','2027','--slug','edited'])
        project=parent/'edited'
        cfg=json.loads((project/'config/semantic-modules.json').read_text())
        checks.append(('semantic_config_1_1',cfg.get('schema_version')=='1.1' and cfg.get('deactivate')==[],str(cfg)))
        cfg['deactivate']=['index']
        (project/'config/semantic-modules.json').write_text(json.dumps(cfg,indent=2)+'\n')
        # Build is expected to fail because source still calls index commands; this proves deactivation is real.
        p=subprocess.run(CLI+['build',str(project)],cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=180)
        checks.append(('recommended_index_can_deactivate',p.returncode!=0 and ('PSEPrintIndex' in p.stdout+p.stderr or 'Undefined control sequence' in p.stdout+p.stderr),'index really removed from active modules'))
        cfg['deactivate']=['contributor-metadata']
        (project/'config/semantic-modules.json').write_text(json.dumps(cfg,indent=2)+'\n')
        p=subprocess.run(CLI+['build',str(project)],cwd=ROOT,env=ENV,text=True,capture_output=True,timeout=60)
        checks.append(('required_module_cannot_deactivate',p.returncode!=0 and 'Required profile module' in (p.stdout+p.stderr),'required semantic ownership protected'))
    failed=[x for x in checks if not x[1]]
    print('Profile module policy regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0

if __name__=='__main__':
    raise SystemExit(main())
