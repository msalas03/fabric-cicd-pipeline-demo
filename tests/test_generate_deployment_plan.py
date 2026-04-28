from scripts.generate_deployment_plan import build_deployment_plan

def test_build_deployment_plan_with_deploy_relevant_files():
    plan = build_deployment_plan(
        environment="dev",
        fabric_changed_items=[],
        git_changed_files=["scripts/create_slice.py"],
        deploy_relevant_files=["scripts/create_slice.py"],
        non_deploy_files=[],
    )

    assert plan["environment"] == "dev"
    assert plan["deploy_relevant"] is True
    assert plan["git_changed_files"] == ["scripts/create_slice.py"]
    assert plan["deploy_relevant_files"] == ["scripts/create_slice.py"]
    assert plan["non_deploy_files"] == []
    assert "generated_at_utc" in plan

def test_build_deployment_plan_without_deploy_relevant_files():
    plan = build_deployment_plan(
        environment="dev",
        fabric_changed_items=[],
        git_changed_files=["README.md"],
        deploy_relevant_files=[],
        non_deploy_files=["README.md"],
    )

    assert plan["environment"] == "dev"
    assert plan["deploy_relevant"] is False
    assert plan["git_changed_files"] == ["README.md"]
    assert plan["deploy_relevant_files"] == []
    assert plan["non_deploy_files"] == ["README.md"]
    assert "generated_at_utc" in plan