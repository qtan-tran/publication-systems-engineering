from __future__ import annotations
import json, os, subprocess, sys, tempfile, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
BASE_ENV=os.environ.copy(); BASE_ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+BASE_ENV.get('PYTHONPATH','')

def generator_profiles():
    ids=[]
    for manifest in sorted((REPO/'profiles').glob('*/profile.json')):
        data=json.loads(manifest.read_text(encoding='utf-8'))
        if data.get('generator_supported') is True:
            ids.append(data['id'])
    return tuple(ids)

PROFILES=generator_profiles()

def run(args, *, cwd=REPO, env=BASE_ENV, expect=0, timeout=180):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect:
        raise AssertionError(f"{args}\nstdout:\n{p.stdout[-4000:]}\nstderr:\n{p.stderr[-4000:]}")
    return p

def main():
    checks=[]; cli=[sys.executable,'-m','pse_cli.cli']
    registry=json.loads(run(cli+['profiles','--json']).stdout)
    ids=[x['id'] for x in registry['profiles']]
    checks.append(('profiles_command',set(PROFILES)==set(ids) and {'critical-edition','poetry','edited-collection'}.issubset(PROFILES),str(ids)))
    schema=json.loads((REPO/'schema/profile.schema.json').read_text())
    checks.append(('profile_schema',schema.get('additionalProperties') is False,'normative schema'))
    for prof in PROFILES:
        data=json.loads((REPO/'profiles'/prof/'profile.json').read_text())
        checks += [
            (f'{prof}_manifest',data.get('schema_version')=='1.1' and isinstance(data.get('module_policy'),dict) and data.get('extends')=='pse-core','manifest validated'),
            (f'{prof}_fixture',(REPO/'tests/fixtures/profile-books'/prof/'book.yml').is_file(),'fixture frozen'),
            (f'{prof}_visual',(REPO/'tests/visual/baselines'/prof/'baseline-manifest.json').is_file(),'visual baseline'),
        ]
    # Wheel content and installed registry: all generator-supported profiles must ship
    # identically to the source registry. One installed critical-edition build proves
    # that the new profile and its module dependencies work outside a source checkout.
    with tempfile.TemporaryDirectory(prefix='pse-profile-wheel-') as td:
        root=Path(td); wh=root/'wh'; wh.mkdir()
        run([sys.executable,'-m','pip','wheel','--no-build-isolation','--no-deps','-w',str(wh),str(REPO)],cwd=root)
        wheel=next(wh.glob('publication_systems_engineering-*.whl'))
        with zipfile.ZipFile(wheel) as zf:
            names=set(zf.namelist())
            for prof in PROFILES:
                checks.append((f'wheel_contains_{prof}',any(n.endswith(f'/profiles/{prof}/profile.json') for n in names) and any(n.endswith(f'/profiles/{prof}/pse-profile-{prof}.sty') for n in names),'profile packaged'))
            checks.append(('wheel_contains_profile_schema',any(n.endswith('/schema/profile.schema.json') for n in names),'schema packaged'))
        target=root/'target'; run([sys.executable,'-m','pip','install','--no-deps','--target',str(target),str(wheel)],cwd=root)
        env=os.environ.copy(); env.pop('PSE_ROOT',None); env['PYTHONPATH']=str(target)
        installed=json.loads(run([sys.executable,'-m','pse_cli.cli','profiles','--json'],cwd=root,env=env).stdout)
        checks.append(('installed_registry',set(PROFILES)=={x['id'] for x in installed['profiles']},'installed registry'))
        books=root/'books'; books.mkdir()
        run([sys.executable,'-m','pse_cli.cli','new',str(books),'--non-interactive','--profile','critical-edition','--title','Installed Critical Edition','--author','PSE','--language','en','--publication-year','2027','--slug','critical'],cwd=root,env=env)
        installed_project=books/'critical'
        run([sys.executable,'-m','pse_cli.cli','build',str(installed_project)],cwd=root,env=env,timeout=240)
        run([sys.executable,'-m','pse_cli.cli','check',str(installed_project)],cwd=root,env=env)
        installed_qa=json.loads((installed_project/'build/qa-report.json').read_text(encoding='utf-8'))
        checks.append(('installed_critical_build',installed_qa.get('status')=='pass' and (installed_project/'build/book.pdf').is_file(),f"qa={installed_qa.get('status')}"))
    failed=[x for x in checks if not x[1]]
    print('Profile contract registry regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
