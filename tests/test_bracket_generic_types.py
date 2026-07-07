from .helpers import has_scope, parse, scoped_tokens


def test_single_param_generic():
    parsed = parse("declare Box\n  items: list[str]\nend\n")
    assert has_scope(parsed, "entity.name.type.prl", "list")
    assert has_scope(parsed, "entity.name.type.prl", "str")
    assert has_scope(parsed, "punctuation.section.generic.prl", "[")
    assert has_scope(parsed, "punctuation.section.generic.prl", "]")


def test_multi_param_generic():
    parsed = parse("declare Box\n  totals: dict[str, int]\nend\n")
    for name in ("dict", "str", "int"):
        assert has_scope(parsed, "entity.name.type.prl", name)
    assert has_scope(parsed, "punctuation.separator.generic.prl", ",")


def test_nested_generic():
    parsed = parse("declare Box\n  rows: list[dict[str, int]]\nend\n")
    for name in ("list", "dict", "str", "int"):
        assert has_scope(parsed, "entity.name.type.prl", name)
    brackets = scoped_tokens(parsed, "punctuation.section.generic.prl")
    assert brackets.count("[") == 2
    assert brackets.count("]") == 2


def test_plain_type_no_generic_unaffected():
    parsed = parse("declare Temperature\n  value: float\nend\n")
    assert has_scope(parsed, "entity.name.type.prl", "float")
    assert not scoped_tokens(parsed, "punctuation.section.generic.prl")
