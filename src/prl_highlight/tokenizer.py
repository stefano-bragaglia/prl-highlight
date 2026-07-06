"""Tokenize source text with a TextMate grammar, for grammar regression tests."""

from __future__ import annotations

import json
from pathlib import Path

from textmate_grammar.parsers.base import LanguageParser

DEFAULT_GRAMMAR_PATH = Path(__file__).resolve().parent / "grammar" / "prl.tmLanguage.json"


def tokenize(
    source: str, grammar_path: str | Path | None = None
) -> list[tuple[str, tuple[str, ...]]]:
    """Tokenize `source` with the TextMate grammar at `grammar_path`.

    Returns a flat, depth-first list of ``(text, scopes)`` pairs, one per
    leaf token the grammar produces. ``scopes`` is the ancestor scope chain
    from outermost (the grammar's own ``scopeName``) to innermost, in order.
    Only text actually captured by a matched pattern appears — characters
    consumed solely by a ``begin``/``end`` delimiter with no capturing
    pattern of its own are not included as separate entries, matching the
    underlying library's own behavior.

    :param source: PRL source text to tokenize. Empty string returns [].
    :param grammar_path: path to a TextMate grammar JSON file. Defaults to
        this repo's own bundled ``prl.tmLanguage.json``.
    :raises FileNotFoundError: if the grammar file does not exist.
    :raises ValueError: if the grammar file is not valid JSON.
    """
    path = Path(grammar_path) if grammar_path is not None else DEFAULT_GRAMMAR_PATH
    if not path.is_file():
        raise FileNotFoundError(f"grammar file not found: {path}")
    grammar = json.loads(path.read_text())

    if not source:
        return []

    parser = LanguageParser(grammar)
    parsed = parser.parse_string(source)

    tokens: list[tuple[str, tuple[str, ...]]] = []
    _collect(parsed, (parsed.token,), tokens)
    return tokens


def _collect(
    element, scopes: tuple[str, ...], tokens: list[tuple[str, tuple[str, ...]]]
) -> None:
    children = element.children
    if not children:
        if element.content:
            tokens.append((element.content, scopes))
        return
    for child in children:
        _collect(child, (*scopes, child.token), tokens)
