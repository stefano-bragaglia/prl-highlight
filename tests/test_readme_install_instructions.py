"""Stage A test for install-docs-tooling's readme-install-instructions story.

A docs-content regression test only - it doesn't validate PyCharm itself,
just that the instructions haven't silently regressed or been deleted.
ponytail: substring-presence check, not a PyCharm integration test - upgrade
only if the instructions are found to drift in practice.
"""
from __future__ import annotations

from pathlib import Path

README = (Path(__file__).parent.parent / "README.md").read_text()


def _installation_section() -> str:
    start = README.index("## Installation")
    end = README.index("\n## ", start + 1)
    return README[start:end]


def test_installation_section_mentions_textmate_bundles_menu_path():
    assert "TextMate Bundles" in _installation_section()


def test_installation_section_mentions_live_templates_menu_path():
    assert "Live Templates" in _installation_section()


def test_installation_section_mentions_locate_bundle_script():
    assert "locate_bundle.py" in _installation_section()


def test_installation_section_names_the_real_bundle_and_templates_files():
    section = _installation_section()
    assert "PRL.tmbundle" in section
    assert "bundle/live-templates/prl.xml" in section


def test_installation_section_does_not_imply_one_click_install():
    # Explicitly *denying* a one-click install ("there is no one-click
    # installer") is exactly the desired phrasing - only ban phrases that
    # would wrongly claim automation exists.
    section = _installation_section().lower()
    for phrase in ("just run this script and you're done", "automatically installs"):
        assert phrase not in section
