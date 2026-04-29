import json
import os
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "configs"

def get_environment() -> str:
    return os.environ.get("FABRIC_ENV", "dev")

def get_config_path() -> Path:
    env_name = get_environment()
    return CONFIG_DIR / env_name / "slice_config.json"

def load_config():
    config_path = get_config_path()
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_command(config):
    slicegraph_path = str(CONFIG_DIR / config["slicegraph"])

    cmd = [
        "fabric-cli", "slices", "create",
        "--slicename", config["slicename"],
        "--slicegraph", slicegraph_path,
        "--sshkey", config["sshkey"]
    ]

    if "projectname" in config:
        cmd += ["--projectname", config["projectname"]]

    if "scope" in config:
        cmd += ["--scope", config["scope"]]

    return cmd

def validate_env():
    required = ["FABRIC_ORCHESTRATOR_HOST", "FABRIC_CREDMGR_HOST"]
    missing = [var for var in required if not os.environ.get(var)]

    has_token = bool(os.environ.get("FABRIC_ID_TOKEN") or os.environ.get("FABRIC_REFRESH_TOKEN"))

    if missing:
        print("[ERROR] Missing required environment variables:")
        for var in missing:
            print(f" - {var}")

    if not has_token:
        print("[ERROR] Missing authentication: set FABRIC_ID_TOKEN or FABRIC_REFRESH_TOKEN")

    if missing or not has_token:
        return False

    return True

def run():
    if not validate_env():
        print("[INFO] Validation failed. Exiting.")
        sys.exit(1)

    print(f"[INFO] Using FABRIC_ENV={get_environment()}")
    print(f"[INFO] Loading config from: {get_config_path()}")

    config = load_config()
    cmd = build_command(config)

    print("[INFO] Running Fabric CLI command")
    print("[INFO] Command:", " ".join(cmd))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)

        print("\n[STDOUT]\n", result.stdout)
        print("\n[STDERR]\n", result.stderr)

        if result.returncode != 0:
            print(f"[ERROR] Command failed with exit code {result.returncode}")
            sys.exit(result.returncode)

    except Exception as e:
        print("[ERROR] Exception during command execution:", e)
        sys.exit(1)

if __name__ == "__main__":
    run()