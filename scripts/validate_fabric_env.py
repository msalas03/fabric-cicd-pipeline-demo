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

def main():
    env_mode = os.environ.get("FABRIC_ENV", "dev")

    if env_mode == "dev":
        print("[INFO] DEV mode detected - skipping strict validation.")
        sys.exit(0)

    print("[INFO] Validating Fabric execution environment...")

    missing_required = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    has_auth = any(os.environ.get(var) for var in AUTH_ENV_VARS)

    if missing_required:
        print("[ERROR] Missing required environment variables:")
        for var in missing_required:
            print(f" - {var}")

    if not has_auth:
        print("[ERROR] Missing authentication:")
        print(" - Set FABRIC_ID_TOKEN or FABRIC_REFRESH_TOKEN")

    if missing_required or not has_auth:
        print("[INFO] Validation failed.")
        sys.exit(1)

    print("[INFO] Validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()