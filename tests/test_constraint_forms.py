from .helpers import has_scope, parse, scoped_tokens


def _rule_with(condition: str) -> str:
    return f'rule "x"\nwhen\n  Foo({condition})\nthen\nend\n'


def test_bind_constraint():
    parsed = parse(_rule_with("$tx_id: id"))
    assert has_scope(parsed, "variable.other.prl", "$tx_id")
    assert has_scope(parsed, "punctuation.separator.binding.prl", ":")
    assert has_scope(parsed, "variable.other.property.prl", "id")


def test_comparison_constraint():
    parsed = parse(_rule_with('status == "pending"'))
    assert has_scope(parsed, "variable.other.property.prl", "status")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "==")
    assert has_scope(parsed, "string.quoted.double.prl", '"pending"')


def test_join_test_rhs_is_a_variable_not_a_literal():
    parsed = parse(_rule_with("account_id == $account_id"))
    assert has_scope(parsed, "variable.other.prl", "$account_id")
    assert "$account_id" not in scoped_tokens(parsed, "string.quoted.double.prl")
    assert "$account_id" not in scoped_tokens(parsed, "constant.numeric.prl")


def test_positional_constraints_have_no_property_scope():
    parsed = parse(_rule_with("0, 0"))
    numerics = scoped_tokens(parsed, "constant.numeric.prl")
    assert numerics.count("0") == 2
    assert scoped_tokens(parsed, "variable.other.property.prl") == []


def test_named_constraint():
    parsed = parse(_rule_with("y=0"))
    assert has_scope(parsed, "variable.other.property.prl", "y")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "=")
    assert has_scope(parsed, "constant.numeric.prl", "0")


def test_dotted_field_path():
    parsed = parse(_rule_with('address.city == "NYC"'))
    assert has_scope(parsed, "variable.other.property.prl", "address")
    assert has_scope(parsed, "variable.other.property.prl", "city")
    assert has_scope(parsed, "punctuation.accessor.prl", ".")
