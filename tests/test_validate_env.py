from scripts.validate_fabric_env import validate_environment


def test_valid_environment():
    env = {
        "FABRIC_ORCHESTRATOR_HOST": "x",
        "FABRIC_CREDMGR_HOST": "y",
        "FABRIC_ID_TOKEN": "token"
    }

    is_valid, errors = validate_environment(env)

    assert is_valid is True
    assert errors == []

def test_missing_required_vars():
    env = {}

    is_valid, errors = validate_environment(env)

    assert is_valid is False
    assert "missing_required" in errors

def test_missing_auth():
    env = {
        "FABRIC_ORCHESTRATOR_HOST": "x",
        "FABRIC_CREDMGR_HOST": "y"
    }

    is_valid, errors = validate_environment(env)

    assert is_valid is False
    assert "missing_auth" in errors