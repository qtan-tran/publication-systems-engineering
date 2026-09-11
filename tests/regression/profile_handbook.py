from pathlib import Path
import json, re, yaml
ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/'wiki/profiles'
PROFILES=ROOT/'profiles'
checks=[]
def add(name,ok,detail=''): checks.append((name,bool(ok),detail))
ids=['academic-monograph','basic-book','bilingual-edition','critical-edition','drama','edited-collection','literary-fiction','poetry','scholarly-edition']
add('overview_exists',(WIKI/'index.md').is_file())
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
nav=str(cfg.get('nav',[]))
over=(WIKI/'index.md').read_text()
for pid in ids:
    page=WIKI/f'{pid}.md'
    add('page_'+pid,page.is_file(),pid)
    add('nav_'+pid,f'profiles/{pid}.md' in nav,pid)
    add('overview_'+pid,f'({pid}.md)' in over,pid)
    if not page.is_file(): continue
    text=page.read_text()
    manifest=json.loads((PROFILES/pid/'profile.json').read_text())
    presentation=json.loads((PROFILES/pid/'presentation.json').read_text())
    add('profile_id_'+pid,f'`{pid}`' in text,pid)
    add('new_command_'+pid,f'--profile {pid}' in text,pid)
    add('demo_path_'+pid,f'examples/profiles/{pid}/' in text,pid)
    add('demo_command_'+pid,f'build_profile_demos.py {pid}' in text,pid)
    add('preset_'+pid,f"`{presentation['preset']}`" in text,pid)
    for mod,policy in manifest.get('module_policy',{}).items():
        pat=f"| `{mod}` | {policy['status']} | {'on' if policy['default_enabled'] else 'off'} |"
        add('policy_'+pid+'_'+mod,pat in text,pat)
    add('build_check_'+pid,'pse build .' in text and 'pse check . --human' in text,pid)
    add('no_build_edit_'+pid,'Do not edit generated files in `build/` as manuscript source' in text,pid)
add('policy_taxonomy',all(x in over for x in ['`required`','`recommended`','`optional`','`discouraged`','`incompatible`']))
add('profiles_commands','pse profiles --generator-only' in over and 'pse profiles --presentation' in over)
add('choice_distinctions',all(x in over for x in ['Academic Monograph vs Scholarly Edition','Critical Edition vs Scholarly Edition','Basic Book vs Literary Fiction']))
failed=[x for x in checks if not x[1]]
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
raise SystemExit(1 if failed else 0)
