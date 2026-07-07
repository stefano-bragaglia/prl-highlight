from .helpers import has_scope, parse, scoped_tokens


def test_null_default():
    parsed = parse("declare Dataset\n  stage: str = null\nend\n")
    assert has_scope(parsed, "keyword.operator.comparison.prl", "=")
    assert has_scope(parsed, "constant.language.null.prl", "null")


def test_negative_int_default():
    parsed = parse("declare Score\n  value: int = -1\nend\n")
    assert has_scope(parsed, "constant.numeric.prl", "-1")


def test_string_default():
    parsed = parse('declare Customer\n  customerId: str = "unknown"\nend\n')
    assert has_scope(parsed, "string.quoted.double.prl", '"unknown"')


def test_bool_default():
    parsed = parse("declare Flag\n  active: bool = true\nend\n")
    assert has_scope(parsed, "constant.language.boolean.prl", "true")


def test_generic_type_and_container_default_disambiguated_on_one_line():
    parsed = parse(
        "declare Dataset\n  remediation_history: list[str] = []\nend\n"
    )
    assert has_scope(parsed, "punctuation.section.generic.prl", "[")
    assert has_scope(parsed, "punctuation.section.container.prl", "[")
    assert has_scope(parsed, "punctuation.section.container.prl", "]")


def test_nonempty_list_default():
    parsed = parse("declare Score\n  values: list[int] = [1, 2, 3]\nend\n")
    numbers = scoped_tokens(parsed, "constant.numeric.prl")
    assert {"1", "2", "3"}.issubset(set(numbers))
    assert has_scope(parsed, "punctuation.separator.container.prl", ",")


def test_nonempty_dict_default():
    parsed = parse(
        'declare Dataset\n  metrics: dict[str, int] = {"a": 1}\nend\n'
    )
    assert has_scope(parsed, "string.quoted.double.prl", '"a"')
    assert has_scope(parsed, "constant.numeric.prl", "1")
    assert has_scope(parsed, "punctuation.separator.container.prl", ":")


def test_no_default_unaffected():
    parsed = parse("declare Temperature\n  value: float\nend\n")
    assert not scoped_tokens(parsed, "punctuation.section.container.prl")
    # The comparison-operator scope must not appear spuriously for a plain
    # field with no default clause at all.
    assert not scoped_tokens(parsed, "keyword.operator.comparison.prl")
