from scripts.promote_deployment_plan import promote_plan


def test_promote_plan_sets_target_environment(monkeypatch):
    monkeypatch.setenv("GITHUB_ACTOR", "msalas03")
    monkeypatch.setenv("GITHUB_REF_NAME", "main")

    plan = {
        "source_environment": "dev",
        "promotion_target": None,
        "deployment_allowed": True,
    }

    result = promote_plan(plan, "qa")

    assert result["source_environment"] == "dev"
    assert result["promotion_target"] == "qa"
    assert result["promoted_by"] == "msalas03"
    assert result["promotion_ref"] == "main"
    assert result["deployment_allowed"] is True