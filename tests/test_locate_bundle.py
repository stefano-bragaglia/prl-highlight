"""Stage A tests for install-docs-tooling's locate-bundle-script story."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from scripts import locate_bundle

REPO_ROOT = Path(__file__).parent.parent


def test_resolve_bundle_path_returns_existing_folder():
    path = locate_bundle.resolve_bundle_path(locate_bundle.BUNDLE_PATH)
    assert path.is_dir()
    assert path.name == "PRL.tmbundle"


def test_resolve_bundle_path_raises_for_missing_folder(tmp_path):
    missing = tmp_path / "does-not-exist"
    with pytest.raises(FileNotFoundError, match=r"does-not-exist"):
        locate_bundle.resolve_bundle_path(missing)


def test_main_prints_only_the_path_and_returns_zero(capsys):
    exit_code = locate_bundle.main()
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == f"{locate_bundle.BUNDLE_PATH}\n"
    assert captured.err == ""


def test_main_reports_error_on_stderr_and_returns_nonzero(monkeypatch, tmp_path, capsys):
    missing = tmp_path / "does-not-exist"
    monkeypatch.setattr(locate_bundle, "BUNDLE_PATH", missing)
    exit_code = locate_bundle.main()
    captured = capsys.readouterr()
    assert exit_code != 0
    assert captured.out == ""
    assert "does-not-exist" in captured.err


def test_script_runs_end_to_end_from_repo_root():
    result = subprocess.run(
        [sys.executable, "scripts/locate_bundle.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    expected = REPO_ROOT / "bundle" / "PRL.tmbundle"
    assert result.returncode == 0
    assert result.stdout == f"{expected}\n"
    assert result.stderr == ""


def test_script_runs_identically_from_a_different_working_directory(tmp_path):
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "locate_bundle.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    expected = REPO_ROOT / "bundle" / "PRL.tmbundle"
    assert result.returncode == 0
    assert result.stdout == f"{expected}\n"
    assert result.stderr == ""
