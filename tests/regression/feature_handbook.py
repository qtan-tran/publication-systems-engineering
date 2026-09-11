from pathlib import Path
import json, yaml
ROOT=Path(__file__).resolve().parents[2]
W=ROOT/'wiki/book-features'
PROFILES=ROOT/'profiles'
checks=[]
def add(name,ok,detail=''): checks.append((name,bool(ok),detail))
profiles=['academic-monograph','basic-book','bilingual-edition','critical-edition','drama','edited-collection','literary-fiction','poetry','scholarly-edition']
labels={
'academic-monograph':'Academic Monograph','basic-book':'Basic Book','bilingual-edition':'Bilingual Edition','critical-edition':'Critical Edition','drama':'Drama','edited-collection':'Edited Collection','literary-fiction':'Literary Fiction','poetry':'Poetry','scholarly-edition':'Scholarly Edition'}
pages={
'structural-hierarchy':'structural-hierarchy.md',
'publication-unit-metadata':'publication-metadata.md',
'contributor-metadata':'publication-metadata.md',
'margin-objects':'margins-and-side-material.md',
'parallel-text':'parallel-text.md',
'apparatus':'apparatus.md',
'canonical-locators':'locators.md',
'dramatic-locators':'locators.md',
'verse-structure':'verse-and-drama.md',
'drama-structure':'verse-and-drama.md',
'bibliography':'bibliography-index-scholarly-matter.md',
'index':'bibliography-index-scholarly-matter.md',
'scholarly-matter':'bibliography-index-scholarly-matter.md',
'multilingual':'multilingual-text.md',
}
all_pages=['index.md','structural-hierarchy.md','publication-metadata.md','typography-and-page-grid.md','margins-and-side-material.md','parallel-text.md','apparatus.md','locators.md','verse-and-drama.md','bibliography-index-scholarly-matter.md','multilingual-text.md']
for f in all_pages: add('page_'+f,(W/f).is_file(),f)
index=(W/'index.md').read_text()
for f in all_pages[1:]: add('overview_link_'+f,f'({f})' in index,f)
add('policy_taxonomy',all(x in index for x in ['`required`','`recommended`','`optional`','`discouraged`','`incompatible`','`not declared`']))
add('source_truth_statement','regression-checked' in index and '`profile.json`' in index)
# Every public module gets a handbook home.
module_ids=sorted(json.loads(p.read_text())['id'] for p in (ROOT/'modules').glob('*/module.json'))
for m in module_ids: add('module_covered_'+m,m in pages,m)
# Bind all policy rows (including explicit not-declared rows) to manifests.
man={p:json.loads((PROFILES/p/'profile.json').read_text()) for p in profiles}
for module,page in pages.items():
    text=(W/page).read_text()
    for p in profiles:
        pol=man[p].get('module_policy',{}).get(module)
        if pol:
            row=f"| [{labels[p]}](../profiles/{p}.md) | {pol['status']} | {'on' if pol['default_enabled'] else 'off'} |"
        else:
            row=f"| [{labels[p]}](../profiles/{p}.md) | not declared | — |"
        add('policy_'+module+'_'+p,row in text,row)
# Presentation page is bound to presentation.json rather than module policy.
pres=(W/'typography-and-page-grid.md').read_text()
for p in profiles:
    d=json.loads((PROFILES/p/'presentation.json').read_text())
    row=f"| [{labels[p]}](../profiles/{p}.md) | `{d['grid']}` | `{d['side_material']}` |"
    add('presentation_'+p,row in pres,row)
add('semantic_presentation_boundary','semantic modules' in pres.lower() and 'presentation contracts' in pres.lower())
add('parallel_modes',all(x in (W/'parallel-text.md').read_text() for x in ['`parallel-columns`','`facing-pages`','`sequential-blocks`','`source-dominant`','`target-dominant`']))
add('apparatus_streams',all(x in (W/'apparatus.md').read_text() for x in ['`textual`','`editorial`','`translation`','`commentary`','`source`']))
add('locator_namespaces',all(x in (W/'locators.md').read_text() for x in ['`canonical`','`dramatic-line`','`verse-line`','`parallel-alignment`']))
add('margin_types',all(x in (W/'margins-and-side-material.md').read_text().lower() for x in ['marginal notes','side captions','apparatus anchors','locator markers','running-side objects']))
# Navigation exposes all handbook pages.
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text()); nav=str(cfg.get('nav',[]))
for f in all_pages: add('nav_'+f,f'book-features/{f}' in nav,f)
# No old phase-stub language should remain in Feature Handbook.
whole='\n'.join((W/f).read_text() for f in all_pages)
add('no_stale_stub_language','documentation stub' not in whole.lower() and 'feature handbook phase' not in whole.lower())
failed=[x for x in checks if not x[1]]
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
raise SystemExit(1 if failed else 0)
