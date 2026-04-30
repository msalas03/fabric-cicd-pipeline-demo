import json
import os
from pathlib import Path


def load_plan(plan_path: Path) -> dict:
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def promote_plan(plan: dict, target_environment: str) -> dict:
    promoted = dict(plan)
    promoted["promotion_target"] = target_environment
    promoted["promoted_by"] = os.environ.get("GITHUB_ACTOR", "unknown")
    promoted["promotion_ref"] = os.environ.get("GITHUB_REF_NAME", "unknown")
    return promoted


def main():
    artifacts_dir = Path("artifacts")
    input_path = artifacts_dir / "deployment_plan.json"
    output_path = artifacts_dir / "promoted_deployment_plan.json"

    target_environment = os.environ.get("FABRIC_ENV", "qa")

    plan = load_plan(input_path)
    promoted = promote_plan(plan, target_environment)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(promoted, f, indent=2)

    print(f"[INFO] Promoted deployment plan written to: {output_path}")
    print(json.dumps(promoted, indent=2))


if __name__ == "__main__":
    main()