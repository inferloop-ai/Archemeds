# AI Code Editor - GitHub Repository Structure

```
ai-code-editor/
├── .github/                           # GitHub specific files
│   ├── workflows/                     # CI/CD workflows
│   │   ├── frontend-ci.yml
│   │   ├── backend-ci.yml
│   │   ├── e2e-tests.yml
│   │   ├── security-scan.yml
│   │   └── release.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── agent_improvement.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS
│
├── docs/                              # Documentation
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── ai-agents.md
│   │   ├── frontend-design.md
│   │   └── backend-design.md
│   ├── api/
│   │   ├── rest-api.md
│   │   ├── websocket-api.md
│   │   └── agent-protocols.md
│   ├── deployment/
│   │   ├── local-setup.md
│   │   ├── docker-deployment.md
│   │   ├── kubernetes-deployment.md
│   │   └── cloud-deployment.md
│   ├── development/
│   │   ├── getting-started.md
│   │   ├── contributing.md
│   │   ├── coding-standards.md
│   │   └── testing-guide.md
│   └── user-guide/
│       ├── quick-start.md
│       ├── features.md
│       └── troubleshooting.md
│
├── frontend/                          # React frontend application
│   ├── public/
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/                # Reusable components
│   │   │   ├── editor/
│   │   │   │   ├── MonacoEditor.tsx
│   │   │   │   ├── EditorTabs.tsx
│   │   │   │   ├── FileExplorer.tsx
│   │   │   │   └── index.ts
│   │   │   ├── chat/
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   ├── ChatInput.tsx
│   │   │   │   └── index.ts
│   │   │   ├── actions/
│   │   │   │   ├── ActionPanel.tsx
│   │   │   │   ├── ActionButton.tsx
│   │   │   │   └── index.ts
│   │   │   ├── diff/
│   │   │   │   ├── DiffViewer.tsx
│   │   │   │   ├── DiffControls.tsx
│   │   │   │   └── index.ts
│   │   │   ├── spec/
│   │   │   │   ├── SpecEditor.tsx
│   │   │   │   ├── RequirementsPanel.tsx
│   │   │   │   └── index.ts
│   │   │   ├── terminal/
│   │   │   │   ├── Terminal.tsx
│   │   │   │   ├── TerminalManager.tsx
│   │   │   │   └── index.ts
│   │   │   └── common/
│   │   │       ├── Button.tsx
│   │   │       ├── Modal.tsx
│   │   │       ├── Loading.tsx
│   │   │       └── index.ts
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useEditor.ts
│   │   │   ├── useChat.ts
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useFileManager.ts
│   │   │   └── useAgent.ts
│   │   ├── services/                  # API and service layers
│   │   │   ├── api/
│   │   │   │   ├── client.ts
│   │   │   │   ├── agents.ts
│   │   │   │   ├── files.ts
│   │   │   │   └── projects.ts
│   │   │   ├── websocket/
│   │   │   │   ├── connection.ts
│   │   │   │   ├── handlers.ts
│   │   │   │   └── types.ts
│   │   │   └── storage/
│   │   │       ├── localStorage.ts
│   │   │       └── indexedDB.ts
│   │   ├── store/                     # State management
│   │   │   ├── slices/
│   │   │   │   ├── editorSlice.ts
│   │   │   │   ├── chatSlice.ts
│   │   │   │   ├── projectSlice.ts
│   │   │   │   └── agentSlice.ts
│   │   │   ├── index.ts
│   │   │   └── types.ts
│   │   ├── types/                     # TypeScript type definitions
│   │   │   ├── editor.ts
│   │   │   ├── chat.ts
│   │   │   ├── agents.ts
│   │   │   ├── files.ts
│   │   │   └── api.ts
│   │   ├── utils/                     # Utility functions
│   │   │   ├── codeParser.ts
│   │   │   ├── diffUtils.ts
│   │   │   ├── fileUtils.ts
│   │   │   └── validation.ts
│   │   ├── styles/                    # Global styles
│   │   │   ├── globals.css
│   │   │   ├── components.css
│   │   │   └── themes.css
│   │   ├── App.tsx
│   │   ├── index.tsx
│   │   └── setupTests.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── vite.config.ts
│   └── .env.example
│
├── backend/                           # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── config.py                  # Configuration management
│   │   ├── dependencies.py            # Dependency injection
│   │   └── __init__.py
│   ├── api/                           # API routes
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── files.py
│   │   │   ├── projects.py
│   │   │   ├── agents.py
│   │   │   └── websocket.py
│   │   └── __init__.py
│   ├── core/                          # Core business logic
│   │   ├── orchestration/
│   │   │   ├── __init__.py
│   │   │   ├── intent_classifier.py
│   │   │   ├── planner.py
│   │   │   ├── executor.py
│   │   │   └── coordinator.py
│   │   ├── memory/
│   │   │   ├── __init__.py
│   │   │   ├── context_manager.py
│   │   │   ├── project_memory.py
│   │   │   ├── conversation_history.py
│   │   │   └── vector_store.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── gateway.py
│   │   │   ├── providers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── openai_provider.py
│   │   │   │   ├── claude_provider.py
│   │   │   │   └── deepseek_provider.py
│   │   │   ├── rate_limiter.py
│   │   │   └── cost_tracker.py
│   │   └── __init__.py
│   ├── agents/                        # AI agents
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── tools.py
│   │   │   └── protocols.py
│   │   ├── code/
│   │   │   ├── __init__.py
│   │   │   ├── code_agent.py
│   │   │   ├── generators/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── python_generator.py
│   │   │   │   ├── javascript_generator.py
│   │   │   │   └── typescript_generator.py
│   │   │   ├── parsers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ast_parser.py
│   │   │   │   └── tree_sitter_parser.py
│   │   │   └── validators/
│   │   │       ├── __init__.py
│   │   │       ├── syntax_validator.py
│   │   │       └── style_validator.py
│   │   ├── infrastructure/
│   │   │   ├── __init__.py
│   │   │   ├── infra_agent.py
│   │   │   ├── terraform_generator.py
│   │   │   ├── docker_generator.py
│   │   │   ├── kubernetes_generator.py
│   │   │   └── cloud_providers/
│   │   │       ├── __init__.py
│   │   │       ├── aws_provider.py
│   │   │       ├── gcp_provider.py
│   │   │       └── azure_provider.py
│   │   ├── testing/
│   │   │   ├── __init__.py
│   │   │   ├── test_agent.py
│   │   │   ├── generators/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── unit_test_generator.py
│   │   │   │   ├── integration_test_generator.py
│   │   │   │   └── e2e_test_generator.py
│   │   │   └── runners/
│   │   │       ├── __init__.py
│   │   │       ├── pytest_runner.py
│   │   │       ├── jest_runner.py
│   │   │       └── coverage_analyzer.py
│   │   ├── devops/
│   │   │   ├── __init__.py
│   │   │   ├── devops_agent.py
│   │   │   ├── ci_generators/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── github_actions.py
│   │   │   │   ├── gitlab_ci.py
│   │   │   │   └── circleci.py
│   │   │   └── deployment/
│   │   │       ├── __init__.py
│   │   │       ├── render_deployer.py
│   │   │       ├── vercel_deployer.py
│   │   │       └── aws_deployer.py
│   │   ├── documentation/
│   │   │   ├── __init__.py
│   │   │   ├── doc_agent.py
│   │   │   ├── generators/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── api_doc_generator.py
│   │   │   │   ├── readme_generator.py
│   │   │   │   └── comment_generator.py
│   │   │   └── parsers/
│   │   │       ├── __init__.py
│   │   │       └── docstring_parser.py
│   │   └── security/
│   │       ├── __init__.py
│   │       ├── security_agent.py
│   │       ├── scanners/
│   │       │   ├── __init__.py
│   │       │   ├── dependency_scanner.py
│   │       │   ├── code_scanner.py
│   │       │   └── secret_scanner.py
│   │       └── policies/
│   │           ├── __init__.py
│   │           └── security_policies.py
│   ├── services/                      # Business services
│   │   ├── __init__.py
│   │   ├── file_manager.py
│   │   ├── git_service.py
│   │   ├── project_service.py
│   │   ├── execution_service.py
│   │   └── workspace_service.py
│   ├── models/                        # Data models
│   │   ├── __init__.py
│   │   ├── agent_models.py
│   │   ├── chat_models.py
│   │   ├── file_models.py
│   │   ├── project_models.py
│   │   └── user_models.py
│   ├── database/                      # Database related
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── migrations/
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── project_repository.py
│   │       ├── chat_repository.py
│   │       └── user_repository.py
│   ├── utils/                         # Utility functions
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   ├── git_utils.py
│   │   ├── code_utils.py
│   │   └── validation.py
│   ├── tests/                         # Backend tests
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── unit/
│   │   │   ├── test_agents/
│   │   │   ├── test_services/
│   │   │   └── test_utils/
│   │   ├── integration/
│   │   │   ├── test_api/
│   │   │   ├── test_agents/
│   │   │   └── test_websocket/
│   │   └── e2e/
│   │       ├── test_workflows/
│   │       └── test_full_stack/
│   ├── requirements/                  # Python dependencies
│   │   ├── base.txt
│   │   ├── development.txt
│   │   ├── production.txt
│   │   └── testing.txt
│   ├── alembic/                       # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── Dockerfile
│   ├── .env.example
│   └── pyproject.toml
│
├── infrastructure/                    # Infrastructure as code
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   └── Dockerfile.nginx
│   ├── kubernetes/
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secrets.yaml
│   │   ├── deployments/
│   │   │   ├── frontend-deployment.yaml
│   │   │   ├── backend-deployment.yaml
│   │   │   ├── postgres-deployment.yaml
│   │   │   ├── redis-deployment.yaml
│   │   │   └── vector-db-deployment.yaml
│   │   ├── services/
│   │   │   ├── frontend-service.yaml
│   │   │   ├── backend-service.yaml
│   │   │   └── database-services.yaml
│   │   ├── ingress/
│   │   │   └── ingress.yaml
│   │   └── helm/
│   │       ├── Chart.yaml
│   │       ├── values.yaml
│   │       ├── values-dev.yaml
│   │       ├── values-prod.yaml
│   │       └── templates/
│   ├── terraform/
│   │   ├── modules/
│   │   │   ├── vpc/
│   │   │   ├── eks/
│   │   │   ├── rds/
│   │   │   └── redis/
│   │   ├── environments/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── terraform.tfvars.example
│   └── scripts/
│       ├── setup-dev.sh
│       ├── deploy.sh
│       ├── backup.sh
│       └── monitoring-setup.sh
│
├── shared/                            # Shared code between frontend/backend
│   ├── types/
│   │   ├── agent-protocols.ts
│   │   ├── api-schemas.ts
│   │   ├── websocket-events.ts
│   │   └── common.ts
│   ├── constants/
│   │   ├── agent-types.ts
│   │   ├── file-types.ts
│   │   └── error-codes.ts
│   └── utils/
│       ├── validation.ts
│       ├── formatting.ts
│       └── parsing.ts
│
├── tools/                             # Development and build tools
│   ├── scripts/
│   │   ├── setup.sh
│   │   ├── test.sh
│   │   ├── lint.sh
│   │   ├── build.sh
│   │   └── deploy.sh
│   ├── generators/
│   │   ├── agent-generator.py
│   │   ├── component-generator.js
│   │   └── api-generator.py
│   └── monitoring/
│       ├── prometheus.yml
│       ├── grafana/
│       │   ├── dashboards/
│       │   └── provisioning/
│       └── alerting/
│           └── rules.yml
│
├── tests/                             # Cross-stack tests
│   ├── e2e/
│   │   ├── specs/
│   │   │   ├── agent-workflows.spec.ts
│   │   │   ├── code-generation.spec.ts
│   │   │   └── collaboration.spec.ts
│   │   ├── fixtures/
│   │   └── support/
│   ├── integration/
│   │   ├── api-integration.test.js
│   │   └── websocket-integration.test.js
│   └── performance/
│       ├── load-tests/
│       └── benchmarks/
│
├── examples/                          # Example projects and demos
│   ├── sample-projects/
│   │   ├── fastapi-todo/
│   │   ├── react-dashboard/
│   │   └── microservices-setup/
│   ├── tutorials/
│   │   ├── getting-started.md
│   │   ├── custom-agents.md
│   │   └── deployment-guide.md
│   └── demos/
│       ├── video-scripts/
│       └── screenshots/
│
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── docker-compose.yml              # Main development environment
├── Makefile                        # Common development commands
├── package.json                    # Root package.json for workspace
├── pyproject.toml                  # Python project configuration
├── .env.example                    # Environment variables template
└── VERSION                         # Current version
```

