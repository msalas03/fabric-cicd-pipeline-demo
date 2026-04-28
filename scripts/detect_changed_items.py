from pathlib import Path
from fabric_cicd import get_changed_items

def detect_changed_items(repo_dir: Path, compare_ref: str = "HEAD~1") -> list[str]:
    return get_changed_items(repository_directory=repo_dir, git_compare_ref=compare_ref)

def main():
    repo_dir = Path(__file__).resolve().parent.parent

    print("[INFO] Detecting changed items...")
    print(f"[INFO] Repository directory: {repo_dir}")

    try:
        changed_items = detect_changed_items(repo_dir)

        if changed_items:
            print("[INFO] Changed items detected:")
            for item in changed_items:
                print(f" - {item}")
        else:
            print("[INFO] No changed items detected.")

    except Exception as e:
        print("[ERROR] Failed to detect changed items:")
        print(e)
        raise

if __name__ == "__main__":
    main()