from unittest.mock import patch

import pytest

from scripts.download_promoted_artifact import main


def test_download_requires_run_id(monkeypatch):
    monkeypatch.delenv("SOURCE_RUN_ID", raising=False)

    with pytest.raises(ValueError, match="SOURCE_RUN_ID is required"):
        main()


def test_download_invokes_gh_cli(monkeypatch):
    monkeypatch.setenv("SOURCE_RUN_ID", "12345")
    monkeypatch.setenv("SOURCE_ARTIFACT_NAME", "deployment-plan")

    with patch("scripts.download_promoted_artifact.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "downloaded"
        mock_run.return_value.stderr = ""

        main()

        args = mock_run.call_args[0][0]
        assert args[:3] == ["gh", "run", "download"]
        assert "12345" in args
        assert "deployment-plan" in args