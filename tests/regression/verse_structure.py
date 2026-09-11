from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+ENV.get('PYTHONPATH','')

def run(cmd,cwd,expect=0,timeout=180):
    p=subprocess.run(cmd,cwd=cwd,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect: raise AssertionError(f"{cmd}\n{p.stdout[-3000:]}\n{p.stderr[-3000:]}")
    return p

def main():
    checks=[]
    module=json.loads((REPO/'modules/verse-structure/module.json').read_text())
    checks.append(('module_manifest',module['id']=='verse-structure' and {'stanzas','verse-lines','stable-verse-ids'}.issubset(module['capabilities']),'manifest'))
    profile=json.loads((REPO/'profiles/poetry/profile.json').read_text())
    checks.append(('profile_uses_module',profile.get('module_policy',{}).get('verse-structure',{}).get('status')=='required','module-owned semantics'))
    sty=(REPO/'profiles/poetry/pse-profile-poetry.sty').read_text()
    checks.append(('presentation_only',r'\NewDocumentCommand{\PSEVerseLine' not in sty and r'\NewDocumentEnvironment{PSEStanza' not in sty,'profile contains hooks only'))
    with tempfile.TemporaryDirectory(prefix='pse-verse-') as td:
        root=Path(td); proj=root/'book'
        run([sys.executable,'-m','pse_cli.cli','new',root,'--non-interactive','--profile','poetry','--title','Synthetic Poetry','--author','PSE','--language','en','--publication-year','2027','--slug','book'],REPO)
        run([sys.executable,'-m','pse_cli.cli','build',proj],REPO,timeout=240)
        run([sys.executable,'-m','pse_cli.cli','check',proj],REPO)
        checks.append(('generated_build',(proj/'build/book.pdf').is_file(),'pdf built'))
        main=(proj/'main.tex').read_text(); content=(proj/'content/poems.tex').read_text()
        checks.append(('semantic_markup',r'\begin{PSEStanza}{s1}' in content and r'\PSEVerseLine{l1}[1]' in content,'stable ids in source'))
        # duplicate line ID must fail at TeX layer
        dup=content.replace(r'\PSEVerseLine{l6}[6]',r'\PSEVerseLine{l1}[6]')
        (proj/'content/poems.tex').write_text(dup)
        p=subprocess.run([sys.executable,'-m','pse_cli.cli','build',str(proj)],cwd=REPO,env=ENV,text=True,capture_output=True,timeout=240)
        checks.append(('duplicate_line_rejected',p.returncode!=0,'duplicate semantic id rejected'))
    failed=[c for c in checks if not c[1]]
    print('Verse structure regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
