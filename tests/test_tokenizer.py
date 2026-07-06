from pathlib import Path

import pytest

from prl_highlight.tokenizer import tokenize

DUMMY_GRAMMAR = Path(__file__).parent / "fixtures" / "dummy_grammar.json"


def test_tokenize_basic_scope():
    tokens = tokenize("foo bar", grammar_path=DUMMY_GRAMMAR)
    assert ("foo", ("source.dummy", "keyword.control.dummy")) in tokens
    assert ("bar", ("source.dummy", "text.plain.dummy")) in tokens


def test_tokenize_empty_string_returns_empty_list():
    assert tokenize("", grammar_path=DUMMY_GRAMMAR) == []


def test_tokenize_missing_grammar_raises():
    with pytest.raises(FileNotFoundError):
        tokenize("foo", grammar_path=Path("/no/such/grammar.json"))


def test_tokenize_invalid_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not valid json")
    with pytest.raises(ValueError):
        tokenize("foo", grammar_path=bad)


def test_tokenize_preserves_source_order():
    tokens = tokenize("foo bar baz", grammar_path=DUMMY_GRAMMAR)
    texts = [text for text, _ in tokens]
    assert texts == ["foo", "bar", "baz"]
