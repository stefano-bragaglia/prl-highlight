from .helpers import parse, scoped_tokens


def test_traditional_pattern_parens_and_dollar_binding():
    parsed = parse(
        'rule "x"\nwhen\n  $app: Application(status == "pending")\nthen\nend\n'
    )
    parens = scoped_tokens(parsed, "punctuation.section.pattern.prl")
    assert "(" in parens
    assert ")" in parens
    bindings = scoped_tokens(parsed, "punctuation.separator.binding.prl")
    assert ":" in bindings


def test_bare_identifier_binding_same_colon_scope():
    parsed = parse(
        'rule "x"\nwhen\n  loan: LoanApplication(amount > 1000)\nthen\nend\n'
    )
    assert ":" in scoped_tokens(parsed, "punctuation.separator.binding.prl")


def test_oopath_delimiters_share_traditional_scope():
    parsed = parse('rule "x"\nwhen\n  /Vehicle[year < 2010]\nthen\nend\n')
    section = scoped_tokens(parsed, "punctuation.section.pattern.prl")
    assert "/" in section
    assert "[" in section
    assert "]" in section


def test_no_binding_prefix_produces_no_binding_token():
    parsed = parse('rule "x"\nwhen\n  Temperature(value > 30)\nthen\nend\n')
    assert scoped_tokens(parsed, "punctuation.separator.binding.prl") == []
    assert "(" in scoped_tokens(parsed, "punctuation.section.pattern.prl")
