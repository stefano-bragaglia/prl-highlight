from .helpers import has_scope, parse


def test_declare_type_name_and_field():
    parsed = parse("declare Temperature\n  value: float\nend\n")
    assert has_scope(parsed, "entity.name.type.prl", "Temperature")
    assert has_scope(parsed, "variable.other.property.prl", "value")
    assert has_scope(parsed, "entity.name.type.prl", "float")


def test_declare_extends_both_types():
    parsed = parse("declare Dog extends Animal\n  breed: str\nend\n")
    assert has_scope(parsed, "entity.name.type.prl", "Dog")
    assert has_scope(parsed, "entity.name.type.prl", "Animal")


def test_pattern_head_type_name():
    parsed = parse('rule "x"\nwhen\n  Temperature($t: value)\nthen\nend\n')
    assert has_scope(parsed, "entity.name.type.prl", "Temperature")


def test_import_names_are_types():
    parsed = parse(
        "from examples.declarative.domain import Vehicle, Fleet\n"
    )
    assert has_scope(parsed, "entity.name.type.prl", "Vehicle")
    assert has_scope(parsed, "entity.name.type.prl", "Fleet")
