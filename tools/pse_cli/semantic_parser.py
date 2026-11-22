from __future__ import annotations

from bisect import bisect_right
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ParseLimits:
    """Conservative parser limits for source diagnostics.

    The parser is deliberately not a TeX engine. These limits bound work on
    pathological or accidental inputs while remaining far above normal book
    source sizes.
    """

    max_file_bytes: int = 8 * 1024 * 1024
    max_group_depth: int = 128
    max_argument_chars: int = 1_000_000
    max_nodes_per_file: int = 100_000
    max_errors_per_file: int = 1_000


DEFAULT_LIMITS = ParseLimits()


@dataclass(frozen=True)
class SourceLoc:
    file: str
    line: int
    column: int
    offset: int


@dataclass(frozen=True)
class SemanticNode:
    kind: str
    name: str
    args: tuple[str, ...]
    loc: SourceLoc


class ParseError(Exception):
    def __init__(self, message: str, loc: SourceLoc, *, code: str = "parse_error"):
        super().__init__(message)
        self.message = message
        self.loc = loc
        self.code = code


def _line_starts(text: str) -> list[int]:
    starts = [0]
    for idx, ch in enumerate(text):
        if ch == "\n":
            starts.append(idx + 1)
    return starts


def _line_col(line_starts: list[int], offset: int) -> tuple[int, int]:
    idx = bisect_right(line_starts, offset) - 1
    idx = max(idx, 0)
    return idx + 1, offset - line_starts[idx] + 1


def _loc(file: str, line_starts: list[int], offset: int) -> SourceLoc:
    line, col = _line_col(line_starts, max(offset, 0))
    return SourceLoc(file=file, line=line, column=col, offset=max(offset, 0))


def _is_escaped(text: str, i: int) -> bool:
    """Return whether character at i is preceded by an odd run of backslashes."""
    j = i - 1
    count = 0
    while j >= 0 and text[j] == "\\":
        count += 1
        j -= 1
    return bool(count % 2)


def _skip_ws_comments(text: str, i: int) -> int:
    n = len(text)
    while i < n:
        if text[i].isspace():
            i += 1
            continue
        if text[i] == "%" and not _is_escaped(text, i):
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        break
    return i


def _read_group(
    text: str,
    i: int,
    file: str,
    line_starts: list[int],
    limits: ParseLimits,
) -> tuple[str, int]:
    i = _skip_ws_comments(text, i)
    if i >= len(text) or text[i] != "{":
        raise ParseError(
            "Expected braced argument.",
            _loc(file, line_starts, min(i, max(len(text) - 1, 0))),
            code="expected_braced_argument",
        )
    start = i
    i += 1
    depth = 1
    out: list[str] = []
    while i < len(text):
        if i - start > limits.max_argument_chars:
            raise ParseError(
                f"Semantic argument exceeds parser limit ({limits.max_argument_chars} characters).",
                _loc(file, line_starts, start),
                code="argument_too_large",
            )
        ch = text[i]
        if ch == "%" and not _is_escaped(text, i):
            j = text.find("\n", i)
            if j < 0:
                raise ParseError(
                    "Unclosed braced argument.",
                    _loc(file, line_starts, start),
                    code="unclosed_braced_argument",
                )
            out.append("\n")
            i = j + 1
            continue
        if ch == "\\":
            if i + 1 < len(text):
                out.append(ch)
                out.append(text[i + 1])
                i += 2
                continue
            out.append(ch)
            i += 1
            continue
        if ch == "{":
            depth += 1
            if depth > limits.max_group_depth:
                raise ParseError(
                    f"Semantic argument exceeds maximum brace depth ({limits.max_group_depth}).",
                    _loc(file, line_starts, i),
                    code="brace_depth_exceeded",
                )
            out.append(ch)
            i += 1
            continue
        if ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(out), i + 1
            out.append(ch)
            i += 1
            continue
        out.append(ch)
        i += 1
    raise ParseError(
        "Unclosed braced argument.",
        _loc(file, line_starts, start),
        code="unclosed_braced_argument",
    )


COMMAND_ARITY = {
    "PSELocator": 1,
    "PSELocatorNS": 2,
    "PSELocatorRef": 1,
    "PSELocatorRefNS": 2,
    "PSELocatorRangeRef": 2,
    "PSELocatorRangeRefNS": 3,
    "PSEApparatusEntry": 3,
    "PSEExplanatoryNote": 2,
    "PSEApparatusRangeEntry": 4,
    "PSEApparatusStreamEntry": 4,
    "PSEApparatusStreamRangeEntry": 5,
    "PSEDramaLine": 1,
    "PSEDramaLineRef": 1,
    "PSEDramaLineRangeRef": 2,
    "PSEDeclareSpeaker": 2,
    "PSEAct": 2,
    "PSEScene": 2,
    "PSEStageDirection": 1,
    "PSEParallelSegment": 3,
    "PSEParallelAlign": 3,
    "PSEParallelTranslationNote": 2,
    "PSEParallelAlignmentLocator": 2,
    "PSEParallelNote": 3,
}
ENV_ARITY = {"PSESpeech": 1}
OPTIONAL_COMMAND_SIGNATURES = {"PSEVerseLine": (1, 1)}  # required-before, optional bracket, required-after



