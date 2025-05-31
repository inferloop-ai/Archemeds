#!/bin/bash

# AI Code Editor Repository Structure Generator (Bash Version)
# Creates the complete directory structure and empty files for the AI-powered code editor project.

set -e  # Exit on any error

PROJECT_NAME="ai-code-editor"

echo "🚀 Creating AI Code Editor project structure..."
echo "📁 Project name: $PROJECT_NAME"

# Create root directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

echo "📂 Creating directory structure..."

# Create all directories
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE
mkdir -p docs/architecture
mkdir -p docs/api
mkdir -p docs/deployment
mkdir -p docs/development
mkdir -p docs/user-guide
mkdir -p frontend/public
mkdir -p frontend/src/components/editor
mkdir -p frontend/src/components/chat
mkdir -p frontend/src/components/actions
mkdir -p frontend/src/components/diff
mkdir -p frontend/src/components/spec
mkdir -p frontend/src/components/terminal
mkdir -p frontend/src/components/common
mkdir -p frontend/src/hooks
mkdir -p frontend/src/services/api
mkdir -p frontend/src/services/websocket
mkdir -p frontend/src/services/storage
mkdir -p frontend/src/store/slices
mkdir -p frontend/src/types
mkdir -p frontend/src/utils
mkdir -p frontend/src/styles
mkdir -p backend/app
mkdir -p backend/api/v1
mkdir -p backend/core/orchestration
mkdir -p backend/core/memory
mkdir -p backend/core/llm/providers
mkdir -p backend/agents/base
mkdir -p backend/agents/code/generators
mkdir -p backend/agents/code/parsers
mkdir -p backend/agents/code/validators
mkdir -p backend/agents/infrastructure/cloud_providers
mkdir -p backend/agents/testing/generators
mkdir -p backend/agents/testing/runners
mkdir -p backend/agents/devops/ci_generators
mkdir -p backend/agents/devops/deployment
mkdir -p backend/agents/documentation/generators
mkdir -p backend/agents/documentation/parsers
mkdir -p backend/agents/security/scanners
mkdir -p backend/agents/security/policies
mkdir -p backend/services
mkdir -p backend/models
mkdir -p backend/database/repositories
mkdir -p backend/database/migrations
mkdir -p backend/utils
mkdir -p backend/tests/unit/test_agents
mkdir -p backend/tests/unit/test_services
mkdir -p backend/tests/unit/test_utils
mkdir -p backend/tests/integration/test_api
mkdir -p backend/tests/integration/test_agents
mkdir -p backend/tests/integration/test_websocket
mkdir -p backend/tests/e2e/test_workflows
mkdir -p backend/tests/e2e/test_full_stack
mkdir -p backend/requirements
mkdir -p backend/alembic/versions
mkdir -p infrastructure/docker
mkdir -p infrastructure/kubernetes/deployments
mkdir -p infrastructure/kubernetes/services
mkdir -p infrastructure/kubernetes/ingress
mkdir -p infrastructure/kubernetes/helm/templates
mkdir -p infrastructure/terraform/modules/vpc
mkdir -p infrastructure/terraform/modules/eks
mkdir -p infrastructure/terraform/modules/rds
mkdir -p infrastructure/terraform/modules/redis
mkdir -p infrastructure/terraform/environments/dev
mkdir -p infrastructure/terraform/environments/staging
mkdir -p infrastructure/terraform/environments/prod
mkdir -p infrastructure/scripts
mkdir -p shared/types
mkdir -p shared/constants
mkdir -p shared/utils
mkdir -p tools/scripts
mkdir -p tools/generators
mkdir -p tools/monitoring/grafana/dashboards
mkdir -p tools/monitoring/grafana/provisioning
mkdir -p tools/monitoring/alerting
mkdir -p tests/e2e/specs
mkdir -p tests/e2e/fixtures
mkdir -p tests/e2e/support
mkdir -p tests/integration
mkdir -p tests/performance/load-tests
mkdir -p tests/performance/benchmarks
mkdir -p examples/sample-projects/fastapi-todo
mkdir -p examples/sample-projects/react-dashboard
mkdir -p examples/sample-projects/microservices-setup
mkdir -p examples/tutorials
mkdir -p examples/demos/video-scripts
mkdir -p examples/demos/screenshots

echo "📄 Creating files..."

# GitHub files
touch .github/workflows/frontend-ci.yml
touch .github/workflows/backend-ci.yml
touch .github/workflows/e2e-tests.yml
touch .github/workflows/security-scan.yml
touch .github/workflows/release.yml
touch .github/ISSUE_TEMPLATE/bug_report.md
touch .github/ISSUE_TEMPLATE/feature_request.md
touch .github/ISSUE_TEMPLATE/agent_improvement.md
touch .github/PULL_REQUEST_TEMPLATE.md
touch .github/CODEOWNERS

