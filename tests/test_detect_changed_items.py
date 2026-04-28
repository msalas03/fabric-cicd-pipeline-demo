from pathlib import Path
from unittest.mock import patch
from scripts.detect_changed_items import detect_changed_items

def test_detect_changed_items_returns_list():
    repo_dir = Path(".")

    with patch("scripts.detect_changed_items.get_changed_items", return_value=["configs/slice_config.json"]):
        result = detect_changed_items(repo_dir)

    assert result == ["configs/slice_config.json"]

def test_detect_changed_items_returns_empty_list():
    repo_dir = Path(".")

    with patch("scripts.detect_changed_items.get_changed_items", return_value=[]):
        result = detect_changed_items(repo_dir)

    assert result == []