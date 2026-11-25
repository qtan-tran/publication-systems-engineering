---
title: Typography and Layout
description: Concepts of typesetting, page layout, presentation profiles, and function-based design in PSE.
---

# Typography and layout

This group focuses on how content becomes a readable visual form, while each edition, and the whole shelf of books, keeps its own design identity.

| Term | Explanation |
| --- | --- |
| **Typesetting** | The process of turning organized content into finished book pages under rules for type, margins, spacing, layout, and pagination. |
| **Typography** | The art and system of principles for using typeface, size, weight, spacing, and arrangement of text to support reading. |
| **Visual hierarchy** | Using size, position, weight, and white space to help the reader recognize the role and importance of each component. |
| **Role-based type scale** | A type-size system established by content role: body text, headings, notes, glossary, chronology, bibliography, and index. |
| **Leading** | The vertical space between lines of type, usually measured between consecutive baselines. |
| **Trim size** | The final physical size of a book page after trimming. |
| **Text block** | The main area of the page reserved for text content. |
| **Inner margin** | The white space on the side nearest the spine. |
| **Outer margin** | The white space on the side opposite the spine, which can hold margin markers or side notes. |
| **Recto/verso** | The two page types of an open book. They usually have margin layouts mirrored across the spine. |
| **Header** | The zone above the text block, which can hold the work title, chapter title, or navigational information. |
| **Footer** | The zone below the text block, usually for page numbers or auxiliary information. |
| **Index heading** | A heading dividing groups of index entries, usually letters A, B, C, or a thematic group. |
| **Page style** | The set of rules governing headers, footers, page numbers, and other repeating elements. |
| **Font embedding** | Including the needed font data inside the PDF so readers can view the document as intended without having the fonts installed. |
| **Vector graphics** | Images described by lines and geometry, which can be enlarged without the pixelation of raster images. |
| **Colophon** | The section recording production information, such as typesetting tools, fonts, design, version, and the parties involved. |

## Design by function, not by manual formatting

If every heading is adjusted individually with direct formatting, components sharing a role easily drift apart in unintended ways. When design follows function instead, components with the same role share one rule: every chapter heading, every note, every table takes its form from the definition of its role.

A role-based type scale does not mean every part of a book uses one size, nor that every book on the shelf must look identical. In a real production project, body text, a chronology, and a bibliography were each adjusted to their own reading needs and information density. This is an example of a design system that has shared rules while allowing intended, recorded exceptions.

## Concepts of PSE design architecture

| Term | Explanation |
| --- | --- |
| **Template** | A reusable configuration or rule set for producing books with a consistent appearance. |
| **Presentation profile** | A set of rules suited to one publication type, for example drama, textbooks, or scholarly monographs. |
| **Semantic module** | A reusable functional component, such as a glossary, chronology, critical apparatus, or index. |
| **Shared core** | The rules, tools, and foundational functionality used by many book projects. |
| **Title-local override** | A change applied to only one title, meeting a particular need without altering the shared rules of the other books. |
| **Design exception** | A deliberate decision not to follow a default rule, grounded in specific content, aesthetic, or functional reasons. |

**Consistency does not mean uniformity.** An extensible publishing system must allow different titles to keep their own character within a shared design architecture.

Related pages: [Build and versioning](build-and-versioning.md), the profile overview in [Book Profiles](../profiles/index.md).
