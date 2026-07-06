"""Stage A tests for bundle-packaging's comment-and-bracket-preferences story."""
from __future__ import annotations

import plistlib
from pathlib import Path

PREFERENCES = Path(__file__).parent.parent / "bundle" / "PRL.tmbundle" / "Preferences"


def _shell_variables(plist: dict) -> dict[str, str]:
    return {v["name"]: v["value"] for v in plist["settings"]["shellVariables"]}


def test_comments_preferences_declares_line_and_block_comment_tokens():
    path = PREFERENCES / "Comments.tmPreferences"
    assert path.exists()
    with path.open("rb") as f:
        plist = plistlib.load(f)
    assert plist["scope"] == "source.prl"
    variables = _shell_variables(plist)
    assert variables["TM_COMMENT_START"] == "// "
    assert variables["TM_COMMENT_START_2"] == "/* "
    assert variables["TM_COMMENT_END_2"] == " */"


def test_typing_pairs_preferences_declares_bracket_and_quote_pairs():
    path = PREFERENCES / "Typing Pairs.tmPreferences"
    assert path.exists()
    with path.open("rb") as f:
        plist = plistlib.load(f)
    assert plist["scope"] == "source.prl"
    pairs = {tuple(pair) for pair in plist["settings"]["smartTypingPairs"]}
    assert pairs == {
        ("(", ")"),
        ("[", "]"),
        ("{", "}"),
        ('"', '"'),
        ("'", "'"),
    }
