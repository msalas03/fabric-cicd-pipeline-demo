import os
import subprocess
from pathlib import Path


def main():
    run_id = os.environ.get("SOURCE_RUN_ID", "").strip()
    artifact_name = os.environ.get("SOURCE_ARTIFACT_NAME", "deployment-plan")
    output_dir = Path("artifacts")
    output_dir.mkdir(exist_ok=True)

    if not run_id:
        raise ValueError("SOURCE_RUN_ID is required for cross-run artifact download.")

    print(f"[INFO] Downloading artifact '{artifact_name}' from run ID {run_id}")

    result = subprocess.run(
        [
            "gh",
            "run",
            "download",
            run_id,
            "--name",
            artifact_name,
            "--dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Failed to download artifact from run {run_id}")

    print("[INFO] Artifact download completed.")


if __name__ == "__main__":
    main()