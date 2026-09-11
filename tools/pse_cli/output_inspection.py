from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from pypdf import PdfReader
from .release_contract import OUTPUT_INSPECTION_SCHEMA_VERSION, sha256_file

def _catalog_language(reader: PdfReader) -> str:
    value = reader.trailer["/Root"].get("/Lang")
    return "" if value is None else str(value).strip("()")

def _outline_count(value: Any) -> int:
    if not isinstance(value, list):
        return 0
    return sum(_outline_count(x) if isinstance(x, list) else 1 for x in value)

def _finish(path: Path, checks: list[dict[str, Any]]) -> dict[str, Any]:
    levels=("error","warning","review","pass","info")
    summary={k:sum(1 for c in checks if c["status"]==k) for k in levels}
    status="error" if summary["error"] else ("warning" if summary["warning"] else ("review" if summary["review"] else "pass"))
    return {"schema_version":OUTPUT_INSPECTION_SCHEMA_VERSION,"kind":"pse-output-inspection","pdf":str(path),"pdf_sha256":sha256_file(path) if Path(path).is_file() else None,"status":status,"summary":summary,"checks":checks,"certification":"none","scope_note":"Machine inspection baseline only; this command does not certify PDF/UA, WCAG, archival, or legal accessibility conformance."}

def inspect_pdf(path: Path, *, expected_language: str | None = None) -> dict[str, Any]:
    path=Path(path); checks=[]
    def add(name,status,detail,machine_verifiable=True):
        checks.append({"name":name,"status":status,"detail":detail,"machine_verifiable":machine_verifiable})
    if not path.is_file():
        add("pdf_exists","error","PDF file not found")
        return _finish(path,checks)
    try: reader=PdfReader(str(path))
    except Exception as exc:
        add("pdf_readable","error",f"{type(exc).__name__}: {exc}")
        return _finish(path,checks)
    add("pdf_readable","pass",f"{len(reader.pages)} page(s)")
    add("not_encrypted","pass" if not reader.is_encrypted else "warning","not encrypted" if not reader.is_encrypted else "PDF is encrypted")
    metadata=reader.metadata or {}
    title=str(metadata.get('/Title') or '').strip(); author=str(metadata.get('/Author') or '').strip()
    add("title_metadata","pass" if title else "warning",title or "missing /Title")
    add("author_metadata","pass" if author else "warning",author or "missing /Author")
    language=_catalog_language(reader)
    if not language: add("document_language","warning","missing PDF catalog /Lang")
    elif expected_language and language.lower()!=expected_language.lower(): add("document_language","warning",{"catalog":language,"expected":expected_language})
    else: add("document_language","pass",language)
    try: outlines=_outline_count(reader.outline)
    except Exception: outlines=0
    add("bookmarks_navigation","pass" if outlines else "review",f"{outlines} bookmark item(s)" if outlines else "no bookmark items detected")
    lengths=[]; errors=[]
    for i,page in enumerate(reader.pages,1):
        try:lengths.append(len((page.extract_text() or '').strip()))
        except Exception:lengths.append(0); errors.append(i)
    text_pages=sum(1 for n in lengths if n>0); total=len(lengths); ratio=(text_pages/total) if total else 0.0
    st="review" if errors or ratio<0.5 or sum(lengths)<100 else "pass"
    add("text_extractability",st,{"pages_with_extractable_text":text_pages,"total_pages":total,"extractable_page_ratio":round(ratio,3),"total_extracted_characters":sum(lengths),"page_extraction_errors":errors})
    root=reader.trailer['/Root']; mark_info=root.get('/MarkInfo'); marked=False
    try: marked=bool(mark_info and mark_info.get('/Marked'))
    except Exception: pass
    add("tagged_pdf","pass" if marked else "review","tag structure detected" if marked else "no tagged-PDF structure detected")
    add("reading_order","review","requires human/specialist inspection; text extraction alone does not establish correct reading order",False)
    add("image_alt_text","review","requires inspection when meaningful images are present; this baseline does not certify alt text",False)
    add("formal_accessibility_conformance","info","not assessed; no PDF/UA, WCAG, archival, or legal accessibility certification",False)
    return _finish(path,checks)

def render_human(report: dict[str, Any]) -> str:
    lines=[f"PSE output inspection: {report['pdf']}",f"status: {report['status']}"]
    for c in report['checks']:
        detail=c['detail']
        if isinstance(detail,(dict,list)): detail=json.dumps(detail,ensure_ascii=False,sort_keys=True)
        lines.append(f"{c['status'].upper():7} {c['name']}: {detail}")
    lines.append('Certification: none.')
    return '\n'.join(lines)
