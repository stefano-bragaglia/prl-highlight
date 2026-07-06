"""XML-shape tests for the PRL Live Templates bundle (bundle/live-templates/prl.xml)."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

TEMPLATE_XML = Path(__file__).parent.parent / "bundle" / "live-templates" / "prl.xml"


def _root() -> ET.Element:
    return ET.parse(TEMPLATE_XML).getroot()


def _template(name: str) -> ET.Element:
    root = _root()
    matches = [t for t in root.findall("template") if t.attrib.get("name") == name]
    assert len(matches) == 1, f"expected exactly one <template name={name!r}>, found {len(matches)}"
    return matches[0]


def _fill_placeholders(value: str) -> str:
    """Replace every $VAR$ with a short sample token; $END$ is a zero-width
    cursor marker (not literal text), so it's dropped rather than lowercased.
    """
    without_end = value.replace("$END$", "")
    return re.sub(r"\$([A-Z_]+)\$", lambda m: m.group(1).lower(), without_end)


def test_file_is_well_formed_xml():
    _root()  # raises ET.ParseError if malformed


def test_root_is_single_template_set_with_prl_group():
    root = _root()
    assert root.tag == "templateSet"
    assert root.attrib.get("group") == "PRL"


def test_structural_block_templates_exist():
    for name in ("prl-rule", "prl-declare", "prl-declare-extends"):
        _template(name)


def test_structural_block_templates_have_other_context():
    for name in ("prl-rule", "prl-declare", "prl-declare-extends"):
        template = _template(name)
        context = template.find("context")
        assert context is not None
        options = {o.attrib["name"]: o.attrib["value"] for o in context.findall("option")}
        assert options.get("OTHER") == "true"


def test_prl_rule_expansion_is_structurally_valid_prl():
    value = _template("prl-rule").attrib["value"]
    filled = _fill_placeholders(value)
    assert filled.startswith('rule "name"')
    assert "\nwhen\n" in filled
    assert "\nthen\n" in filled
    assert filled.rstrip("\n").endswith("end")


def test_prl_declare_expansion_is_structurally_valid_prl():
    value = _template("prl-declare").attrib["value"]
    filled = _fill_placeholders(value)
    assert filled.startswith("declare type")
    assert "field: field_type" in filled
    assert filled.rstrip("\n").endswith("end")


def test_prl_declare_extends_expansion_is_structurally_valid_prl():
    value = _template("prl-declare-extends").attrib["value"]
    filled = _fill_placeholders(value)
    assert filled.startswith("declare type extends parent")
    assert "field: field_type" in filled
    assert filled.rstrip("\n").endswith("end")


def test_condition_construct_templates_exist():
    for name in ("prl-not", "prl-accumulate", "prl-forall", "prl-or", "prl-exists"):
        _template(name)


def test_condition_construct_templates_have_other_context():
    for name in ("prl-not", "prl-accumulate", "prl-forall", "prl-or", "prl-exists"):
        template = _template(name)
        context = template.find("context")
        assert context is not None
        options = {o.attrib["name"]: o.attrib["value"] for o in context.findall("option")}
        assert options.get("OTHER") == "true"


def test_prl_not_expansion_is_structurally_valid_prl():
    filled = _fill_placeholders(_template("prl-not").attrib["value"])
    assert filled == "not ( pattern )"


def test_prl_accumulate_expansion_is_structurally_valid_prl():
    value = _template("prl-accumulate").attrib["value"]
    filled = _fill_placeholders(value)
    assert filled.startswith("accumulate(\n")
    assert "inner;" in filled
    assert re.search(r"result: \w+\(bind\);", filled)
    assert filled.rstrip("\n").endswith(")")


def test_prl_accumulate_function_variable_is_enum_of_supported_functions():
    template = _template("prl-accumulate")
    function_var = next(v for v in template.findall("variable") if v.attrib["name"] == "FUNCTION")
    expression = function_var.attrib["expression"]
    for fn in ("sum", "count", "min", "max", "collectList"):
        assert fn in expression


def test_prl_forall_expansion_is_structurally_valid_prl():
    value = _template("prl-forall").attrib["value"]
    filled = _fill_placeholders(value)
    assert filled.startswith("forall(\n")
    assert "pattern," in filled
    assert "condition" in filled
    assert filled.rstrip("\n").endswith(")")


def test_prl_or_expansion_is_structurally_valid_prl():
    filled = _fill_placeholders(_template("prl-or").attrib["value"])
    assert filled == "left or\nright"


def test_prl_exists_expansion_is_structurally_valid_prl():
    filled = _fill_placeholders(_template("prl-exists").attrib["value"])
    assert filled == "exists pattern"
