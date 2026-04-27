# Fabric CI/CD Pipeline Demo

## Overview

This project demonstrates a structured approach to building CI/CD workflows using the **Fabric CLI**, **Fabric-CICD Python SDK**, and **GitHub Actions**.

The focus is on moving from manual, command-line interactions to **config-driven, automated deployment pipelines** that are maintainable, testable, and CI/CD-ready.

---

## Objectives

* Understand how Fabric CLI interacts with remote services
* Transition from CLI-based execution to SDK-based automation
* Build reusable, config-driven deployment logic
* Implement fail-fast validation patterns
* Integrate workflows into GitHub Actions

---

## Tech Stack

* Python 3.13
* fabric-cli
* fabric-cicd (v1.0.0)
* GitHub Actions
* JSON-based configuration

---

## Architecture Overview

This project demonstrates two approaches to automation:

### 1. CLI-Based Workflow

```text
Python Script → subprocess → fabric-cli → Remote Services
```

* Fast to prototype
* Relies on environment variables and shell context
* Returns unstructured output (stdout/stderr)

---

### 2. SDK-Based Workflow

```text
Python Script → fabric_cicd SDK → Structured Objects → Remote Services
```

* Uses typed inputs (e.g., TokenCredential)
* Returns structured results (DeploymentResult)
* Better suited for CI/CD and testing

---

## Project Structure

```text
fabric-cicd-pipeline-demo/
│
├── .github/workflows/        # CI/CD pipelines
├── configs/                 # JSON configuration files
├── scripts/                 # Python automation scripts
├── notes/                   # Learning modules and breakdowns
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Key Components

### Config-Driven Design

Deployment inputs are externalized into JSON files:

* `slice_config.json`
* `graph-definition.json`

This enables:

* reusability
* separation of logic and configuration
* easier CI/CD integration

---

### CLI Automation

`scripts/create_slice.py`:

* Builds dynamic CLI commands
* Executes via subprocess
* Captures stdout/stderr
* Implements environment validation

---

### SDK Integration

`scripts/deploy_with_sdk.py`:

* Uses `fabric_cicd.deploy_with_config`
* Demonstrates required inputs (config + TokenCredential)
* Inspects core SDK objects:

  * `FabricWorkspace`
  * `DeploymentResult`
  * `get_changed_items`

---

### Validation Layer

`scripts/validate_fabric_env.py`:

* Ensures required environment variables exist
* Implements **fail-fast behavior**
* Prevents invalid pipeline execution

---

### CI/CD Pipeline

`.github/workflows/fabric-ci.yml`:

* Runs on push and manual trigger
* Installs dependencies
* Executes Python scripts
* Validates environment configuration

---

## Key Learnings

### CLI vs SDK Tradeoff

* CLI is useful for quick execution but harder to scale
* SDK provides structured inputs/outputs and better integration for automation

### Fail-Fast Design

Early validation of environment variables and dependencies:

* reduces debugging complexity
* prevents wasted CI/CD runs
* improves reliability

### Environment-Driven Configuration

The workflow depends on:

* service endpoints
* authentication tokens
* runtime environment variables

---

## Example Workflow Execution

1. GitHub Action is triggered
2. Python environment is initialized
3. Dependencies are installed
4. Validation script checks environment variables
5. SDK inspection script runs successfully

---

## Limitations (Intentional)

This project does **not** include real Fabric credentials.
Instead, it focuses on:

* structure
* automation patterns
* pipeline design

This mirrors early-stage CI/CD development before secrets are introduced.

---

## Future Enhancements

* Integrate GitHub Secrets for real authentication
* Implement selective deployment using `get_changed_items`
* Add multi-environment support (dev/test/prod)
* Extend pipeline with approval gates

---

## Key Takeaway

This project demonstrates how to transition from manual CLI usage to a **structured, scalable CI/CD pipeline** using Python and GitHub Actions. The SDK-based approach provides a more maintainable and testable foundation for real-world deployment automation.
