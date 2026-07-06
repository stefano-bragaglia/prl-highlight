"""Broad safety net: every vendored fixture, tokenized end to end, must not
have any non-whitespace token fall back to the grammar's bare root scope
(source.prl with nothing more specific) - that would mean something in a
real .prl file isn't recognized by the grammar at all.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from prl_highlight.tokenizer import tokenize

FIXTURES = sorted((Path(__file__).parent / "fixtures" / "prl_examples").glob("*.prl"))


@pytest.mark.parametrize("fixture_path", FIXTURES, ids=lambda p: p.name)
def test_no_bare_scope_tokens(fixture_path: Path):
    tokens = tokenize(fixture_path.read_text())
    unmatched = [
        (index, text)
        for index, (text, scopes) in enumerate(tokens)
        if text.strip() and len(scopes) <= 1
    ]
    assert not unmatched, (
        f"{fixture_path.name}: token(s) fell back to the bare root scope "
        f"(no more specific scope applied) - first at token index "
        f"{unmatched[0][0]}: {unmatched[0][1]!r}"
    )
