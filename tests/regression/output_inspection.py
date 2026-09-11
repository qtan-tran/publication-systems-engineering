from __future__ import annotations
import json, sys, tempfile
from pathlib import Path
from pypdf import PdfWriter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from pse_cli.output_inspection import inspect_pdf
checks=[]
def add(name,passed,detail=''): checks.append({"name":name,"pass":bool(passed),"detail":detail})
demo_reports={}
for pdf in sorted((ROOT/'examples/profiles').glob('*/output/*-demo.pdf')):
    profile=pdf.parents[1].name
    demo_reports[profile]=inspect_pdf(pdf,expected_language='en')
add('canonical_demo_count',len(demo_reports)==9,sorted(demo_reports))
for profile, demo_report in demo_reports.items():
    items={c['name']:c for c in demo_report['checks']}
    add(f'{profile}_language',items['document_language']['status']=='pass',items['document_language'])
    add(f'{profile}_text_extractable',items['text_extractability']['status']=='pass',items['text_extractability'])
    add(f'{profile}_metadata',items['title_metadata']['status']=='pass' and items['author_metadata']['status']=='pass',{'title':items['title_metadata'],'author':items['author_metadata']})
poetry=ROOT/'examples/profiles/poetry/output/poetry-demo.pdf'
r=demo_reports['poetry']; by={c['name']:c for c in r['checks']}
add('canonical_pdf_readable',r['summary']['error']==0,r['summary'])
add('canonical_hash_binding',bool(r.get('pdf_sha256')) and len(r.get('pdf_sha256',''))==64,r.get('pdf_sha256'))
add('canonical_title',by['title_metadata']['status']=='pass',by['title_metadata'])
add('canonical_author',by['author_metadata']['status']=='pass',by['author_metadata'])
add('canonical_language',by['document_language']['status']=='pass',by['document_language'])
add('canonical_bookmarks',by['bookmarks_navigation']['status'] in {'pass','review'},by['bookmarks_navigation'])
add('canonical_text_extractable',by['text_extractability']['status']=='pass',by['text_extractability'])
add('no_false_certification',r.get('certification')=='none' and 'does not certify' in r.get('scope_note',''),r.get('scope_note',''))
add('reading_order_human_review',by['reading_order']['status']=='review' and by['reading_order']['machine_verifiable'] is False,by['reading_order'])
add('alt_text_human_review',by['image_alt_text']['status']=='review' and by['image_alt_text']['machine_verifiable'] is False,by['image_alt_text'])
with tempfile.TemporaryDirectory() as td:
    bad=Path(td)/'minimal.pdf'; w=PdfWriter(); w.add_blank_page(width=100,height=100)
    with bad.open('wb') as fh:w.write(fh)
    m=inspect_pdf(bad,expected_language='en'); d={c['name']:c for c in m['checks']}
    add('missing_metadata_reported',d['title_metadata']['status']=='warning' and d['author_metadata']['status']=='warning',m['summary'])
    add('missing_language_reported',d['document_language']['status']=='warning',d['document_language'])
    add('untagged_not_certified',d['tagged_pdf']['status']=='review',d['tagged_pdf'])
payload={"suite":"output_inspection","passed":all(c['pass'] for c in checks),"checks":checks}
print(json.dumps(payload,indent=2)); raise SystemExit(0 if payload['passed'] else 1)
