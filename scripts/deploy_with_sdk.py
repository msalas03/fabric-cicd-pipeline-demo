import inspect
from fabric_cicd import deploy_with_config, FabricWorkspace, DeploymentResult, get_changed_items

def main():
    print("[deploy_with_config signature]")
    print(inspect.signature(deploy_with_config))

    print("\n[FabricWorkspace]")
    print(FabricWorkspace)

    print("\n[FabricWorkspace __init__ signature]")
    print(inspect.signature(FabricWorkspace))

    print("\n[DeploymentResult]")
    print(DeploymentResult)

    print("\n[DeploymentResult __init__ signature]")
    print(inspect.signature(DeploymentResult))

    print("\n[get_changed_items signature]")
    print(inspect.signature(get_changed_items))

if __name__ == "__main__":
    main()