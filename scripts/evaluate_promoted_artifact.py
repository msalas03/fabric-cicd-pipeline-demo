import json
import os
from pathlib import Path


def load_plan(plan_path: Path) -> dict:
    with open(plan_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    artifacts_dir = Path("artifacts")

    promoted_path = artifacts_dir / "promoted_deployment_plan.json"
    base_path = artifacts_dir / "deployment_plan.json"

    plan_path = promoted_path if promoted_path.exists() else base_path

    plan = load_plan(plan_path)

    deployment_allowed = str(plan.get("deployment_allowed", False)).lower()
    decision_reason = plan.get("policy_decision_reason", "No decision reason available.")

    print(f"[INFO] Using plan file: {plan_path}")
    print(f"[INFO] deployment_allowed={deployment_allowed}")
    print(f"[INFO] decision_reason={decision_reason}")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"deployment_allowed={deployment_allowed}\n")
            f.write(f"decision_reason={decision_reason}\n")


if __name__ == "__main__":
    main()