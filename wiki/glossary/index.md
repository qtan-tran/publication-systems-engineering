---
title: The PSE Glossary
description: Conceptual glossary of publication architecture, textual scholarship, typography, and quality assurance in Publication Systems Engineering.
---

# The PSE Glossary

This glossary presents the concepts of Publication Systems Engineering (PSE) as a **conceptual architecture of a publishing system**, not as an alphabetical list. This organization helps readers without a background in programming, LaTeX, or book design understand each term in relation to the others, and understand why each one matters in book production.

The definitions draw on experience from real production projects, then generalize it for a range of publication types: scholarly monographs, textbooks, philosophical works, drama, and scholarly critical editions.

The glossary prefers clear English terms that will remain usable over the long term, and it documents the Vietnamese equivalents chosen for the Vietnamese edition of this wiki so that the two languages stay aligned.

## Structure of the glossary

- [Textual scholarship](textual-scholarship.md): which text is being conveyed to the reader, and on what basis we confirm that this is the right text.
- [Semantic structure](semantic-structure.md): how the text is organized, independently of how it is presented on the page.
- [Locators and references](locators-and-references.md): identifiers, anchors, tables of contents, indexes, and the reference relations between parts of the content.
- [Typography and layout](typography-and-layout.md): how content becomes a readable visual form while each edition keeps its own design identity.
- [Build and versioning](build-and-versioning.md): the build process, version management, packaging, archiving, and metadata.
- [Quality assurance and release](quality-assurance.md): validation, regression testing, the layers of quality sign-off, and the release decision.

These are conceptual groups, not seven mandatory linear stages. The layers have dependencies among them and can be exercised several times during production.

The foundational principle of PSE is to **separate content, logical structure, presentation, and the production process, while guaranteeing that they stay in correspondence**.

## A general definition of PSE

**Publication Systems Engineering**

Publication Systems Engineering treats book production as the design, organization, validation, and maintenance of a publication production system, rather than as a one-off task of laying out text on pages.

Such a system includes the source text, content structure, locator and reference conventions, design principles, typesetting tools, quality-control processes, and the mechanisms for archiving and reproducing editions.

PSE separates components with different functions while guaranteeing their correspondence; it standardizes reusable work while preserving the distinctive character of each work; and it automates rule-governed work without replacing scholarly and editorial judgment with formal checks.

The goal of PSE is not only to produce books that are beautiful and consistent, but to build a publication process that is verifiable, traceable, repairable, reproducible, and maintainable over the long term.

## Concept pairs that are easy to confuse

The pairs below are commonly confused in day-to-day discussion; distinguishing them clearly makes conversations about book quality more precise.

| Concept A | Concept B | Core difference |
| --- | --- | --- |
| Verse line | Physical line | A unit of the work versus a unit of the printed page. |
| Canonical locator | Page number | A position by the conventions of the text versus a position in one specific edition. |
| Anchor | Marker | A technical address versus a symbol the reader sees. |
| Table of contents | Index | A map of the book's structure versus a map of its content objects. |
| Glossary | Index | Explaining meaning versus pointing to occurrences. |
| Index key | Display term | A management identifier versus the form shown to the reader. |
| Working link | Meaningful link | A reachable destination versus the destination actually intended by the content. |
| Omission | Lacuna | An editorial error versus a passage not fully transmitted by tradition. |
| Variant | Textual error | A defensible alternative reading versus a corruption that needs repair. |
| Page style | Presentation profile | Rules for one kind of page versus a presentation system for one kind of edition. |
| Baseline | Latest version | A basis for comparison versus the most recent state. |
| Successful build | Successful validation | A product was produced versus a product meets its checks. |
| Quality assurance | Quality control | Building an error-preventing system versus testing a specific product. |
| Regression testing | Version diff | Checking that functions are preserved versus listing what changed. |
| Visually identical | Identical in content | Similar appearance versus genuinely similar content and data. |
| Consistency | Uniformity | Sharing principles versus looking the same. |
| Freeze | Sign-off | A pause on changes versus a justified conclusion of quality. |
| Final proof | Release | The object needing final review versus the product cleared for publication. |
| Book file | Project bundle | The product people read versus the source system used to produce, repair, and reprint it. |

## Ten foundational principles

### 1. Separate content from presentation

Content should be identified by its function before any presentation decision is made. A heading is a heading because of its role in the text, not because it is printed in large type. This principle makes it possible to change the design, trim size, or output format without reorganizing all the content.

