from scripts.create_slice import build_command, get_config_path


def test_get_config_path_defaults_to_dev(monkeypatch):
    monkeypatch.delenv("FABRIC_ENV", raising=False)

    result = get_config_path()

    assert str(result).replace("\\", "/").endswith("configs/dev/slice_config.json")


def test_get_config_path_uses_prod(monkeypatch):
    monkeypatch.setenv("FABRIC_ENV", "prod")

    result = get_config_path()

    assert str(result).replace("\\", "/").endswith("configs/prod/slice_config.json")


def test_build_command_basic():
    config = {
        "slicename": "test",
        "slicegraph": "graph.json",
        "sshkey": "key",
    }

    cmd = build_command(config)

    assert "fabric-cli" in cmd
    assert "--slicename" in cmd
    assert "test" in cmd


def test_build_command_optional_fields():
    config = {
        "slicename": "test",
        "slicegraph": "graph.json",
        "sshkey": "key",
        "projectname": "proj",
        "scope": "all",
    }

    cmd = build_command(config)

    assert "--projectname" in cmd
    assert "--scope" in cmd