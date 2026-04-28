from pathlib import Path
from fabric_cicd import get_changed_items

DEPLOY_RELEVANT_PREFIXES = [
    "configs/",
    "scripts/",
]

def detect_changed_items(repo_dir: Path, compare_ref: str = "HEAD~1") -> list[str]:
    return get_changed_items(repository_directory=repo_dir, git_compare_ref=compare_ref)

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

    try:
        changed_items = detect_changed_items(repo_dir)
        classified = classify_changed_items(changed_items)

        if changed_items:
            print("[INFO] Changed items detected:")
            for item in changed_items:
                print(f" - {item}")
        else:
            print("[INFO] No changed items detected.")

        print("\n[INFO] Deploy-relevant items:")
        if classified["deploy_relevant"]:
            for item in classified["deploy_relevant"]:
                print(f" - {item}")
        else:
            print(" - None")

        print("\n[INFO] Non-deploy items:")
        if classified["non_deploy"]:
            for item in classified["non_deploy"]:
                print(f" - {item}")
        else:
            print(" - None")

    except Exception as e:
        print("[ERROR] Failed to detect or classify changed items:")
        print(e)
        raise

if __name__ == "__main__":
    main()