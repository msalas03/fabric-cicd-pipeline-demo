import os
import subprocess
from pathlib import Path

from fabric_cicd import get_changed_items

DEPLOY_RELEVANT_PREFIXES = [
    "configs/",
    "scripts/",
]

def detect_fabric_changed_items(repo_dir: Path, compare_ref: str = "HEAD~1") -> list[str]:
    return get_changed_items(repository_directory=repo_dir, git_compare_ref=compare_ref)

def detect_git_changed_files(repo_dir: Path, compare_ref: str = "HEAD~1") -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", compare_ref, "HEAD"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files

def is_deploy_relevant(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized.startswith(prefix) for prefix in DEPLOY_RELEVANT_PREFIXES)

def classify_changed_items(changed_items: list[str]) -> dict:
    deploy_relevant = [item for item in changed_items if is_deploy_relevant(item)]
    non_deploy = [item for item in changed_items if not is_deploy_relevant(item)]

    return {
        "deploy_relevant": deploy_relevant,
        "non_deploy": non_deploy,
    }

def main():
    repo_dir = Path(__file__).resolve().parent.parent

    print("[INFO] Detecting changed items...")
    print(f"[INFO] Repository directory: {repo_dir}")

    fabric_changed_items = []
    git_changed_files = []

    try:
        fabric_changed_items = detect_fabric_changed_items(repo_dir)
    except Exception as e:
        print("[WARN] Fabric change detection failed:")
        print(e)

    try:
        git_changed_files = detect_git_changed_files(repo_dir)
    except Exception as e:
        print("[ERROR] Git file change detection failed:")
        print(e)
        raise

    print("\n[INFO] Fabric-recognized changed items:")
    if fabric_changed_items:
        for item in fabric_changed_items:
            print(f" - {item}")
    else:
        print(" - None")

    print("\n[INFO] Git changed files:")
    if git_changed_files:
        for item in git_changed_files:
            print(f" - {item}")
    else:
        print(" - None")

    classified = classify_changed_items(git_changed_files)

    print("\n[INFO] Deploy-relevant files:")
    if classified["deploy_relevant"]:
        for item in classified["deploy_relevant"]:
            print(f" - {item}")
    else:
        print(" - None")

    print("\n[INFO] Non-deploy files:")
    if classified["non_deploy"]:
        for item in classified["non_deploy"]:
            print(f" - {item}")
    else:
        print(" - None")

    has_deploy_relevant = bool(classified["deploy_relevant"])
    print(f"\n[INFO] Deploy relevant changes present: {has_deploy_relevant}")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"deploy_relevant={str(has_deploy_relevant).lower()}\n")

if __name__ == "__main__":
    main()