## Key Directory Explanations

### Frontend (`/frontend`)
- **Components**: Modular React components organized by feature
- **Hooks**: Custom React hooks for state management and side effects
- **Services**: API clients and external service integrations
- **Store**: State management using Redux Toolkit or Zustand
- **Types**: TypeScript type definitions

### Backend (`/backend`)
- **API**: RESTful and WebSocket API endpoints
- **Core**: Business logic including orchestration and memory management
- **Agents**: Specialized AI agents for different tasks
- **Services**: Business services for file management, Git operations, etc.
- **Models**: Data models and schemas

### Infrastructure (`/infrastructure`)
- **Docker**: Container configurations for development and production
- **Kubernetes**: K8s manifests and Helm charts
- **Terraform**: Infrastructure as code for cloud deployments
- **Scripts**: Automation scripts for deployment and maintenance

### Shared (`/shared`)
- **Types**: Shared TypeScript definitions between frontend and backend
- **Constants**: Common constants and enums
- **Utils**: Utility functions used across the stack

### Tools (`/tools`)
- **Scripts**: Development automation scripts
- **Generators**: Code generators for agents, components, etc.
- **Monitoring**: Monitoring and observability configurations

This structure supports:
- **Monorepo architecture** with clear separation of concerns
- **Scalable development** with modular components and services
- **CI/CD integration** with proper testing and deployment workflows
- **Documentation-driven development** with comprehensive docs
- **Production readiness** with infrastructure as code and monitoring

The structure follows industry best practices and supports both development and production environments.