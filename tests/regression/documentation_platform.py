from pathlib import Path
import subprocess, sys, yaml
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def add(n,ok,d=''): checks.append((n,bool(ok),d))
cfg=yaml.safe_load((ROOT/'mkdocs.yml').read_text())
add('material_theme',cfg.get('theme',{}).get('name')=='material')
add('canonical_source',cfg.get('docs_dir')=='wiki')
add('strict_config',cfg.get('strict') is True)
add('search_enabled','search' in cfg.get('plugins',[]))
add('directory_urls',cfg.get('use_directory_urls') is True)
add('no_hardcoded_site_url','site_url' not in cfg)
add('pse_stylesheet','assets/stylesheets/pse.css' in cfg.get('extra_css',[]))
add('404_exists',(ROOT/'wiki/404.md').is_file())
add('platform_contract',(ROOT/'docs/documentation/DOCUMENTATION-PLATFORM.md').is_file())
add('material_dependency','mkdocs-material' in (ROOT/'requirements/docs.txt').read_text())
qa=subprocess.run([sys.executable,str(ROOT/'scripts/docs/validate_docs.py')],cwd=ROOT,capture_output=True,text=True)
add('source_qa',qa.returncode==0,qa.stdout[-200:])
out=ROOT/'build/test-mkdocs-deployment.yml'; out.parent.mkdir(exist_ok=True)
prep=subprocess.run([sys.executable,str(ROOT/'scripts/docs/prepare_mkdocs_config.py'),'--site-url','https://docs.example.test/pse','--output',str(out.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
add('deployment_config_generated',prep.returncode==0 and out.is_file(),prep.stderr)
if out.is_file():
 dep=yaml.safe_load(out.read_text()); add('deployment_site_url',dep.get('site_url')=='https://docs.example.test/pse/',str(dep.get('site_url')))
else: add('deployment_site_url',False)
wf=(ROOT/'.github/workflows/docs-pages.yml').read_text()
add('pages_base_url_bound','steps.pages.outputs.base_url' in wf)
add('strict_renderer_gate','mkdocs build --strict' in wf)
add('analytics_not_hardcoded',all(x not in '\n'.join(p.read_text(errors='replace') for p in (ROOT/'wiki').rglob('*.md')) for x in ['G-', 'plausible.io/js']))
for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+((': '+d) if d else ''))
failed=[x for x in checks if not x[1]]
print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
raise SystemExit(1 if failed else 0)
