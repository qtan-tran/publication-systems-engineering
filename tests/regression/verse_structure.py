from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
    manifest=json.loads((ROOT/'modules/verse-structure/module.json').read_text())
    sty=(ROOT/'modules/verse-structure/pse-module-verse-structure.sty').read_text()
    runtime=json.loads((ROOT/'runtime/pse-runtime.json').read_text())
    checks={
        'semantic_module_preserved':manifest['id']=='verse-structure' and 'verse-structure' in runtime['modules'],
        'verse_semantics_present':{'stanzas','verse-lines','stable-verse-ids'}.issubset(set(manifest['capabilities'])),
        'stable_line_identity':r'\PSEVerseLine' in sty,
        'stanza_identity':'PSEStanza' in sty,
        'no_poetry_profile':'poetry' not in runtime['profiles'],
    }
    for name,ok in checks.items():print(('PASS' if ok else 'FAIL'),name)
    return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
