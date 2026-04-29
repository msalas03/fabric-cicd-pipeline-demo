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


def get_environment(env: dict) -> str:
    return env.get("FABRIC_ENV", "dev")


def validate_environment(env: dict) -> tuple[bool, list[str]]:
    fabric_env = get_environment(env)

    if fabric_env == "dev":
        return True, []

    missing_required = [var for var in REQUIRED_ENV_VARS if not env.get(var)]
    has_auth = any(env.get(var) for var in AUTH_ENV_VARS)

    errors = []

    if missing_required:
        errors.append("missing_required")

    if not has_auth:
        errors.append("missing_auth")

    return len(errors) == 0, errors


def main():
    print("[INFO] Validating Fabric execution environment...")

    fabric_env = get_environment(os.environ)
    print(f"[INFO] FABRIC_ENV={fabric_env}")

    if fabric_env == "dev":
        print("[INFO] DEV mode detected - skipping strict validation.")
        sys.exit(0)

    is_valid, errors = validate_environment(os.environ)

    if "missing_required" in errors:
        print("[ERROR] Missing required environment variables:")
        for var in REQUIRED_ENV_VARS:
            print(f" - {var}")

    if "missing_auth" in errors:
        print("[ERROR] Missing authentication:")
        print(" - Set FABRIC_ID_TOKEN or FABRIC_REFRESH_TOKEN")

    if not is_valid:
        print("[INFO] Validation failed.")
        sys.exit(1)

    print("[INFO] Validation passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()