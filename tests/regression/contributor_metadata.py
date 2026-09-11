from __future__ import annotations
import json, os, shutil, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    checks=[]
    module=json.loads((ROOT/'modules/contributor-metadata/module.json').read_text())
    profile=json.loads((ROOT/'profiles/edited-collection/profile.json').read_text())
    sty=(ROOT/'modules/contributor-metadata/pse-module-contributor-metadata.sty').read_text()
    pst=(ROOT/'profiles/edited-collection/pse-profile-edited-collection.sty').read_text()
    checks += [
      ('module_registered',module['id']=='contributor-metadata','module id'),
      ('profile_uses_module',profile.get('module_policy',{}).get('contributor-metadata',{}).get('status')=='required',str(profile.get('module_policy'))),
      ('minimal_identity_api',all(x in sty for x in ('\\PSEDeclareContributor','\\PSEContribution')),'declaration + relation'),
      ('role_is_relation','pse@contribution@#1@#2@#3' in sty,'role participates in relation key'),
      ('presentation_boundary','\\PSEDeclareContributor' not in pst and '\\PSEContribution' not in pst,'profile does not own semantic API'),
    ]
    if shutil.which('lualatex'):
      with tempfile.TemporaryDirectory(prefix='pse-contributor-') as td:
        td=Path(td); tex=td/'ok.tex'
        tex.write_text(r'''\documentclass{article}
\usepackage{pse-module-contributor-metadata}
\begin{document}
\PSEDeclareContributor{a}{Ada Example}[Synthetic Institute][0000-0000-0000-0000]
\PSEContribution{a}{chapter-1}{author}
\end{document}
''')
        env=os.environ.copy(); env['TEXINPUTS']=str((ROOT/'modules/contributor-metadata').resolve())+os.pathsep+env.get('TEXINPUTS','')
        p=subprocess.run(['lualatex','--interaction=nonstopmode','--halt-on-error',str(tex)],cwd=td,text=True,capture_output=True,env=env)
        checks.append(('lualatex_smoke',p.returncode==0,(p.stdout+p.stderr)[-500:]))
    failed=[c for c in checks if not c[1]]
    print('Contributor metadata regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
