# Fabric CLI Learning

## Environment Setup
- Python version: 3.13
- Virtual environment: venv\Scripts\activate
- Installed packages: fabric-cicd 1.0.0, fabric-cli 0.8
- CLI command confirmed as: `fabric-cli`
- File path terminal navigation: cd [location] 
- Execute file in terminal: python [file_name]


## Commands Explored
- fabric-cli --help
- fabric-cli resources --help
resources → ask the orchestrator what infrastructure/resources are available

- fabric-cli slices --help
slices → create, delete, or query user slices

- fabric-cli slivers --help
slivers → query slivers associated with slices

- fabric-cli tokens --help
tokens → issue, refresh, or revoke auth tokens through the credential manager


## Initial Observations
- High level overview
Fabric CLI is a command-line interface for working with FABRIC’s remote infrastructure services. It uses configured service endpoints and authentication to create, query, and manage environment resources and access tokens.

- What the CLI appears to manage - this CLI talks to remote FABRIC services over APIs
It is a client for the FABRIC testbed services: token management, slice management, sliver management, and resource queries. The orchestrator side handles slice/sliver/resource operations, and the credential manager handles token creation/refresh/revoke.

- Which commands may require credentials
assume most nontrivial remote commands require authentication unless proven otherwise.

- Which environment variables are referenced
In practical terms, these are settings the CLI reads automatically so you do not have to type them on every command. Variables such as FABRIC_ORCHESTRATOR_HOST, FABRIC_CREDMGR_HOST, FABRIC_TOKEN_LOCATION, and FABRIC_PROJECT_ID.

- Any terminology that is unfamiliar
FABRIC_ORCHESTRATOR_HOST points the CLI to the orchestrator service.
FABRIC_CREDMGR_HOST points the CLI to the credential manager service.

- Key Insights
This CLI is tightly coupled to remote services and won’t even fully expose command details without configuration.
$env:FABRIC_ORCHESTRATOR_HOST="dummy-host"
$env:FABRIC_CREDMGR_HOST="dummy-host"

- What inputs does create require
--slicename TEXT     Slice Name  [required]
--slicegraph TEXT    Slice Graph  [required]
--sshkey TEXT        SSH Key  [required]
--idtoken TEXT       Fabric Identity Token OR --refreshtoken TEXT  Fabric Refresh Token
--projectname TEXT   project name
--scope [cf|mf|all]  scope

- What does a “slice” appear to represent
Slice = environment
Slivers = components inside that environment
Slice graph = blueprint of the environment

- What does issuing a token involve
authenticating with the credential manager to obtain an access token used for subsequent CLI operations