# Fabric CI/CD Pipeline Demo

## Overview

This project demonstrates a **production-style CI/CD pipeline** using:

* Fabric CLI
* Fabric-CICD Python SDK
* GitHub Actions
* Policy-driven deployment logic

The pipeline evolves from basic command execution into a **modular, environment-aware, and policy-governed deployment system**.

---

## Key Features

### 1. Multi-Stage CI/CD Pipeline

```text
lint → test → validate → deploy
```

* **Linting (Ruff)** ensures code quality
* **Unit tests (pytest)** validate behavior
* **Validation stage** evaluates environment and deployment plan
* **Deploy stage** executes only when policy allows

---

### 2. Environment-Aware Behavior

The pipeline supports:

* `dev` → relaxed validation, no approvals
* `prod` → strict validation, approval required

Environment is controlled via:

```yaml
workflow_dispatch → fabric_env input
```

---

### 3. Policy-Driven Deployment

Deployment rules are centralized in:

```text
policies/deployment_policy.json
```

Example:

```json
{
  "dev": {
    "require_main_branch": false,
    "require_deploy_relevant_changes": false,
    "require_approval": false
  },
  "prod": {
    "require_main_branch": true,
    "require_deploy_relevant_changes": true,
    "require_approval": true
  }
}
```

A Python policy evaluator determines:

* whether deployment is allowed
* which checks failed
* why the decision was made

---

### 4. Change Detection (Git + SDK)

The pipeline detects changes using:

* Fabric SDK (`get_changed_items`)
* Git diff (`git diff --name-only`)

Changes are classified as:

* **Deploy-relevant**
* **Non-deploy**

---

### 5. Deployment Plan Artifact

Each run generates:

```text
artifacts/deployment_plan.json
```

This includes:

* environment
* branch
* changed files
* deploy relevance
* policy decision
* reasoning

Example:

```json
{
  "environment": "dev",
  "branch": "main",
  "deploy_relevant": true,
  "deployment_allowed": false,
  "policy_decision_reason": "Not a production environment."
}
```

---

### 6. GitHub Actions Job Summary

Each run produces a **human-readable summary** directly in the Actions UI:

* environment
* changed files
* deploy-relevant files
* policy decision
* deployment outcome

---

### 7. Reusable Composite Action

The pipeline extracts logic into a reusable component:

```text
.github/actions/deployment-plan/
```

This action:

* sets up Python
* installs dependencies
* detects changes
* generates deployment plan
* exposes `deployment_allowed`

This enables reuse across workflows and projects.

---

### 8. Deployment Safety Controls

Deployment only proceeds when:

* environment is `prod`
* branch is `main`
* deploy-relevant changes exist
* policy allows deployment
* GitHub Environment approval is granted

---

## Project Structure

```text
.github/
  workflows/
  actions/
    deployment-plan/

configs/
  dev/
  prod/

policies/
  deployment_policy.json

scripts/
  create_slice.py
  detect_changed_items.py
  evaluate_deployment_policy.py
  generate_deployment_plan.py
  validate_fabric_env.py

tests/

artifacts/ (generated at runtime)
```

---

## Pipeline Flow

```text
1. Lint code
2. Run tests
3. Detect changes
4. Generate deployment plan
5. Evaluate deployment policy
6. Upload artifact
7. Validate environment
8. Deploy (if allowed)
```

---

## Key Concepts Demonstrated

* CI/CD pipeline design
* Policy-based deployment decisions
* Environment-aware configuration
* Change-based deployment gating
* Artifact-driven workflows
* Reusable GitHub Actions
* Separation of concerns (policy vs execution)

---

## Future Enhancements

* GitHub Environments with required reviewers
* Secrets management for real deployments
* Promotion model (dev → prod)
* Matrix testing across environments
* Reusable workflows across repositories

---

## Key Takeaway

This project demonstrates how to move from simple automation to a **structured, policy-driven CI/CD system** that separates decision logic, execution, and environment behavior.

---

## Status

![Fabric CI/CD Pipeline](https://github.com/msalas03/fabric-cicd-pipeline-demo/actions/workflows/fabric-ci.yml/badge.svg)
