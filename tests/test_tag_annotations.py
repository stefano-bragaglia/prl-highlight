from .helpers import has_scope, parse, scoped_tokens


def test_no_loop_tag_before_rule_no_value():
    parsed = parse('@no-loop\nrule "cap score"\nwhen\nthen\nend\n')
    assert has_scope(parsed, "entity.name.tag.prl", "no-loop")
    assert scoped_tokens(parsed, "meta.tag-value.prl") == []


def test_role_tag_with_value_before_declare():
    parsed = parse("@role(event)\ndeclare StockTick\n  ts: float\nend\n")
    assert has_scope(parsed, "entity.name.tag.prl", "role")
    assert has_scope(parsed, "meta.tag-value.prl", "event")


def test_expires_tag_value_is_not_a_numeric_literal():
    parsed = parse("@expires(30s)\ndeclare StockTick\n  ts: float\nend\n")
    assert has_scope(parsed, "meta.tag-value.prl", "30s")
    assert "30s" not in scoped_tokens(parsed, "constant.numeric.prl")


def test_field_level_key_tag():
    parsed = parse(
        "declare Customer\n  @key\n  id: str\n  name: str\nend\n"
    )
    assert has_scope(parsed, "entity.name.tag.prl", "key")


def test_timestamp_tag_no_value():
    parsed = parse("declare StockTick\n  @timestamp\n  ts: float\nend\n")
    assert has_scope(parsed, "entity.name.tag.prl", "timestamp")
    assert scoped_tokens(parsed, "meta.tag-value.prl") == []
