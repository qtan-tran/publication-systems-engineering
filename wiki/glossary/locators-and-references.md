---
title: Locators and References
description: Canonical locators, anchors, tables of contents, indexes, and the reference relations that let a reader find exactly one passage again.
---

# Locators and references

A scholarly book is not only a sequence of pages read in order. It is also a network of relations that lets a reader move from an idea, a concept, or a note to the relevant location. A good locator system must let the reader find exactly one passage again, even when the visual form of the book changes.

## Identifiers, anchors, and markers

| Term | Explanation |
| --- | --- |
| **Locator** | A piece of information that identifies the position of content, such as a page number, chapter number, verse-line number, or paragraph ID. |
| **Canonical locator** | An identifier under a reference convention established for the work or source edition. It does not change just because the book is reflowed or printed in another trim. |
| **Locator scheme** | The set of rules that defines how the units of a text are numbered, organized, and referenced. |
| **Locator set** | The set of all locators expected, or actually present, in a text. Comparing two sets reveals positions that are missing, extra, or wrong. |
| **Anchor** | An address placed at a specific position inside an electronic document. Links can use this address to bring the reader to exactly the right passage. Anchors are usually invisible. |
| **Marker** | A visible symbol that helps the reader know where they are in the text, for example verse-line numbers printed in the margin. |
| **Destination** | The position that a link or lookup action brings the reader to. |
| **Duplicate anchor** | Two or more different positions using the same anchor identifier, which can make the destination ambiguous or wrong. |
| **Missing anchor** | An address that should exist but was not created, leaving part of the content unreachable through the reference system. |
| **Folio** | The page number printed on the page, usually at the head or foot. It is not necessarily the same as the physical page index inside the PDF file. |

### Distinguishing four nearby concepts

Consider verse line 815 of a Greek drama: the **canonical locator** is the number 815 under the convention of the source edition; the **technical address** of the anchor, for example `sourceverse.815`, is the machine-readable address; the **printed marker** is the number 815 the reader sees in the margin; the **page number** 42 belongs to the specific edition. When the book is reflowed, verse 815 may move from page 42 to page 45: the canonical locator is still 815, but the physical position of the anchor, the marker, and the page number need to be updated accordingly. These four concepts are tightly related but not identical.

## Different locator schemes

| Edition type | Locator scheme in use | Example |
| --- | --- | --- |
| Platonic dialogue | Stephanus numbers | 80d |
| Aristotelian work | Bekker numbers | 1094a1 |
| Greek drama | Verse numbers from the source edition | 815 |
| Numbered scripture | Chapter and verse | 3.12 |
| Scholarly monograph | Chapters, sections, subsections | 2.3.1 |
| Textbook | Lessons, exercises | Lesson 12, exercise 4 |

## Shared locator architecture

**The canonical locator abstraction** is an architectural principle that lets PSE manage many locator schemes with one general mechanism, without imposing one numbering rule on every work. For example, PSE can understand that both Plato's `80d` and a Greek drama's `815` are source locators, while recognizing that they belong to two different conventions.

**A locator-scheme validator** is the mechanism that checks the validity of locators under the rules of each text type: the validator for Stephanus numbers is not the validator for verse numbers, and neither is the validator for a chapter/section/subsection structure.

This is standardization done right: **share the architectural principle, preserve the distinct conventions of each text**.

### The semantic alignment ledger

A **semantic alignment ledger** is a structured record of the relations between each source unit, the translation, the speaker, the anchor, the position in the edition, and the verification result. A simplified example:

| Source locator | Speaker | Translation unit | Page | Content check |
| --- | --- | --- | --- | --- |
| 810 | Speaker A | Identified | 42 | Verified |
| 811 | Speaker B | Identified | 42 | Needs check |
| 812 | Speaker A | Identified | 42 | Verified |
| 813 | Speaker A | Unconfirmed | 43 | Open |

The table shows that a unit can be fully located technically while still unverified in content. The ledger is not a second translation; it is a body of evidence that tells the editor how far each part of the text has been processed.

In the technical postmortems of real production projects, the shared locator model, the alignment ledger, and per-scheme validators were proposed as reusable improvements for PSE; they are not yet confirmed as fully implemented core features.

## Components of the lookup system

| Term | Explanation |
| --- | --- |
| **Table of contents** | The list of the parts of the book, showing the hierarchical structure and starting positions. |
| **Outline** | A navigable hierarchy of parts that a PDF reader can open to move quickly between chapters and sections. |
| **Bookmark** | A selectable entry in the navigation system of an electronic document. In PDF production, bookmarks usually form the outline tree. |
| **Link** | A mechanism that moves the reader from one position to another, within the same book or to an external document. |
| **Cross-reference** | A pointer from the current content to other related content, for example "see chapter 3" or "see the note on line 815". It can exist in both print and electronic books. |
| **Reverse link** | A link that allows returning to the starting position, for example from a note back to the passage being read. |
| **Note key** | The internal identifier of a note, letting the system recognize it even when the displayed numbering changes. |
| **Index key** | The identifier used to collect and sort the occurrences of a term in the index. |
| **Index entry** | A person, place, event, or concept presented in the index, together with the relevant locations. |
| **Subentry** | A component under a main entry, distinguishing different aspects of the same subject. |
| **Display term** | The form in which a term actually appears to the reader. It can differ from the internal key used for management and sorting. |
| **PDF PageLabels** | The information that lets a PDF reader display page names or numbers by the book's convention, for example "Cover", "iv", or "1", instead of counting from the first page of the file. |

## Semantic relations

A **semantic edge** is a meaningful relation between two content components. For example, a note about a place name is linked to the passage in the main text that mentions that place. What must be guaranteed is not only that the link works, but that it leads to exactly the content it should explain.

| Term | Explanation |
| --- | --- |
| **Technical link check** | Verifying that a link exists, works, and has a valid destination. |
| **Link semantic reconciliation** | Checking whether a link brings the reader to the object that is intended, in content terms. |
| **Diff semantic edges** | Comparing the relation network between two versions to find links that were added, removed, changed, or retargeted. |
| **Folio consistency** | The correspondence between the printed page numbers, the table of contents, the index, PDF page labels, and link destinations. |
| **TOC/folio consistency** | Checking that each contents entry lists the right page number and points to the right start position of the corresponding part. |
| **Glossary/index normalization** | Unifying spelling, transliteration, sorting, the management of alternative names, and entry hierarchy, avoiding duplicate or inconsistent entries. |

### Why both meaning and technique must be checked

Suppose a note links to page 42. Clicking it really opens page 42: technically, the link works. However, after a translation revision, the passage that needs the note has moved to page 43; the link is no longer meaningful.

The same applies to link counts: a new version having five fewer links does not prove five links broke; duplicate links may have been removed, or line wrapping may have changed.

**What needs checking is the relation between pieces of content, not just the number of links.**

Related pages: [Semantic structure](semantic-structure.md), [Quality assurance and release](quality-assurance.md).
