import json
import os
from datetime import UTC, datetime
from pathlib import Path

from scripts.detect_changed_items import (
    classify_changed_items,
    detect_fabric_changed_items,
    detect_git_changed_files,
)


def build_deployment_plan(
    environment: str,
    fabric_changed_items: list[str],
    git_changed_files: list[str],
    deploy_relevant_files: list[str],
    non_deploy_files: list[str],
) -> dict:
    return {
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "environment": environment,
        "deploy_relevant": bool(deploy_relevant_files),
        "fabric_changed_items": fabric_changed_items,
        "git_changed_files": git_changed_files,
        "deploy_relevant_files": deploy_relevant_files,
        "non_deploy_files": non_deploy_files,
    }

def main():
    repo_dir = Path(__file__).resolve().parent.parent
    artifacts_dir = repo_dir / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    environment = os.environ.get("FABRIC_ENV", "dev")

    fabric_changed_items = []
    try:
        fabric_changed_items = detect_fabric_changed_items(repo_dir)
    except Exception as e:
        print("[WARN] Fabric-aware change detection failed:")
        print(e)

    git_changed_files = detect_git_changed_files(repo_dir)
    classified = classify_changed_items(git_changed_files)

    plan = build_deployment_plan(
        environment=environment,
        fabric_changed_items=fabric_changed_items,
        git_changed_files=git_changed_files,
        deploy_relevant_files=classified["deploy_relevant"],
        non_deploy_files=classified["non_deploy"],
    )

    output_path = artifacts_dir / "deployment_plan.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)

    print(f"[INFO] Deployment plan written to: {output_path}")
    print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()