# Documentation
touch docs/architecture/overview.md
touch docs/architecture/ai-agents.md
touch docs/architecture/frontend-design.md
touch docs/architecture/backend-design.md
touch docs/api/rest-api.md
touch docs/api/websocket-api.md
touch docs/api/agent-protocols.md
touch docs/deployment/local-setup.md
touch docs/deployment/docker-deployment.md
touch docs/deployment/kubernetes-deployment.md
touch docs/deployment/cloud-deployment.md
touch docs/development/getting-started.md
touch docs/development/contributing.md
touch docs/development/coding-standards.md
touch docs/development/testing-guide.md
touch docs/user-guide/quick-start.md
touch docs/user-guide/features.md
touch docs/user-guide/troubleshooting.md

# Frontend files
touch frontend/public/index.html
touch frontend/public/manifest.json
touch frontend/public/favicon.ico
touch frontend/src/components/editor/MonacoEditor.tsx
touch frontend/src/components/editor/EditorTabs.tsx
touch frontend/src/components/editor/FileExplorer.tsx
touch frontend/src/components/editor/index.ts
touch frontend/src/components/chat/ChatInterface.tsx
touch frontend/src/components/chat/MessageBubble.tsx
touch frontend/src/components/chat/ChatInput.tsx
touch frontend/src/components/chat/index.ts
touch frontend/src/components/actions/ActionPanel.tsx
touch frontend/src/components/actions/ActionButton.tsx
touch frontend/src/components/actions/index.ts
touch frontend/src/components/diff/DiffViewer.tsx
touch frontend/src/components/diff/DiffControls.tsx
touch frontend/src/components/diff/index.ts
touch frontend/src/components/spec/SpecEditor.tsx
touch frontend/src/components/spec/RequirementsPanel.tsx
touch frontend/src/components/spec/index.ts
touch frontend/src/components/terminal/Terminal.tsx
touch frontend/src/components/terminal/TerminalManager.tsx
touch frontend/src/components/terminal/index.ts
touch frontend/src/components/common/Button.tsx
touch frontend/src/components/common/Modal.tsx
touch frontend/src/components/common/Loading.tsx
touch frontend/src/components/common/index.ts
touch frontend/src/hooks/useEditor.ts
touch frontend/src/hooks/useChat.ts
touch frontend/src/hooks/useWebSocket.ts
touch frontend/src/hooks/useFileManager.ts
touch frontend/src/hooks/useAgent.ts
touch frontend/src/services/api/client.ts
touch frontend/src/services/api/agents.ts
touch frontend/src/services/api/files.ts
touch frontend/src/services/api/projects.ts
touch frontend/src/services/websocket/connection.ts
touch frontend/src/services/websocket/handlers.ts
touch frontend/src/services/websocket/types.ts
touch frontend/src/services/storage/localStorage.ts
touch frontend/src/services/storage/indexedDB.ts
touch frontend/src/store/slices/editorSlice.ts
touch frontend/src/store/slices/chatSlice.ts
touch frontend/src/store/slices/projectSlice.ts
touch frontend/src/store/slices/agentSlice.ts
touch frontend/src/store/index.ts
touch frontend/src/store/types.ts
touch frontend/src/types/editor.ts
touch frontend/src/types/chat.ts
touch frontend/src/types/agents.ts
touch frontend/src/types/files.ts
touch frontend/src/types/api.ts
touch frontend/src/utils/codeParser.ts
touch frontend/src/utils/diffUtils.ts
touch frontend/src/utils/fileUtils.ts
touch frontend/src/utils/validation.ts
touch frontend/src/styles/globals.css
touch frontend/src/styles/components.css
touch frontend/src/styles/themes.css
touch frontend/src/App.tsx
touch frontend/src/index.tsx
touch frontend/src/setupTests.ts
touch frontend/package.json
touch frontend/tsconfig.json
touch frontend/tailwind.config.js
touch frontend/vite.config.ts
touch frontend/.env.example

