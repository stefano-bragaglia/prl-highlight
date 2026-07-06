"""XML-shape tests for the PRL Live Templates bundle (bundle/live-templates/prl.xml)."""

import xml.etree.ElementTree as ET
from pathlib import Path

TEMPLATE_XML = Path(__file__).parent.parent / "bundle" / "live-templates" / "prl.xml"


def _root() -> ET.Element:
    return ET.parse(TEMPLATE_XML).getroot()


def test_file_is_well_formed_xml():
    _root()  # raises ET.ParseError if malformed


def test_root_is_single_template_set_with_prl_group():
    root = _root()
    assert root.tag == "templateSet"
    assert root.attrib.get("group") == "PRL"
