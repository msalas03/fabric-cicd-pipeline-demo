## Module 3 – SDK Integration
- deploy_with_config is a high-level deployment entry point using a config file and Azure TokenCredential
- publish is a module, not a callable function
- publish_all_items publishes items using a FabricWorkspace object
- get_changed_items supports Git-based change detection for selective deployment
- FabricWorkspace appears to be the central object for representing deployment/publish context
- DeploymentResult provides structured deployment outcomes
- deploy_with_config requires both a config file path and a token_credential
- The SDK expects authentication as a Python credential object rather than only CLI/env-token input
- This makes the library more explicit and better suited for structured automation

fabric-cicd is a Python SDK-style deployment library, not just a shell wrapper. It supports config-driven deployment, workspace-based publishing, Git-aware change detection, and structured result handling.

The SDK is more flexible for automation because it uses explicit typed arguments like TokenCredential and returns structured results, which makes it easier to validate inputs, handle errors, and integrate into larger Python workflows.

Fabric CLI is useful for command-driven interaction, but the Fabric-CICD SDK is better suited for reusable automation because it relies on explicit Python objects, typed inputs, and structured deployment results.
