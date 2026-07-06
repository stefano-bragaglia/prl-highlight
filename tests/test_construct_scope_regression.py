"""Regression tests: representative tokens per construct category carry the
expected scope, each pinned to a real vendored fixture (or, where no fixture
happens to exercise a construct, a small inline snippet - noted per test).
"""
from __future__ import annotations

from pathlib import Path

from .helpers import has_scope, parse

FIXTURES = Path(__file__).parent / "fixtures" / "prl_examples"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text()


# -- structural keywords -----------------------------------------------------


def test_declare_rule_when_then_end_in_blocks_world():
    parsed = parse(_fixture("blocks_world.prl"))
    for word in ("declare", "rule", "when", "then", "end"):
        assert has_scope(parsed, "keyword.control.prl", word)


def test_not_in_negation():
    parsed = parse(_fixture("negation.prl"))
    assert has_scope(parsed, "keyword.control.prl", "not")


def test_extends_in_inheritance():
    parsed = parse(_fixture("inheritance.prl"))
    assert has_scope(parsed, "keyword.control.prl", "extends")


def test_import_from_as_in_imported_types():
    parsed = parse(_fixture("imported_types.prl"))
    assert has_scope(parsed, "keyword.control.prl", "from")
    assert has_scope(parsed, "keyword.control.prl", "import")


def test_or_in_disjunction():
    parsed = parse(_fixture("disjunction.prl"))
    assert has_scope(parsed, "keyword.control.prl", "or")


def test_exists_in_existence_check():
    parsed = parse(_fixture("existence_check.prl"))
    assert has_scope(parsed, "keyword.control.prl", "exists")


def test_forall_in_universal():
    parsed = parse(_fixture("universal.prl"))
    assert has_scope(parsed, "keyword.control.prl", "forall")


def test_accumulate_in_aggregation():
    parsed = parse(_fixture("aggregation.prl"))
    assert has_scope(parsed, "keyword.control.prl", "accumulate")


def test_no_loop_attribute_in_self_modify():
    # self_modify.prl's rule-attribute "no-loop" is a plain PRL keyword;
    # its @no-loop *tag* form is covered separately below.
    parsed = parse('rule "x"\n  no-loop\nwhen\nthen\nend\n')
    assert has_scope(parsed, "keyword.control.prl", "no-loop")


def test_package_and_salience_inline():
    # No vendored fixture happens to use `package` or `salience`.
    parsed = parse('package com.example;\nrule "x"\n  salience 10\nwhen\nthen\nend\n')
    assert has_scope(parsed, "keyword.control.prl", "package")
    assert has_scope(parsed, "keyword.control.prl", "salience")


# -- tag annotations ----------------------------------------------------------


def test_key_tag_in_identity_key():
    parsed = parse(_fixture("identity_key.prl"))
    assert has_scope(parsed, "entity.name.tag.prl", "key")


def test_no_loop_tag_in_self_modify():
    parsed = parse(_fixture("self_modify.prl"))
    assert has_scope(parsed, "entity.name.tag.prl", "no-loop")


def test_role_expires_timestamp_tags_in_event_stream():
    parsed = parse(_fixture("event_stream.prl"))
    assert has_scope(parsed, "entity.name.tag.prl", "role")
    assert has_scope(parsed, "meta.tag-value.prl", "event")
    assert has_scope(parsed, "entity.name.tag.prl", "expires")
    assert has_scope(parsed, "meta.tag-value.prl", "30s")
    assert has_scope(parsed, "entity.name.tag.prl", "timestamp")


# -- fact type and field names ------------------------------------------------


def test_type_and_field_names_in_temperature_alarm():
    parsed = parse(_fixture("temperature_alarm.prl"))
    assert has_scope(parsed, "entity.name.type.prl", "Temperature")
    assert has_scope(parsed, "variable.other.property.prl", "sensor")


# -- pattern syntax: traditional vs OOPath -----------------------------------


def test_traditional_pattern_in_negation():
    parsed = parse(_fixture("negation.prl"))
    assert has_scope(parsed, "entity.name.type.prl", "On")
    assert has_scope(parsed, "punctuation.section.pattern.prl", "(")
    assert has_scope(parsed, "punctuation.section.pattern.prl", ")")


def test_oopath_pattern_in_temperature_alarm_same_scope_as_traditional():
    # temperature_alarm.prl is the one vendored fixture using OOPath syntax.
    parsed = parse(_fixture("temperature_alarm.prl"))
    assert has_scope(parsed, "entity.name.type.prl", "Temperature")
    assert has_scope(parsed, "punctuation.section.pattern.prl", "/")
    assert has_scope(parsed, "punctuation.section.pattern.prl", "[")
    assert has_scope(parsed, "punctuation.section.pattern.prl", "]")


