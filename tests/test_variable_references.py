from .helpers import has_scope, parse, scoped_tokens


def test_fact_binding_dollar_var():
    parsed = parse('rule "x"\nwhen\n  $s: Score(value > 90)\nthen\nend\n')
    assert has_scope(parsed, "variable.other.prl", "$s")


def test_accumulate_variables_both_occurrences():
    parsed = parse(
        'rule "x"\nwhen\n'
        "  accumulate(\n"
        "    Order($amount: amount);\n"
        "    $total: sum($amount);\n"
        "    $total > 1000\n"
        "  )\n"
        "then\nend\n"
    )
    variables = scoped_tokens(parsed, "variable.other.prl")
    assert variables.count("$amount") == 2
    assert variables.count("$total") == 2


def test_unprefixed_name_inside_then_block_is_not_a_variable_ref():
    parsed = parse('rule "x"\nwhen\n  $tx: Transaction()\nthen\n  fired.append(tx_id)\nend\n')
    assert "tx_id" not in scoped_tokens(parsed, "variable.other.prl")