def _read_optional_bracket(text: str, i: int, file: str, line_starts: list[int], limits: ParseLimits) -> tuple[str, int]:
    i = _skip_ws_comments(text, i)
    if i >= len(text) or text[i] != "[":
        return "", i
    start = i
    i += 1
    depth = 1
    out: list[str] = []
    while i < len(text):
        if i - start > limits.max_argument_chars:
            raise ParseError("Optional semantic argument exceeds parser limit.", _loc(file, line_starts, start), code="argument_too_large")
        ch = text[i]
        if ch == "%" and not _is_escaped(text, i):
            j = text.find("\n", i)
            if j < 0:
                raise ParseError("Unclosed optional argument.", _loc(file, line_starts, start), code="unclosed_optional_argument")
            out.append("\n"); i = j + 1; continue
        if ch == "[" and not _is_escaped(text, i):
            depth += 1
        elif ch == "]" and not _is_escaped(text, i):
            depth -= 1
            if depth == 0:
                return "".join(out), i + 1
        out.append(ch); i += 1
    raise ParseError("Unclosed optional argument.", _loc(file, line_starts, start), code="unclosed_optional_argument")

def parse_text(
    text: str,
    file: str,
    *,
    limits: ParseLimits = DEFAULT_LIMITS,
) -> tuple[list[SemanticNode], list[ParseError]]:
    nodes: list[SemanticNode] = []
    errors: list[ParseError] = []
    i = 0
    n = len(text)
    starts = _line_starts(text)

    while i < n:
        if len(nodes) >= limits.max_nodes_per_file:
            errors.append(
                ParseError(
                    f"Semantic node count exceeds parser limit ({limits.max_nodes_per_file}).",
                    _loc(file, starts, i),
                    code="node_limit_exceeded",
                )
            )
            break
        if len(errors) >= limits.max_errors_per_file:
            break
        ch = text[i]
        if ch == "%" and not _is_escaped(text, i):
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if ch != "\\":
            i += 1
            continue
        start = i
        i += 1
        if i >= n:
            break
        if text[i].isalpha() or text[i] == "@":
            j = i
            while j < n and (text[j].isalpha() or text[j] == "@"):
                j += 1
            name = text[i:j]
            i = j
        else:
            name = text[i]
            i += 1

        if name == "begin":
            try:
                env, i2 = _read_group(text, i, file, starts, limits)
                i = i2
                if env in ENV_ARITY:
                    args: list[str] = []
                    for _ in range(ENV_ARITY[env]):
                        a, i = _read_group(text, i, file, starts, limits)
                        args.append(a)
                    nodes.append(
                        SemanticNode(
                            "environment_begin",
                            env,
                            tuple(args),
                            _loc(file, starts, start),
                        )
                    )
            except ParseError as exc:
                errors.append(exc)
                i = max(i, start + 1)
            continue

        optional_sig = OPTIONAL_COMMAND_SIGNATURES.get(name)
        if optional_sig is not None:
            args = []
            try:
                before, after = optional_sig
                for _ in range(before):
                    a, i = _read_group(text, i, file, starts, limits); args.append(a)
                opt, i = _read_optional_bracket(text, i, file, starts, limits); args.append(opt)
                for _ in range(after):
                    a, i = _read_group(text, i, file, starts, limits); args.append(a)
                nodes.append(SemanticNode("command", name, tuple(args), _loc(file, starts, start)))
            except ParseError as exc:
                errors.append(exc); i = max(i, start + 1)
            continue
        arity = COMMAND_ARITY.get(name)
        if arity is None:
            continue
        args = []
        try:
            for _ in range(arity):
                a, i = _read_group(text, i, file, starts, limits)
                args.append(a)
            nodes.append(
                SemanticNode("command", name, tuple(args), _loc(file, starts, start))
            )
        except ParseError as exc:
            errors.append(exc)
            i = max(i, start + 1)
    return nodes, errors


def parse_files(
    paths: Iterable[Path],
    root: Path,
    *,
    limits: ParseLimits = DEFAULT_LIMITS,
) -> tuple[list[SemanticNode], list[ParseError]]:
    nodes: list[SemanticNode] = []
    errors: list[ParseError] = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
        except OSError as exc:
            errors.append(ParseError(f"Could not stat source file: {exc}", SourceLoc(rel, 1, 1, 0), code="source_io_error"))
            continue
        if size > limits.max_file_bytes:
            errors.append(
                ParseError(
                    f"Source file exceeds parser limit ({limits.max_file_bytes} bytes).",
                    SourceLoc(rel, 1, 1, 0),
                    code="file_too_large",
                )
            )
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            errors.append(
                ParseError(
                    f"Source file is not valid UTF-8: {exc}",
                    SourceLoc(rel, 1, 1, 0),
                    code="invalid_utf8",
                )
            )
            continue
        ns, es = parse_text(text, rel, limits=limits)
        nodes.extend(ns)
        errors.extend(es)
    return nodes, errors


def loc_dict(loc: SourceLoc) -> dict:
    return asdict(loc)
