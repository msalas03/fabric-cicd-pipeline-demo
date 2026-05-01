import json
from unittest.mock import patch

from scripts.evaluate_promoted_artifact import load_plan


def test_load_plan_reads_json(tmp_path):
    plan_file = tmp_path / "deployment_plan.json"
    plan_file.write_text(json.dumps({"deployment_allowed": True}), encoding="utf-8")

    result = load_plan(plan_file)

    assert result["deployment_allowed"] is True


def test_prefers_promoted_plan_when_present(tmp_path, monkeypatch):
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()

    base_plan = artifacts_dir / "deployment_plan.json"
    promoted_plan = artifacts_dir / "promoted_deployment_plan.json"

    base_plan.write_text(json.dumps({"deployment_allowed": False}), encoding="utf-8")
    promoted_plan.write_text(json.dumps({"deployment_allowed": True}), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    from scripts.evaluate_promoted_artifact import main

    with patch("builtins.print") as mock_print:
        main()

    # ensure promoted plan was used
    printed = " ".join(str(call.args) for call in mock_print.call_args_list)
    assert "promoted_deployment_plan.json" in printed
    assert "deployment_allowed=true" in printed.lower()


def test_falls_back_to_base_plan_when_no_promoted(tmp_path, monkeypatch):
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()

    base_plan = artifacts_dir / "deployment_plan.json"
    base_plan.write_text(json.dumps({"deployment_allowed": False}), encoding="utf-8")

    monkeypatch.chdir(tmp_path)

    from scripts.evaluate_promoted_artifact import main

    with patch("builtins.print") as mock_print:
        main()

    printed = " ".join(str(call.args) for call in mock_print.call_args_list)
    assert "deployment_plan.json" in printed
    assert "deployment_allowed=false" in printed.lower()