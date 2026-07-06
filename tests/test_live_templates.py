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
    """Replace every $VAR$ (including $END$) with a short sample token."""
    return re.sub(r"\$([A-Z_]+)\$", lambda m: m.group(1).lower(), value)


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
