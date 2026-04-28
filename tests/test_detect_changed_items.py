from pathlib import Path
from unittest.mock import patch
from scripts.detect_changed_items import (
    detect_fabric_changed_items,
    detect_git_changed_files,
    is_deploy_relevant,
    classify_changed_items,
)

def test_detect_fabric_changed_items_returns_list():
    repo_dir = Path(".")

    with patch(
        "scripts.detect_changed_items.get_changed_items",
        return_value=["configs/slice_config.json"],
    ):
        result = detect_fabric_changed_items(repo_dir)

    assert result == ["configs/slice_config.json"]

def test_detect_git_changed_files_returns_list():
    repo_dir = Path(".")

    mock_stdout = "configs/slice_config.json\nscripts/create_slice.py\n"

    with patch("scripts.detect_changed_items.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = mock_stdout
        mock_run.return_value.stderr = ""

        result = detect_git_changed_files(repo_dir)

    assert result == [
        "configs/slice_config.json",
        "scripts/create_slice.py",
    ]

def test_is_deploy_relevant_for_configs():
    assert is_deploy_relevant("configs/slice_config.json") is True

def test_is_deploy_relevant_for_scripts():
    assert is_deploy_relevant("scripts/create_slice.py") is True

def test_is_not_deploy_relevant_for_notes():
    assert is_deploy_relevant("notes/module1.md") is False

def test_classify_changed_items():
    changed_items = [
        "configs/slice_config.json",
        "scripts/create_slice.py",
        "README.md",
        "notes/module1.md",
    ]

    result = classify_changed_items(changed_items)

    assert result["deploy_relevant"] == [
        "configs/slice_config.json",
        "scripts/create_slice.py",
    ]
    assert result["non_deploy"] == [
        "README.md",
        "notes/module1.md",
    ]