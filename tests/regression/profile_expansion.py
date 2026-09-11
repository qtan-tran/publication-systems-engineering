from __future__ import annotations
import json, os, subprocess, sys, tempfile
from pathlib import Path
REPO=Path(__file__).resolve().parents[2]
ENV=os.environ.copy(); ENV['PYTHONPATH']=str(REPO/'tools')+os.pathsep+ENV.get('PYTHONPATH','')

def generator_profiles():
    ids=[]
    for manifest in sorted((REPO/'profiles').glob('*/profile.json')):
        data=json.loads(manifest.read_text(encoding='utf-8'))
        if data.get('generator_supported') is True:
            ids.append(data['id'])
    return tuple(ids)

PROFILES=generator_profiles()
FORBIDDEN=(r'\PSESetTitle',r'\PSESetAuthor',r'\PSEEnableProofMode',r'\PSESetProofRecipient',r'\AddToShipoutPictureFG')

def run(*args, expect=0, timeout=240):
    p=subprocess.run([sys.executable,'-m','pse_cli.cli',*map(str,args)],cwd=REPO,env=ENV,text=True,capture_output=True,timeout=timeout)
    if p.returncode!=expect: raise AssertionError(f"{args}\n{p.stdout[-5000:]}\n{p.stderr[-5000:]}")
    return p

def main():
    checks=[]
    checks.append(('expanded_profiles_registered',{'critical-edition','poetry','edited-collection'}.issubset(PROFILES),str(PROFILES)))
    checks.append(('profile_contract_doc',(REPO/'docs/architecture/PROFILE-API-CONTRACT.md').is_file(),'contract present'))
    for prof in PROFILES:
        d=REPO/'profiles'/prof
        sty=d/f'pse-profile-{prof}.sty'; manifest=d/'profile.json'
        checks.append((f'{prof}_files',sty.is_file() and manifest.is_file(),str(d)))
        data=json.loads(manifest.read_text())
        checks.append((f'{prof}_manifest',data.get('id')==prof and data.get('extends')=='pse-core' and data.get('generator_supported') is True,'manifest valid'))
        text=sty.read_text()
        checks.append((f'{prof}_no_backbone_override',not any(tok in text for tok in FORBIDDEN),'forbidden core/security APIs absent'))
        if prof == 'critical-edition':
            checks.append(('critical_semantics_module_owned',not any(tok in text for tok in (r'\NewDocumentCommand{\PSELocator',r'\NewDocumentCommand{\PSEApparatus',r'\newenvironment{PSEApparatus')),'no locator/apparatus semantic implementation in profile'))
        if prof == 'poetry':
            checks.append(('poetry_semantics_module_owned',not any(tok in text for tok in (r'\NewDocumentCommand{\PSEVerseLine',r'\NewDocumentEnvironment{PSEStanza')),'no verse semantic implementation in profile'))
        if prof == 'edited-collection':
            checks.append(('edited_collection_semantics_module_owned',not any(tok in text for tok in (r'\NewDocumentCommand{\PSEDeclareContributor',r'\NewDocumentCommand{\PSEContribution')),'no contributor semantic implementation in profile'))
    # Generator discovery is registry-driven for every profile. Heavy TeX lifecycle
    # checks are confined here to the newly introduced profile; existing profiles keep
    # their established dedicated regressions and full visual orchestration remains registry-driven.
    with tempfile.TemporaryDirectory(prefix='pse-profile-expansion-') as td:
        parent=Path(td)
        projects={}
        for prof in PROFILES:
            slug='profile-'+prof
            run('new',parent,'--non-interactive','--profile',prof,'--title',f'Synthetic {prof}','--author','Synthetic Editor','--language','en','--publication-year','2027','--slug',slug)
            project=parent/slug; projects[prof]=project
            main=(project/'main.tex').read_text()
            checks.append((f'{prof}_generated_package',f'\\usepackage{{pse-profile-{prof}}}' in main,'correct profile package'))
            book=(project/'book.yml').read_text()
            checks.append((f'{prof}_metadata',f'profile: {prof}' in book,'profile metadata'))
        project=projects['critical-edition']
        run('build',project,timeout=240); run('check',project)
        qa=json.loads((project/'build/qa-report.json').read_text())
        pdf=qa.get('metrics',{}).get('pdf',{})
        scholarly=qa.get('metrics',{}).get('scholarly',{})
        checks.append(('critical_qa',qa.get('status')=='pass',f"qa={qa.get('status')}"))
        checks.append(('critical_geometry',abs(float(pdf.get('width_mm',0))-126.0)<0.05 and abs(float(pdf.get('height_mm',0))-198.0)<0.05,str(pdf)))
        checks.append(('critical_locator_contract',scholarly.get('locator_scheme',{}).get('present')==4 and scholarly.get('locator_scheme',{}).get('missing')==[],str(scholarly.get('locator_scheme',{}))))
        proof=run('proof',project,'--recipient','Critical Edition Reviewer','--proof-id','PSE-CRITICAL-001',timeout=240)
        checks.append(('critical_secure_proof','proof:' in proof.stdout and any((project/'build/proofs').glob('*.pdf')),'recipient-specific proof'))
        critical_main=(project/'main.tex').read_text(encoding='utf-8')
        checks.append(('critical_publication_page',r'\PSEPublicationPage' in critical_main,'standard publication page retains mandatory attribution hook'))
    failed=[x for x in checks if not x[1]]
    print('Profile expansion regression')
    for n,ok,d in checks: print(('PASS' if ok else 'FAIL'),n+':',d)
    print(f'summary: {len(checks)-len(failed)}/{len(checks)} pass')
    return 1 if failed else 0
if __name__=='__main__': raise SystemExit(main())
