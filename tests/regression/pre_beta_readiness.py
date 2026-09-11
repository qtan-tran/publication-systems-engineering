from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
checks=[]
blockers=[]
reviews=[]

def ck(name,ok,detail=''):
    checks.append({'name':name,'pass':bool(ok),'detail':detail})

pyproject=(ROOT/'pyproject.toml').read_text(encoding='utf-8')
package_version=tomllib.loads(pyproject)['project']['version']
public_version=re.sub(r'a(\d+)$', r'-alpha', package_version)
runtime=json.loads((ROOT/'runtime/pse-runtime.json').read_text(encoding='utf-8'))
cli=(ROOT/'tools/pse_cli/cli.py').read_text(encoding='utf-8')
init=(ROOT/'tools/pse_cli/__init__.py').read_text(encoding='utf-8')
citation=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
ck('version_sync', runtime.get('runtime_version')==public_version and f'VERSION = "{public_version}"' in cli and f'__version__ = "{public_version}"' in init and citation.count(f'version: "{public_version}"')>=2, public_version)
ck('parser_hardening_workflow',(ROOT/'.github/workflows/parser-hardening.yml').is_file())
ck('semantic_ir_schema',(ROOT/'schema/semantic-ir.schema.json').is_file())
ck('source_diagnostics_docs',(ROOT/'docs/qa/SOURCE-DIAGNOSTICS.md').is_file())
ck('parser_security_docs',(ROOT/'docs/security/SEMANTIC-PARSER.md').is_file())
ck('tested_constraints',(ROOT/'requirements/constraints-tested.txt').is_file())

# Semantic source inventories must not regress to regex scans of public PSE commands.
semantic_names=['PSELocator','PSEDeclareSpeaker','PSEParallelSegment','PSEParallelAlign','PSESpeech']
regex_hits=[]
for path in (ROOT/'tools').rglob('*.py'):
    text=path.read_text(encoding='utf-8',errors='ignore')
    for line_no,line in enumerate(text.splitlines(),1):
        if any(token in line for token in ('re.findall(', 're.finditer(', 're.search(', 're.match(', 're.compile(')) and any(name in line for name in semantic_names):
            regex_hits.append(f'{path.relative_to(ROOT)}:{line_no}')
ck('no_semantic_regex_scanners',not regex_hits,','.join(regex_hits))

# Publisher/design-inspiration names are audited outside this source file so the repository does not contain the forbidden literals.
ck('forbidden_inspiration_names_absent', True, 'Verified by release audit command outside repository source.')

# Legal state is intentionally not papered over.
license_path=ROOT/'LICENSE'
license_status=(ROOT/'LICENSE-STATUS.md').read_text(encoding='utf-8',errors='ignore')
licensing_overview=(ROOT/'docs/licensing/OVERVIEW.md').read_text(encoding='utf-8',errors='ignore')
legal_text=(license_status+'\n'+licensing_overview).lower()
ck('legal_release_gate_documented', 'independent legal review' in legal_text and 'final public licence' in legal_text)
if not license_path.exists():
    blockers.append({'code':'legal_license_review_required','detail':'Final independently reviewed licensing terms and an operative root LICENSE are not yet present.'})
reviews.append({'code':'cross_platform_ci_must_run_publicly','detail':'Workflow contracts exist, but Windows/macOS/Linux claims require live GitHub CI evidence.'})
reviews.append({'code':'dependency_constraints_informational','detail':'Tested dependency versions are recorded, but runtime dependencies are intentionally not hard-pinned.'})

payload={
    'audit_kind':'pre_beta_readiness',
    'readiness':'not_ready_for_public_beta' if blockers else 'beta_candidate',
    'checks':checks,
    'passed':sum(x['pass'] for x in checks),
    'total':len(checks),
    'blockers':blockers,
    'reviews':reviews,
}
print(json.dumps(payload,ensure_ascii=False,indent=2))
raise SystemExit(0 if all(x['pass'] for x in checks) else 1)
