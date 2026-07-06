from .helpers import has_scope, parse


def _rule_with(condition: str) -> str:
    return f'rule "x"\nwhen\n  Foo({condition})\nthen\nend\n'


def test_double_quoted_string():
    parsed = parse(_rule_with('status == "pending"'))
    assert has_scope(parsed, "string.quoted.double.prl", '"pending"')


def test_single_quoted_string():
    parsed = parse(_rule_with("status == 'pending'"))
    assert has_scope(parsed, "string.quoted.single.prl", "'pending'")


def test_integer_and_float_are_one_token_each():
    parsed = parse(_rule_with("age > 18"))
    assert has_scope(parsed, "constant.numeric.prl", "18")

    parsed2 = parse(_rule_with("price > 100.0"))
    tokens = [t for t, _ in parsed2.find(tokens="constant.numeric.prl")]
    contents = [el.content for el in tokens]
    assert "100.0" in contents
    assert "100" not in contents
    assert "0" not in contents


def test_negative_numbers_include_the_minus_sign():
    parsed = parse(_rule_with("value == -1"))
    assert has_scope(parsed, "constant.numeric.prl", "-1")

    parsed2 = parse(_rule_with("value == -0.5"))
    assert has_scope(parsed2, "constant.numeric.prl", "-0.5")


def test_all_four_boolean_spellings():
    for spelling in ("true", "false", "True", "False"):
        parsed = parse(_rule_with(f"flag == {spelling}"))
        assert has_scope(parsed, "constant.language.boolean.prl", spelling)


def test_both_null_spellings():
    for spelling in ("null", "None"):
        parsed = parse(_rule_with(f"x == {spelling}"))
        assert has_scope(parsed, "constant.language.null.prl", spelling)


def test_escaped_quote_inside_string_does_not_terminate_early():
    parsed = parse(_rule_with(r'note == "she said \"hi\""'))
    assert has_scope(parsed, "string.quoted.double.prl", r'"she said \"hi\""')
