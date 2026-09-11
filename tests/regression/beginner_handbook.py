from pathlib import Path
import re, yaml
ROOT=Path(__file__).resolve().parents[2]
WIKI=ROOT/'wiki/getting-started'
checks=[]
def add(name,ok,detail=''): checks.append((name,bool(ok),detail))
pages=['index.md','what-is-pse.md','install.md','choose-a-profile.md','create-a-project.md','project-folder.md','edit-your-book.md','build-and-check.md','troubleshooting.md','next-steps.md']
for page in pages: add('page_'+page,(WIKI/page).is_file(),page)
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
nav=str(cfg.get('nav',[]))
for page in pages: add('nav_'+page,f'getting-started/{page}' in nav,page)
text='\n'.join((WIKI/p).read_text() for p in pages)
for command in ['pse doctor --deep','pse profiles --generator-only','pse new ','pse build .','pse check . --human']:
 add('command_'+re.sub(r'\W+','_',command).strip('_'),command in text,command)
for profile in ['academic-monograph','basic-book','bilingual-edition','critical-edition','drama','edited-collection','literary-fiction','poetry','scholarly-edition']:
 add('profile_'+profile,profile in (WIKI/'choose-a-profile.md').read_text(),profile)
folder=(WIKI/'project-folder.md').read_text()
for item in ['book.yml','main.tex','content/','assets/','config/pse-local.tex','config/semantic-modules.json','build/']:
 add('folder_'+re.sub(r'\W+','_',item),item in folder,item)
add('generated_not_source','Do not edit files in `build/` as source' in folder)
add('private_storage','private storage' in text.lower())
add('release_distinction','working PDF' in (WIKI/'next-steps.md').read_text() and '`pse release`' in (WIKI/'next-steps.md').read_text())
add('no_framework_edit_prerequisite','Do not edit the shared PSE core' in folder)
failed=[x for x in checks if not x[1]]
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
raise SystemExit(1 if failed else 0)