# Backend files
touch backend/app/main.py
touch backend/app/config.py
touch backend/app/dependencies.py
touch backend/app/__init__.py
touch backend/api/__init__.py
touch backend/api/v1/__init__.py
touch backend/api/v1/chat.py
touch backend/api/v1/files.py
touch backend/api/v1/projects.py
touch backend/api/v1/agents.py
touch backend/api/v1/websocket.py
touch backend/core/__init__.py
touch backend/core/orchestration/__init__.py
touch backend/core/orchestration/intent_classifier.py
touch backend/core/orchestration/planner.py
touch backend/core/orchestration/executor.py
touch backend/core/orchestration/coordinator.py
touch backend/core/memory/__init__.py
touch backend/core/memory/context_manager.py
touch backend/core/memory/project_memory.py
touch backend/core/memory/conversation_history.py
touch backend/core/memory/vector_store.py
touch backend/core/llm/__init__.py
touch backend/core/llm/gateway.py
touch backend/core/llm/rate_limiter.py
touch backend/core/llm/cost_tracker.py
touch backend/core/llm/providers/__init__.py
touch backend/core/llm/providers/openai_provider.py
touch backend/core/llm/providers/claude_provider.py
touch backend/core/llm/providers/deepseek_provider.py
touch backend/agents/__init__.py
touch backend/agents/base/__init__.py
touch backend/agents/base/agent.py
touch backend/agents/base/tools.py
touch backend/agents/base/protocols.py
touch backend/agents/code/__init__.py
touch backend/agents/code/code_agent.py
touch backend/agents/code/generators/__init__.py
touch backend/agents/code/generators/python_generator.py
touch backend/agents/code/generators/javascript_generator.py
touch backend/agents/code/generators/typescript_generator.py
touch backend/agents/code/parsers/__init__.py
touch backend/agents/code/parsers/ast_parser.py
touch backend/agents/code/parsers/tree_sitter_parser.py
touch backend/agents/code/validators/__init__.py
touch backend/agents/code/validators/syntax_validator.py
touch backend/agents/code/validators/style_validator.py
touch backend/agents/infrastructure/__init__.py
touch backend/agents/infrastructure/infra_agent.py
touch backend/agents/infrastructure/terraform_generator.py
touch backend/agents/infrastructure/docker_generator.py
touch backend/agents/infrastructure/kubernetes_generator.py
touch backend/agents/infrastructure/cloud_providers/__init__.py
touch backend/agents/infrastructure/cloud_providers/aws_provider.py
touch backend/agents/infrastructure/cloud_providers/gcp_provider.py
touch backend/agents/infrastructure/cloud_providers/azure_provider.py
touch backend/agents/testing/__init__.py
touch backend/agents/testing/test_agent.py
touch backend/agents/testing/generators/__init__.py
touch backend/agents/testing/generators/unit_test_generator.py
touch backend/agents/testing/generators/integration_test_generator.py
touch backend/agents/testing/generators/e2e_test_generator.py
touch backend/agents/testing/runners/__init__.py
touch backend/agents/testing/runners/pytest_runner.py
touch backend/agents/testing/runners/jest_runner.py
touch backend/agents/testing/runners/coverage_analyzer.py
touch backend/agents/devops/__init__.py
touch backend/agents/devops/devops_agent.py
touch backend/agents/devops/ci_generators/__init__.py
touch backend/agents/devops/ci_generators/github_actions.py
touch backend/agents/devops/ci_generators/gitlab_ci.py
touch backend/agents/devops/ci_generators/circleci.py
touch backend/agents/devops/deployment/__init__.py
touch backend/agents/devops/deployment/render_deployer.py
touch backend/agents/devops/deployment/vercel_deployer.py
touch backend/agents/devops/deployment/aws_deployer.py
touch backend/agents/documentation/__init__.py
touch backend/agents/documentation/doc_agent.py
touch backend/agents/documentation/generators/__init__.py
touch backend/agents/documentation/generators/api_doc_generator.py
touch backend/agents/documentation/generators/readme_generator.py
touch backend/agents/documentation/generators/comment_generator.py
touch backend/agents/documentation/parsers/__init__.py
touch backend/agents/documentation/parsers/docstring_parser.py
touch backend/agents/security/__init__.py
touch backend/agents/security/security_agent.py
touch backend/agents/security/scanners/__init__.py
touch backend/agents/security/scanners/dependency_scanner.py
touch backend/agents/security/scanners/code_scanner.py
touch backend/agents/security/scanners/secret_scanner.py
touch backend/agents/security/policies/__init__.py
touch backend/agents/security/policies/security_policies.py
touch backend/services/__init__.py
touch backend/services/file_manager.py
touch backend/services/git_service.py
touch backend/services/project_service.py
touch backend/services/execution_service.py
touch backend/services/workspace_service.py
touch backend/models/__init__.py
touch backend/models/agent_models.py
touch backend/models/chat_models.py
touch backend/models/file_models.py
touch backend/models/project_models.py
touch backend/models/user_models.py
touch backend/database/__init__.py
touch backend/database/connection.py
touch backend/database/repositories/__init__.py
touch backend/database/repositories/project_repository.py
touch backend/database/repositories/chat_repository.py
touch backend/database/repositories/user_repository.py
touch backend/utils/__init__.py
touch backend/utils/file_utils.py
touch backend/utils/git_utils.py
touch backend/utils/code_utils.py
touch backend/utils/validation.py
touch backend/tests/__init__.py
touch backend/tests/conftest.py
touch backend/requirements/base.txt
touch backend/requirements/development.txt
touch backend/requirements/production.txt
touch backend/requirements/testing.txt
touch backend/alembic/env.py
touch backend/alembic/alembic.ini
touch backend/Dockerfile
touch backend/.env.example
touch backend/pyproject.toml

