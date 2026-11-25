---
title: A Complete Worked Example
description: Build a five-chapter Ancient Greek textbook with public-domain illustrations, from an empty folder to a checked PDF.
---

# A complete worked example: an Ancient Greek textbook

This page walks the whole [Beginner Handbook](index.md) path on one real, finished project: a five-chapter introductory textbook for teaching Ancient Greek, with two photographs and a historical manuscript scan as illustrations. Every command below is a single line you paste into a terminal, and every file edit is ordinary text editing. No programming is involved.

The finished project is published in the PSE repository, so you can compare your own work against it at any point: <https://github.com/qtan-tran/publication-systems-engineering/tree/main/examples/tutorials/greek-textbook>. Its chapters are deliberately small so that the whole book fits on one screen of your attention.

## What the finished book contains

- five chapters, each in its own file under `content/`: why learn Greek, the alphabet, first nouns, the present tense, and a first reading of real Greek;
- a table of contents that PSE builds automatically, an index of key terms, and an Image Credits page in the back matter;
- polytonic Ancient Greek set with a full Greek font, so accents and breathing marks display correctly;
- three public-domain illustrations from Wikimedia Commons;
- a PDF produced and machine-checked with the exact commands shown on this page.

## Step 0. Prepare the workstation

Follow [Install and check PSE](install.md) first, and stop only after `pse doctor` passes. You need an internet connection for the image downloads in Step 3.

## Step 1. Create the project

Create projects in **private storage**, outside the PSE repository. In a terminal, run:

```text
pse new /path/to/private-projects \
  --profile academic-monograph \
  --title "Ancient Greek for Beginners" \
  --author "Alexandros Didaskalos" \
  --language en \
  --publication-year 2027 \
  --slug greek-textbook \
  --non-interactive
```

On PowerShell, put the command on one line instead of using the backslash continuation shown above.

Two remarks for this book in particular:

- `academic-monograph` is the supported profile for textbooks and any structured nonfiction. If you were looking for a profile named `academic-book` or `textbook`, this is the one to use.
- The options in the command are the same values the generator asks for interactively when you leave them out. `--non-interactive` skips the questions, which is also the right choice when the terminal cannot ask (for example inside a script).

`pse new` prints the directory it created; change into it. Then open `book.yml` in your text editor and add one further line of metadata under `title`:

```text
subtitle: A Complete Textbook
```

## Step 2. Write the chapters

The generator creates starter chapters. A chapter is one plain-text file, `content/chapter-01.tex`, `content/chapter-02.tex`, and so on. Open each one and replace the starter text with your own, keeping the same simple shape:

- the file starts with the chapter heading, for example `\chapter{Why Learn Ancient Greek?}`;
- paragraphs are lines of text separated by one blank line;
- a section heading inside the chapter is `\section{...}` in the same style;
- a page footnote is wrapped in `\footnote{...}` at the point where the note marker belongs.

The demo book uses five chapters: *Why Learn Ancient Greek?*, *The Alphabet and Sounds*, *First Nouns and the Article*, *The Present Tense*, and *Reading Real Greek*. Chapter 2 contains a table of the letters; Chapter 3 declines the noun `\PSEGreek{λόγος}`; keep tables exactly as the starter files show them and simply replace the words inside.

Finally, open `main.tex` in the project root and give the book its chapter list: one `\input` line per chapter, in reading order, replacing the starter lines:

```tex
\input{content/chapter-01.tex}
\input{content/chapter-02.tex}
\input{content/chapter-03.tex}
\input{content/chapter-04.tex}
\input{content/chapter-05.tex}
```

Chapter order is the order of these lines; nothing else needs to change in `main.tex` at this point.

## Step 3. Add public-domain illustrations

Create a folder named `assets` in the project root if the generator did not create one. Then, from the project root, fetch the three illustrations used by the demo:

```text
curl -sL -o assets/parthenon-west.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Parthenon_from_west.jpg"
curl -sL -o assets/homer-bm-1825.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Bust%20Homer%20BM%201825.jpg"
curl -sL -o assets/greek-manuscript-6c.png "https://commons.wikimedia.org/wiki/Special:FilePath/Greek%20manuscript%20cursive%206th%20century.png"
```

