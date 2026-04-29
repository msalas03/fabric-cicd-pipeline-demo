from scripts.create_slice import build_command


def test_build_command_basic():
    config = {
        "slicename": "test",
        "slicegraph": "graph.json",
        "sshkey": "key"
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
        "scope": "all"
    }

    cmd = build_command(config)

    assert "--projectname" in cmd
    assert "--scope" in cmd