### 2. Preserve the identity of content

A source unit must keep its identity within an established locator scheme, even when its position in the book changes. This is the foundation of lookup, cross-reference, collation, and scholarly revision.

### 3. Check relations, not only components

A note can be textually correct but placed at the wrong location. An index can be beautifully sorted yet lead to irrelevant pages. The quality of a book depends both on the quality of each part and on the correspondence between the parts.

### 4. Fix problems at their source

If an index entry is duplicated, fix how entries are managed in the source, not just delete the duplicate from the final index. If a table of contents lists a wrong page number, fix the mechanism that generates the contents, do not retype the number by hand. This addresses causes instead of hiding symptoms.

### 5. Standardize function, do not impose form

Components with the same function should be governed by shared principles. Yet a play, a philosophical work, and a textbook may each need different presentation. An extensible publishing system must know what should be shared and what must be designed per work.

### 6. Every change needs scope and justification

Not every improvement to one book belongs in the shared core. A title-local adjustment may serve only a particular need. A change should enter the shared parts only when its function is clear, reusable, and tested across the relevant publication types.

### 7. Do not use one kind of evidence to certify a different kind of quality

Having the full number of lines does not prove a translation is correct. A PDF opening does not prove every link is meaningful. Embedded fonts do not prove full accessibility. Each quality claim needs to be supported by the appropriate kind of evidence.

### 8. Repairability is part of quality

A good publishing system does not only produce a final product. It must allow tracing a problem, fixing it at the right scope, restoring a version, and rebuilding without unnecessary cost.

### 9. Distinguish uncertainty from error

In scholarly publishing, not every uncertainty can be resolved. Some questions about variants, transmission history, or interpretation remain open. The editor's responsibility is to identify, explain, and honestly record those uncertainties, rather than making the text artificially definite.

### 10. Quality must be proportionate to the cost of checking

A validation process should not become a bloated bureaucracy. Rule-governed, repetitive checks should be automated. Work requiring philological, scholarly, or aesthetic judgment deserves appropriate human effort. The goal is not the most checks, but trustworthy evidence through a lean, sustainable, extensible process.

## Term conventions across languages

The Vietnamese edition of this wiki uses a consistent set of translations. The table records them so future edits keep both languages aligned.

| English | Vietnamese |
| --- | --- |
| Publication Systems Engineering | Kỹ nghệ hệ thống xuất bản |
| Semantic structure | Cấu trúc logic của nội dung |
| Canonical locator | Định vị chuẩn |
| Anchor | Điểm neo |
| Marker | Dấu chỉ vị trí |
| Semantic edge | Quan hệ tham chiếu |
| Semantic alignment ledger | Sổ đối chiếu ngữ nghĩa |
| Normalization | Chuẩn hóa |
| Baseline | Mốc đối chiếu |
| Regression testing | Kiểm thử hồi quy |
| Render-diff | So sánh hình ảnh trang |
| Validator | Bộ kiểm định |
| Build | Tạo lập ấn bản |
| Resumable build | Tạo lập có thể tiếp tục |
| Artifact | Sản phẩm tạo lập |
| Manifest | Bảng kê |
| Checksum | Mã kiểm toàn vẹn |
| Freeze | Khóa trạng thái |
| Sign-off | Xác nhận hoàn tất |
| Proof | Bản đọc soát |
| Release | Phát hành |
| Definition of done | Điều kiện hoàn tất |
| Postmortem | Báo cáo tổng kết kỹ thuật |

Proper names and technical standard names are not translated: PSE, PDF, EPUB, XMP, Unicode, and LaTeX keep their original form in both languages.

## Scope of the glossary

This glossary is a proposal for conceptual standardization. It is grounded in the technical postmortems of real production projects and in the development direction of PSE, supplemented with general publishing and software-engineering concepts to form a coherent system.

It is not yet a specification of features that exist in the PSE source code. Mechanisms such as the shared canonical-locator model, per-scheme validators, link semantic reconciliation, or resumable builds still need to be checked against the actual implementation before documentation can present them as finished features.

Over the long term, the value of this glossary is not only in explaining technical vocabulary. It can become the shared conceptual foundation of PSE, giving authors, translators, editors, designers, and software developers one common language for discussing how a book is made and what makes it trustworthy.

Related layers: the term tables in [Textual scholarship](textual-scholarship.md) through [Quality assurance and release](quality-assurance.md).
