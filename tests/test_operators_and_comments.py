from .helpers import has_scope, parse, scoped_tokens


def _rule_with(condition: str) -> str:
    return f'rule "x"\nwhen\n  Foo({condition})\nthen\nend\n'


def test_each_comparison_operator_is_one_token():
    for op in ("==", "!=", "<", "<=", ">", ">="):
        parsed = parse(_rule_with(f"age {op} 18"))
        assert has_scope(parsed, "keyword.operator.comparison.prl", op)


def test_line_comment_does_not_swallow_next_line():
    parsed = parse('// a comment\nrule "x"\nwhen\nthen\nend\n')
    assert has_scope(parsed, "comment.line.double-slash.prl", "// a comment")
    assert has_scope(parsed, "keyword.control.prl", "rule")


def test_url_like_string_does_not_start_a_comment():
    parsed = parse(_rule_with('url == "http://example.com"'))
    assert scoped_tokens(parsed, "comment.line.double-slash.prl") == []
    assert has_scope(parsed, "string.quoted.double.prl", '"http://example.com"')


def test_block_comment_spans_multiple_lines():
    parsed = parse("/* line one\nline two\nline three */\n")
    tokens = scoped_tokens(parsed, "comment.block.prl")
    assert any("line one" in t and "line three" in t for t in tokens)
