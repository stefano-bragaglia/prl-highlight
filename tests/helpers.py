"""Shared tokenizing helpers for prl-grammar's own Stage A tests.

Not the reusable public helper that grammar-test-harness ships (that
feature is being built on a separate branch) - a small local utility
scoped to this feature's tests only.
"""
from __future__ import annotations

import json
from pathlib import Path

from textmate_grammar.elements import ContentElement
from textmate_grammar.parsers.base import LanguageParser

GRAMMAR_PATH = Path(__file__).parent.parent / "src/prl_highlight/grammar/prl.tmLanguage.json"


def parse(text: str) -> ContentElement:
    """Parse *text* with the real, on-disk PRL grammar."""
    grammar = json.loads(GRAMMAR_PATH.read_text())
    parser = LanguageParser(grammar)
    return parser.parse_string(text)


def register_stub_python() -> None:
    """Register a minimal stand-in for source.python.

    The real vendored MagicPython grammar fails to load in this test
    library (an Oniguruma-binding incompatibility, not a PyCharm-side
    issue) - see embedded-python-rhs tests for the full explanation.
    """
    stub = {
        "scopeName": "source.python",
        "patterns": [
            {"match": r"#[^\n]*", "name": "comment.line.number-sign.python"},
            {"match": r"\"[^\"]*\"", "name": "string.quoted.double.python"},
            {"match": r"'[^']*'", "name": "string.quoted.single.python"},
            {"match": r"[^\s]+", "name": "source.python.plain"},
        ],
    }
    LanguageParser(stub)


def scoped_tokens(parsed: ContentElement, scope: str) -> list[str]:
    """Return the text content of every token carrying *scope*."""
    return [element.content for element, _ in parsed.find(tokens=scope)]


def has_scope(parsed: ContentElement, scope: str, content: str | None = None) -> bool:
    """True if *scope* occurs anywhere, optionally restricted to *content*."""
    tokens = scoped_tokens(parsed, scope)
    return content in tokens if content is not None else bool(tokens)