# -- constraint forms ---------------------------------------------------------


def test_bind_constraint_in_family_tree():
    parsed = parse(_fixture("family_tree.prl"))
    assert has_scope(parsed, "variable.other.prl", "$p")
    assert has_scope(parsed, "punctuation.separator.binding.prl", ":")


def test_comparison_constraint_in_loan_application():
    parsed = parse(_fixture("loan_application.prl"))
    assert has_scope(parsed, "variable.other.property.prl", "age")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "<")


def test_positional_constraint_in_compact_patterns():
    parsed = parse(_fixture("compact_patterns.prl"))
    tokens = [el.content for el, _ in parsed.find(tokens="constant.numeric.prl")]
    assert "0" in tokens


def test_named_constraint_in_compact_patterns():
    parsed = parse(_fixture("compact_patterns.prl"))
    assert has_scope(parsed, "variable.other.property.prl", "y")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "=")


# -- $variable references -----------------------------------------------------


def test_variable_references_in_blocks_world():
    parsed = parse(_fixture("blocks_world.prl"))
    for var in ("$x", "$y", "$z"):
        assert has_scope(parsed, "variable.other.prl", var)


# -- literals ------------------------------------------------------------------


def test_string_literal_in_blocks_world():
    parsed = parse(_fixture("blocks_world.prl"))
    assert has_scope(parsed, "string.quoted.double.prl", '"red"')


def test_integer_literal_in_loan_application():
    parsed = parse(_fixture("loan_application.prl"))
    assert has_scope(parsed, "constant.numeric.prl", "21")


def test_float_literal_in_event_stream():
    parsed = parse(_fixture("event_stream.prl"))
    assert has_scope(parsed, "constant.numeric.prl", "100.0")


def test_boolean_true_lowercase_in_existence_check():
    parsed = parse(_fixture("existence_check.prl"))
    assert has_scope(parsed, "constant.language.boolean.prl", "true")


def test_boolean_true_pythoncase_in_loan_application():
    parsed = parse(_fixture("loan_application.prl"))
    assert has_scope(parsed, "constant.language.boolean.prl", "True")


def test_boolean_and_null_inline():
    # No fixture happens to use false/False/null/None as a PRL constraint
    # literal (loan_application.prl's False only appears inside Python RHS).
    parsed = parse(
        'rule "x"\nwhen\n'
        "  Foo(a == false, b == False, c == null, d == None)\n"
        "then\nend\n"
    )
    assert has_scope(parsed, "constant.language.boolean.prl", "false")
    assert has_scope(parsed, "constant.language.boolean.prl", "False")
    assert has_scope(parsed, "constant.language.null.prl", "null")
    assert has_scope(parsed, "constant.language.null.prl", "None")


# -- operators and comments ---------------------------------------------------


def test_gte_operator_in_temperature_alarm():
    parsed = parse(_fixture("temperature_alarm.prl"))
    assert has_scope(parsed, "keyword.operator.comparison.prl", ">=")


def test_remaining_operators_inline():
    # != and <= don't appear in any of the 17 vendored fixtures.
    parsed = parse('rule "x"\nwhen\n  Foo(a != 1, b <= 2)\nthen\nend\n')
    assert has_scope(parsed, "keyword.operator.comparison.prl", "!=")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "<=")


def test_line_comment_in_blocks_world():
    parsed = parse(_fixture("blocks_world.prl"))
    tokens = [el.content for el, _ in parsed.find(tokens="comment.line.double-slash.prl")]
    assert any(t.startswith("//") for t in tokens)


def test_block_comment_inline():
    # No vendored fixture uses a /* */ block comment.
    parsed = parse('/* a block comment */\nrule "x"\nwhen\nthen\nend\n')
    assert has_scope(parsed, "comment.block.prl", "/* a block comment */")


# -- embedded Python RHS -------------------------------------------------------


def test_embedded_python_rhs_in_self_modify():
    parsed = parse(_fixture("self_modify.prl"))
    # Anything from the stub/real source.python grammar proves the RHS body
    # is being handed off to Python highlighting rather than PRL's own scopes.
    python_scoped = [
        el.content
        for el, stack in parsed.find(tokens="meta.embedded.block.python.prl")
    ]
    assert python_scoped


def test_end_inside_python_string_does_not_close_block_early():
    parsed = parse(
        'rule "x"\nwhen\nthen\n'
        '  logger.info("end of rule")\n'
        "end\n"
    )
    ends = [el.content for el, _ in parsed.find(tokens="keyword.control.prl") if el.content == "end"]
    # Exactly one real closing `end` recognized - not the one inside the string.
    assert len(ends) == 1
