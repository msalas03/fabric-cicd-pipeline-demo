import os
import sys

REQUIRED_ENV_VARS = [
    "FABRIC_ORCHESTRATOR_HOST",
    "FABRIC_CREDMGR_HOST",
]

AUTH_ENV_VARS = [
    "FABRIC_ID_TOKEN",
    "FABRIC_REFRESH_TOKEN",
]

def validate_environment(env: dict) -> tuple[bool, list[str]]:
    required = ["FABRIC_ORCHESTRATOR_HOST", "FABRIC_CREDMGR_HOST"]
    missing = [var for var in required if not env.get(var)]

    has_auth = bool(env.get("FABRIC_ID_TOKEN") or env.get("FABRIC_REFRESH_TOKEN"))

    errors = []

    if missing:
        errors.append("missing_required")

    if not has_auth:
        errors.append("missing_auth")

    return (len(errors) == 0), errors

def main():
    print("[INFO] Validating Fabric execution environment...")

    is_valid, errors = validate_environment(os.environ)

    if "missing_required" in errors:
        print("[ERROR] Missing required environment variables:")
        print(" - FABRIC_ORCHESTRATOR_HOST")
        print(" - FABRIC_CREDMGR_HOST")

    if "missing_auth" in errors:
        print("[ERROR] Missing authentication:")
        print(" - Set FABRIC_ID_TOKEN or FABRIC_REFRESH_TOKEN")

    if not is_valid:
        print("[INFO] Validation failed.")
        sys.exit(1)

    print("[INFO] Validation passed.")
    sys.exit(0)