from pathlib import Path
import json,yaml
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'wiki/profiles'
profiles=sorted(p.parent.name for p in (ROOT/'profiles').glob('*/profile.json'))
nav=str(yaml.safe_load((ROOT/'mkdocs.yml').read_text())['nav'])
over=(W/'index.md').read_text()
checks=[]
def ck(name,ok):checks.append((name,bool(ok)))
ck('six_profiles',len(profiles)==6)
ck('overview',all(f'({pid}.md)' in over for pid in profiles))
for pid in profiles:
    manifest=json.loads((ROOT/'profiles'/pid/'profile.json').read_text())
    presentation=json.loads((ROOT/'profiles'/pid/'presentation.json').read_text())
    text=(W/f'{pid}.md').read_text()
    ck(f'{pid}_page',f'`{pid}`' in text)
    ck(f'{pid}_nav',f'profiles/{pid}.md' in nav)
    ck(f'{pid}_generator_command',f'--profile {pid}' in text)
    ck(f'{pid}_presentation_preset',f"`{presentation['preset']}`" in text)
    ck(f'{pid}_demo',f'examples/profiles/{pid}/' in text)
    for mid,rule in manifest['module_policy'].items():
        expected=f"| `{mid}` | {rule['status']} | {'on' if rule['default_enabled'] else 'off'} |"
        ck(f'{pid}_{mid}_policy',expected in text)
for retired in ('basic-book','poetry','scholarly-edition'):
    ck(f'{retired}_page',(W/f'{retired}.md').is_file() and retired not in profiles)
ck('no_legacy_migration_guide',not (ROOT/'wiki/getting-started/profile-migration.md').is_file())
for name,ok in checks:print(('PASS' if ok else 'FAIL'),name)
print(f'summary: {sum(ok for _,ok in checks)}/{len(checks)} pass')
raise SystemExit(0 if all(ok for _,ok in checks) else 1)
