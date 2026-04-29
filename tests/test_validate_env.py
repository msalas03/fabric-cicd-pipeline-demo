from scripts.validate_fabric_env import get_environment, validate_environment


def test_get_environment_defaults_to_dev():
    env = {}

    result = get_environment(env)

    assert result == "dev"


def test_get_environment_reads_prod():
    env = {"FABRIC_ENV": "prod"}

    result = get_environment(env)

    assert result == "prod"


def test_dev_environment_passes_without_strict_validation():
    env = {"FABRIC_ENV": "dev"}

    is_valid, errors = validate_environment(env)

    assert is_valid is True
    assert errors == []


def test_prod_environment_fails_when_required_vars_and_auth_are_missing():
    env = {"FABRIC_ENV": "prod"}

    is_valid, errors = validate_environment(env)

    assert is_valid is False
    assert "missing_required" in errors
    assert "missing_auth" in errors


def test_prod_environment_fails_when_auth_is_missing():
    env = {
        "FABRIC_ENV": "prod",
        "FABRIC_ORCHESTRATOR_HOST": "orchestrator.example",
        "FABRIC_CREDMGR_HOST": "credmgr.example",
    }

    is_valid, errors = validate_environment(env)

    assert is_valid is False
    assert "missing_auth" in errors


def test_prod_environment_passes_with_required_vars_and_token():
    env = {
        "FABRIC_ENV": "prod",
        "FABRIC_ORCHESTRATOR_HOST": "orchestrator.example",
        "FABRIC_CREDMGR_HOST": "credmgr.example",
        "FABRIC_ID_TOKEN": "token123",
    }

    is_valid, errors = validate_environment(env)

    assert is_valid is True
    assert errors == []