# Infrastructure files
touch infrastructure/docker/docker-compose.yml
touch infrastructure/docker/docker-compose.dev.yml
touch infrastructure/docker/docker-compose.prod.yml
touch infrastructure/docker/Dockerfile.nginx
touch infrastructure/kubernetes/namespace.yaml
touch infrastructure/kubernetes/configmap.yaml
touch infrastructure/kubernetes/secrets.yaml
touch infrastructure/kubernetes/deployments/frontend-deployment.yaml
touch infrastructure/kubernetes/deployments/backend-deployment.yaml
touch infrastructure/kubernetes/deployments/postgres-deployment.yaml
touch infrastructure/kubernetes/deployments/redis-deployment.yaml
touch infrastructure/kubernetes/deployments/vector-db-deployment.yaml
touch infrastructure/kubernetes/services/frontend-service.yaml
touch infrastructure/kubernetes/services/backend-service.yaml
touch infrastructure/kubernetes/services/database-services.yaml
touch infrastructure/kubernetes/ingress/ingress.yaml
touch infrastructure/kubernetes/helm/Chart.yaml
touch infrastructure/kubernetes/helm/values.yaml
touch infrastructure/kubernetes/helm/values-dev.yaml
touch infrastructure/kubernetes/helm/values-prod.yaml
touch infrastructure/terraform/main.tf
touch infrastructure/terraform/variables.tf
touch infrastructure/terraform/outputs.tf
touch infrastructure/terraform/terraform.tfvars.example
touch infrastructure/scripts/setup-dev.sh
touch infrastructure/scripts/deploy.sh
touch infrastructure/scripts/backup.sh
touch infrastructure/scripts/monitoring-setup.sh

# Shared files
touch shared/types/agent-protocols.ts
touch shared/types/api-schemas.ts
touch shared/types/websocket-events.ts
touch shared/types/common.ts
touch shared/constants/agent-types.ts
touch shared/constants/file-types.ts
touch shared/constants/error-codes.ts
touch shared/utils/validation.ts
touch shared/utils/formatting.ts
touch shared/utils/parsing.ts

# Tools files
touch tools/scripts/setup.sh
touch tools/scripts/test.sh
touch tools/scripts/lint.sh
touch tools/scripts/build.sh
touch tools/scripts/deploy.sh
touch tools/generators/agent-generator.py
touch tools/generators/component-generator.js
touch tools/generators/api-generator.py
touch tools/monitoring/prometheus.yml
touch tools/monitoring/alerting/rules.yml

# Test files
touch tests/integration/api-integration.test.js
touch tests/integration/websocket-integration.test.js
touch tests/e2e/specs/agent-workflows.spec.ts
touch tests/e2e/specs/code-generation.spec.ts
touch tests/e2e/specs/collaboration.spec.ts

# Example files
touch examples/tutorials/getting-started.md
touch examples/tutorials/custom-agents.md
touch examples/tutorials/deployment-guide.md

# Root files
touch .gitignore
touch .gitattributes
touch .editorconfig
touch .pre-commit-config.yaml
touch LICENSE
touch README.md
touch CHANGELOG.md
touch CONTRIBUTING.md
touch CODE_OF_CONDUCT.md
touch SECURITY.md
touch docker-compose.yml
touch Makefile
touch package.json
touch pyproject.toml
touch .env.example
touch VERSION

# Make scripts executable
chmod +x tools/scripts/*.sh
chmod +x infrastructure/scripts/*.sh
chmod +x tools/generators/*.py

echo ""
echo "✅ Project structure created successfully!"
echo "📁 Root directory: $(pwd)"
echo "📊 Directory structure complete with all files and folders"
echo ""
echo "Next steps:"
echo "1. Initialize git: git init"
echo "2. Set up your environment variables: cp .env.example .env"
echo "3. Install dependencies (after setting up package.json and pyproject.toml)"
echo "4. Start development"
echo ""
echo "🎉 Happy coding!"