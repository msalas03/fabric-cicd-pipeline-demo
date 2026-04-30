import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_PATH = BASE_DIR / "policies" / "deployment_policy.json"


def load_policy() -> dict:
    with open(POLICY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def evaluate_policy(
    environment: str,
    branch: str,
    deploy_relevant: bool,
    policy: dict,
) -> dict:
    env_policy = policy.get(environment)

    if env_policy is None:
        return {
            "deployment_allowed": False,
            "failed_checks": ["unknown_environment"],
            "decision_reason": f"No deployment policy defined for environment '{environment}'.",
        }

    failed_checks = []

    if env_policy.get("require_main_branch", False) and branch != "main":
        failed_checks.append("main_branch_required")

    if env_policy.get("require_deploy_relevant_changes", False) and not deploy_relevant:
        failed_checks.append("deploy_relevant_changes_required")

    deployment_allowed = len(failed_checks) == 0
    approval_required = env_policy.get("require_approval", False)

    if approval_required and deployment_allowed:
        decision_reason = "Deployment requires approval."
    elif deployment_allowed:
        decision_reason = "Deployment policy checks passed."
    else:
        reason_map = {
            "unknown_environment": "Unknown environment.",
            "main_branch_required": "Deployment requires the main branch.",
            "deploy_relevant_changes_required": "Deployment requires deploy-relevant changes.",
        }
        decision_reason = " ".join(reason_map[check] for check in failed_checks)

    return {
        "deployment_allowed": deployment_allowed,
        "failed_checks": failed_checks,
        "decision_reason": decision_reason,
        "approval_required": approval_required,
    }


def main():
    policy = load_policy()
    result = evaluate_policy(
        environment="dev",
        branch="main",
        deploy_relevant=False,
        policy=policy,
    )
    print(result)


if __name__ == "__main__":
    main()