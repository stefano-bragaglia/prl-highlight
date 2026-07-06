#!/usr/bin/env python3
"""Print the absolute path to this repo's TextMate bundle folder.

Paste the printed path into PyCharm's Preferences -> Editor -> TextMate
Bundles -> + folder picker. Prints nothing but the path on success so the
output is directly copy-pasteable or pipeable.
"""
from __future__ import annotations

import sys
from pathlib import Path

BUNDLE_PATH = Path(__file__).resolve().parent.parent / "bundle" / "PRL.tmbundle"


def resolve_bundle_path(bundle_path: Path) -> Path:
    """Return *bundle_path* if it exists, else raise FileNotFoundError."""
    if not bundle_path.is_dir():
        raise FileNotFoundError(f"bundle folder not found: {bundle_path}")
    return bundle_path


def main() -> int:
    try:
        path = resolve_bundle_path(BUNDLE_PATH)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
