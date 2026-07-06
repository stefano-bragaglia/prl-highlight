from .helpers import has_scope, parse


def test_rule_when_then_end_are_keywords():
    parsed = parse('rule "x"\nwhen\n  Foo()\nthen\n  pass\nend\n')
    for word in ("rule", "when", "then", "end"):
        assert has_scope(parsed, "keyword.control.prl", word)


def test_declare_extends_end_are_keywords():
    parsed = parse("declare Foo extends Bar\n  x: str\nend\n")
    assert has_scope(parsed, "keyword.control.prl", "declare")
    assert has_scope(parsed, "keyword.control.prl", "extends")
    assert has_scope(parsed, "keyword.control.prl", "end")


def test_end_inside_longer_identifier_is_not_a_keyword():
    parsed = parse("declare Foo\n  endDate: int\nend\n")
    tokens = [t for t, _ in parsed.find(tokens="keyword.control.prl")]
    contents = [el.content for el in tokens]
    assert "endDate" not in contents


def test_no_loop_is_a_single_keyword_token():
    parsed = parse('rule "x"\n  no-loop\nwhen\nthen\nend\n')
    assert has_scope(parsed, "keyword.control.prl", "no-loop")


def test_no_loop_with_boolean_value():
    parsed = parse('rule "x"\n  no-loop true\nwhen\nthen\nend\n')
    assert has_scope(parsed, "keyword.control.prl", "no-loop")


def test_package_keyword():
    parsed = parse("package com.example;\n")
    assert has_scope(parsed, "keyword.control.prl", "package")


def test_import_and_as_keywords():
    parsed = parse("import Foo.Bar as Baz\n")
    assert has_scope(parsed, "keyword.control.prl", "import")
    assert has_scope(parsed, "keyword.control.prl", "as")


def test_or_exists_forall_accumulate_keywords():
    parsed = parse(
        'rule "x"\nwhen\n'
        "  Person($name: name, age > 18) or\n"
        "  exists Invoice(overdue == true)\n"
        "  forall(\n"
        "    Order(status == \"pending\"),\n"
        "    Approval(order_id == $id)\n"
        "  )\n"
        "  accumulate(\n"
        "    Order($amount: amount);\n"
        "    $total: sum($amount);\n"
        "    $total > 1000\n"
        "  )\n"
        "then\nend\n"
    )
    for word in ("or", "exists", "forall", "accumulate"):
        assert has_scope(parsed, "keyword.control.prl", word)