You can equally well download the images in your browser and save them into `assets`. All three works are in the public domain, which is why a book may reprint them without a permission process. Whatever images you use, keep only images you have the right to reproduce, and write down the source of each one.

A picture enters a chapter as a figure block. This one, from Chapter 1, places the Parthenon photograph with its caption:

```tex
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.86\linewidth]{assets/parthenon-west.jpg}
  \caption{The Parthenon on the Acropolis of Athens, seen from the west.
  The classical city produced the dialect this book teaches.}
\end{figure}
```

The width is a fraction of the printed text width; `0.6\linewidth` gives the smaller, centered treatment used for the Homer bust. The caption always appears under the printed image.

Credit the images in the back matter so the printed book documents its own sources. In `main.tex`, after the last `\input` line and before `\PSEPrintIndex`, the demo book has:

```tex
\PSEBeginBackMatter
\chapter*{Image Credits}
\addcontentsline{toc}{chapter}{Image Credits}
The illustrations in this book come from Wikimedia Commons and are in the
public domain: the Parthenon photograph (Chapter 1), the British Museum
bust of Homer (Chapter 1), and the sixth-century Greek cursive manuscript
(Chapter 5).
\PSEPrintIndex
```

## Step 4. Type Ancient Greek with full accents

Polytonic Greek uses breathings and accents that ordinary body fonts do not always carry. PSE solves this with its `multilingual` semantic module and a Greek-complete font. Open `config/semantic-modules.json` in the project and add `multilingual` to the activate list:

```json
{
  "schema_version": "1.1",
  "activate": ["multilingual"],
  "deactivate": [],
  "config": {}
}
```

Then wrap every run of Greek text in `\PSEGreek{...}`. Inside a sentence it looks like this (Chapter 3):

```tex
The word \PSEGreek{λόγος} (word, account) shows the endings of a whole
family of masculine nouns.
```

And a whole quotation in Chapter 5 reads:

```tex
\PSEGreek{ὁ} \PSEGreek{ἄνθρωπος} \PSEGreek{ἐν} \PSEGreek{τῇ} \PSEGreek{οἰκίᾳ}
\PSEGreek{γράφει} \PSEGreek{τὸν} \PSEGreek{λόγον} \PSEGreek{τῷ} \PSEGreek{βιβλίῳ}.
```

!!! note "Fonts on your machine"
    The module relies on a Greek-complete font family (PSE uses Gentium Plus by default). Most TeX distributions ship it; if Greek letters are missing or look wrong in the PDF, see [Install and check PSE](install.md) for the font package to add, then run `pse build .` again.

## Step 5. Build and check

From the project root, run the standard trio:

```text
pse build .
pse check . --human
pse inspect-output .
```

What each command contributes:

- `pse build .` runs the typesetting and writes the working PDF to `build/book.pdf`. Repeat it after any edit; a repeat build is always safe.
- `pse check . --human` prints machine findings at the four PSE levels. Fix every `error` before moving on; give `warning` items your attention; `review` items call for your editorial judgement. See [Build and check your PDF](build-and-check.md) for how to read the report.
- `pse inspect-output .` records the finished-PDF inspection baseline (metadata, navigation, text extractability).

Open `build/book.pdf` and look at it. Machine checks cannot decide every typographic question; your eyes are part of the finished loop.

## Step 6. What to see in the finished PDF

- the table of contents lists the five chapters and appears in the front matter;
- Chapter 1 shows the Parthenon photograph with its caption, and the bust of Homer;
- Chapter 5 shows the sixth-century manuscript page;
- Greek words such as ἄνθρωπος print with their breathing marks intact;
- the index at the back collects the key terms marked with `\PSEIndex{...}` in the chapters.

## If something goes wrong

- **`LuaLaTeX is not available on PATH.`** Your computer has no TeX distribution installed yet. Follow [Install and check PSE](install.md), then confirm with `pse doctor`.
- **A build message names a file under `assets/`.** Check that the image exists in the project's `assets` folder and that its filename matches the `\includegraphics` line exactly.
- **Greek text prints without its accents.** Check Step 4: the `multilingual` module must be listed in `config/semantic-modules.json`.
- Anything else: [First troubleshooting](troubleshooting.md).

Finished? Continue with [Where to go next](next-steps.md).
