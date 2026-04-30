from scripts.evaluate_deployment_policy import evaluate_policy


def test_dev_allows_deployment_even_without_main_or_relevant_changes():
    policy = {
        "dev": {
            "require_main_branch": False,
            "require_deploy_relevant_changes": False,
            "require_approval": False,
        }
    }

    result = evaluate_policy(
        environment="dev",
        branch="feature/test",
        deploy_relevant=False,
        policy=policy,
    )

    assert result["deployment_allowed"] is True
    assert result["failed_checks"] == []
    assert result["decision_reason"] == "Deployment policy checks passed."


def test_qa_requires_approval_when_policy_checks_pass():
    policy = {
        "qa": {
            "require_main_branch": True,
            "require_deploy_relevant_changes": True,
            "require_approval": True,
        }
    }

    result = evaluate_policy(
        environment="qa",
        branch="main",
        deploy_relevant=True,
        policy=policy,
    )

    assert result["deployment_allowed"] is True
    assert result["failed_checks"] == []
    assert result["decision_reason"] == "Deployment requires approval."


def test_prod_blocks_non_main_branch():
    policy = {
        "prod": {
            "require_main_branch": True,
            "require_deploy_relevant_changes": True,
            "require_approval": True,
        }
    }

    result = evaluate_policy(
        environment="prod",
        branch="feature/test",
        deploy_relevant=True,
        policy=policy,
    )

    assert result["deployment_allowed"] is False
    assert "main_branch_required" in result["failed_checks"]


def test_prod_blocks_when_no_deploy_relevant_changes():
    policy = {
        "prod": {
            "require_main_branch": True,
            "require_deploy_relevant_changes": True,
            "require_approval": True,
        }
    }

    result = evaluate_policy(
        environment="prod",
        branch="main",
        deploy_relevant=False,
        policy=policy,
    )

    assert result["deployment_allowed"] is False
    assert "deploy_relevant_changes_required" in result["failed_checks"]


def test_prod_requires_approval_when_main_and_deploy_relevant():
    policy = {
        "prod": {
            "require_main_branch": True,
            "require_deploy_relevant_changes": True,
            "require_approval": True,
        }
    }

    result = evaluate_policy(
        environment="prod",
        branch="main",
        deploy_relevant=True,
        policy=policy,
    )

    assert result["deployment_allowed"] is True
    assert result["failed_checks"] == []
    assert result["decision_reason"] == "Deployment requires approval."


def test_unknown_environment_is_blocked():
    policy = {}

    result = evaluate_policy(
        environment="qa",
        branch="main",
        deploy_relevant=True,
        policy=policy,
    )

    assert result["deployment_allowed"] is False
    assert result["failed_checks"] == ["unknown_environment"]