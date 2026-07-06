"""Stage A tests for bundle-packaging's bundle-folder-scaffold story."""
from __future__ import annotations

import json
import plistlib
from pathlib import Path

BUNDLE_ROOT = Path(__file__).parent.parent / "bundle" / "PRL.tmbundle"
CANONICAL_GRAMMAR = (
    Path(__file__).parent.parent / "src" / "prl_highlight" / "grammar" / "prl.tmLanguage.json"
)


def test_info_plist_is_valid_plist_with_name_and_uuid():
    info_path = BUNDLE_ROOT / "info.plist"
    assert info_path.exists()
    with info_path.open("rb") as f:
        info = plistlib.load(f)
    assert info["name"] == "PRL"
    assert "uuid" in info and info["uuid"]


def test_syntaxes_grammar_is_valid_json_with_prl_scope():
    grammar_path = BUNDLE_ROOT / "Syntaxes" / "PRL.tmLanguage.json"
    assert grammar_path.exists()
    grammar = json.loads(grammar_path.read_text())
    assert grammar["scopeName"] == "source.prl"
    assert "prl" in grammar["fileTypes"]


def test_bundled_grammar_matches_canonical_grammar_content():
    grammar_path = BUNDLE_ROOT / "Syntaxes" / "PRL.tmLanguage.json"
    assert grammar_path.read_text() == CANONICAL_GRAMMAR.read_text()


def test_expected_bundle_file_set_is_present():
    expected = {
        BUNDLE_ROOT / "info.plist",
        BUNDLE_ROOT / "Syntaxes" / "PRL.tmLanguage.json",
    }
    for path in expected:
        assert path.exists(), f"missing required bundle file: {path}"
