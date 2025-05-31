#!/usr/bin/env python3
"""
AI Code Editor Repository Structure Generator
Creates the complete directory structure and empty files for the AI-powered code editor project.
"""

import os
from pathlib import Path

def create_project_structure():
    """Create the complete project structure with directories and empty files."""
    
    # Project root
    root = "ai-code-editor"
    
    # Define the complete structure
    structure = {
        # GitHub specific files
        ".github/workflows": [
            "frontend-ci.yml",
            "backend-ci.yml", 
            "e2e-tests.yml",
            "security-scan.yml",
            "release.yml"
        ],
        ".github/ISSUE_TEMPLATE": [
            "bug_report.md",
            "feature_request.md",
            "agent_improvement.md"
        ],
        ".github": [
            "PULL_REQUEST_TEMPLATE.md",
            "CODEOWNERS"
        ],

        # Documentation
        "docs/architecture": [
            "overview.md",
            "ai-agents.md", 
            "frontend-design.md",
            "backend-design.md"
        ],
        "docs/api": [
            "rest-api.md",
            "websocket-api.md",
            "agent-protocols.md"
        ],
        "docs/deployment": [
            "local-setup.md",
            "docker-deployment.md",
            "kubernetes-deployment.md", 
            "cloud-deployment.md"
        ],
        "docs/development": [
            "getting-started.md",
            "contributing.md",
            "coding-standards.md",
            "testing-guide.md"
        ],
        "docs/user-guide": [
            "quick-start.md",
            "features.md",
            "troubleshooting.md"
        ],

        # Frontend
        "frontend/public": [
            "index.html",
            "manifest.json",
            "favicon.ico"
        ],
        "frontend/src/components/editor": [
            "MonacoEditor.tsx",
            "EditorTabs.tsx",
            "FileExplorer.tsx",
            "index.ts"
        ],
        "frontend/src/components/chat": [
            "ChatInterface.tsx",
            "MessageBubble.tsx",
            "ChatInput.tsx",
            "index.ts"
        ],
        "frontend/src/components/actions": [
            "ActionPanel.tsx",
            "ActionButton.tsx",
            "index.ts"
        ],
        "frontend/src/components/diff": [
            "DiffViewer.tsx",
            "DiffControls.tsx",
            "index.ts"
        ],
        "frontend/src/components/spec": [
            "SpecEditor.tsx",
            "RequirementsPanel.tsx",
            "index.ts"
        ],
        "frontend/src/components/terminal": [
            "Terminal.tsx",
            "TerminalManager.tsx",
            "index.ts"
        ],
        "frontend/src/components/common": [
            "Button.tsx",
            "Modal.tsx",
            "Loading.tsx",
            "index.ts"
        ],
        "frontend/src/hooks": [
            "useEditor.ts",
            "useChat.ts",
            "useWebSocket.ts",
            "useFileManager.ts",
            "useAgent.ts"
        ],
        "frontend/src/services/api": [
            "client.ts",
            "agents.ts",
            "files.ts",
            "projects.ts"
        ],
        "frontend/src/services/websocket": [
            "connection.ts",
            "handlers.ts",
            "types.ts"
        ],
        "frontend/src/services/storage": [
            "localStorage.ts",
            "indexedDB.ts"
        ],
        "frontend/src/store/slices": [
            "editorSlice.ts",
            "chatSlice.ts",
            "projectSlice.ts",
            "agentSlice.ts"
        ],
        "frontend/src/store": [
            "index.ts",
            "types.ts"
        ],
        "frontend/src/types": [
            "editor.ts",
            "chat.ts",
            "agents.ts",
            "files.ts",
            "api.ts"
        ],
        "frontend/src/utils": [
            "codeParser.ts",
            "diffUtils.ts",
            "fileUtils.ts",
            "validation.ts"
        ],
        "frontend/src/styles": [
            "globals.css",
            "components.css",
            "themes.css"
        ],
        "frontend/src": [
            "App.tsx",
            "index.tsx",
            "setupTests.ts"
        ],
        "frontend": [
            "package.json",
            "tsconfig.json",
            "tailwind.config.js",
            "vite.config.ts",
            ".env.example"
        ],

        # Backend
        "backend/app": [
            "main.py",
            "config.py",
            "dependencies.py",
            "__init__.py"
        ],
        "backend/api/v1": [
            "__init__.py",
            "chat.py",
            "files.py",
            "projects.py",
            "agents.py",
            "websocket.py"
        ],
        "backend/api": [
            "__init__.py"
        ],
        "backend/core/orchestration": [
            "__init__.py",
            "intent_classifier.py",
            "planner.py",
            "executor.py",
            "coordinator.py"
        ],
        "backend/core/memory": [
            "__init__.py",
            "context_manager.py",
            "project_memory.py",
            "conversation_history.py",
            "vector_store.py"
        ],
        "backend/core/llm/providers": [
            "__init__.py",
            "openai_provider.py",
            "claude_provider.py",
            "deepseek_provider.py"
        ],
        "backend/core/llm": [
            "__init__.py",
            "gateway.py",
            "rate_limiter.py",
            "cost_tracker.py"
        ],
        "backend/core": [
            "__init__.py"
        ],
        "backend/agents/base": [
            "__init__.py",
            "agent.py",
            "tools.py",
            "protocols.py"
        ],
        "backend/agents/code/generators": [
            "__init__.py",
            "python_generator.py",
            "javascript_generator.py",
            "typescript_generator.py"
        ],
        "backend/agents/code/parsers": [
            "__init__.py",
            "ast_parser.py",
            "tree_sitter_parser.py"
        ],
        "backend/agents/code/validators": [
            "__init__.py",
            "syntax_validator.py",
            "style_validator.py"
        ],
        "backend/agents/code": [
            "__init__.py",
            "code_agent.py"
        ],
        "backend/agents/infrastructure/cloud_providers": [
            "__init__.py",
            "aws_provider.py",
            "gcp_provider.py",
            "azure_provider.py"
        ],
        "backend/agents/infrastructure": [
            "__init__.py",
            "infra_agent.py",
            "terraform_generator.py",
            "docker_generator.py",
            "kubernetes_generator.py"
        ],
        "backend/agents/testing/generators": [
            "__init__.py",
            "unit_test_generator.py",
            "integration_test_generator.py",
            "e2e_test_generator.py"
        ],
        "backend/agents/testing/runners": [
            "__init__.py",
            "pytest_runner.py",
            "jest_runner.py",
            "coverage_analyzer.py"
        ],
        "backend/agents/testing": [
            "__init__.py",
            "test_agent.py"
        ],
        "backend/agents/devops/ci_generators": [
            "__init__.py",
            "github_actions.py",
            "gitlab_ci.py",
            "circleci.py"
        ],
        "backend/agents/devops/deployment": [
            "__init__.py",
            "render_deployer.py",
            "vercel_deployer.py",
            "aws_deployer.py"
        ],
        "backend/agents/devops": [
            "__init__.py",
            "devops_agent.py"
        ],
        "backend/agents/documentation/generators": [
            "__init__.py",
            "api_doc_generator.py",
            "readme_generator.py",
            "comment_generator.py"
        ],
        "backend/agents/documentation/parsers": [
            "__init__.py",
            "docstring_parser.py"
        ],
        "backend/agents/documentation": [
            "__init__.py",
            "doc_agent.py"
        ],
        "backend/agents/security/scanners": [
            "__init__.py",
            "dependency_scanner.py",
            "code_scanner.py",
            "secret_scanner.py"
        ],
        "backend/agents/security/policies": [
            "__init__.py",
            "security_policies.py"
        ],
        "backend/agents/security": [
            "__init__.py",
            "security_agent.py"
        ],
        "backend/agents": [
            "__init__.py"
        ],
        "backend/services": [
            "__init__.py",
            "file_manager.py",
            "git_service.py",
            "project_service.py",
            "execution_service.py",
            "workspace_service.py"
        ],
        "backend/models": [
            "__init__.py",
            "agent_models.py",
            "chat_models.py",
            "file_models.py",
            "project_models.py",
            "user_models.py"
        ],
        "backend/database/repositories": [
            "__init__.py",
            "project_repository.py",
            "chat_repository.py",
            "user_repository.py"
        ],
        "backend/database/migrations": [],
        "backend/database": [
            "__init__.py",
            "connection.py"
        ],
        "backend/utils": [
            "__init__.py",
            "file_utils.py",
            "git_utils.py",
            "code_utils.py",
            "validation.py"
        ],
        "backend/tests/unit/test_agents": [],
        "backend/tests/unit/test_services": [],
        "backend/tests/unit/test_utils": [],
        "backend/tests/integration/test_api": [],
        "backend/tests/integration/test_agents": [],
        "backend/tests/integration/test_websocket": [],
        "backend/tests/e2e/test_workflows": [],
        "backend/tests/e2e/test_full_stack": [],
        "backend/tests/unit": [],
        "backend/tests/integration": [],
        "backend/tests/e2e": [],
        "backend/tests": [
            "__init__.py",
            "conftest.py"
        ],
        "backend/requirements": [
            "base.txt",
            "development.txt",
            "production.txt",
            "testing.txt"
        ],
        "backend/alembic/versions": [],
        "backend/alembic": [
            "env.py",
            "alembic.ini"
        ],
        "backend": [
            "Dockerfile",
            ".env.example",
            "pyproject.toml"
        ],

        # Infrastructure
        "infrastructure/docker": [
            "docker-compose.yml",
            "docker-compose.dev.yml",
            "docker-compose.prod.yml",
            "Dockerfile.nginx"
        ],
        "infrastructure/kubernetes/deployments": [
            "frontend-deployment.yaml",
            "backend-deployment.yaml",
            "postgres-deployment.yaml",
            "redis-deployment.yaml",
            "vector-db-deployment.yaml"
        ],
        "infrastructure/kubernetes/services": [
            "frontend-service.yaml",
            "backend-service.yaml",
            "database-services.yaml"
        ],
        "infrastructure/kubernetes/ingress": [
            "ingress.yaml"
        ],
        "infrastructure/kubernetes/helm/templates": [],
        "infrastructure/kubernetes/helm": [
            "Chart.yaml",
            "values.yaml",
            "values-dev.yaml",
            "values-prod.yaml"
        ],
        "infrastructure/kubernetes": [
            "namespace.yaml",
            "configmap.yaml",
            "secrets.yaml"
        ],
        "infrastructure/terraform/modules/vpc": [],
        "infrastructure/terraform/modules/eks": [],
        "infrastructure/terraform/modules/rds": [],
        "infrastructure/terraform/modules/redis": [],
        "infrastructure/terraform/modules": [],
        "infrastructure/terraform/environments/dev": [],
        "infrastructure/terraform/environments/staging": [],
        "infrastructure/terraform/environments/prod": [],
        "infrastructure/terraform/environments": [],
        "infrastructure/terraform": [
            "main.tf",
            "variables.tf",
            "outputs.tf",
            "terraform.tfvars.example"
        ],
        "infrastructure/scripts": [
            "setup-dev.sh",
            "deploy.sh",
            "backup.sh",
            "monitoring-setup.sh"
        ],

        # Shared
        "shared/types": [
            "agent-protocols.ts",
            "api-schemas.ts",
            "websocket-events.ts",
            "common.ts"
        ],
        "shared/constants": [
            "agent-types.ts",
            "file-types.ts",
            "error-codes.ts"
        ],
        "shared/utils": [
            "validation.ts",
            "formatting.ts",
            "parsing.ts"
        ],

        # Tools
        "tools/scripts": [
            "setup.sh",
            "test.sh",
            "lint.sh",
            "build.sh",
            "deploy.sh"
        ],
        "tools/generators": [
            "agent-generator.py",
            "component-generator.js",
            "api-generator.py"
        ],
        "tools/monitoring/grafana/dashboards": [],
        "tools/monitoring/grafana/provisioning": [],
        "tools/monitoring/grafana": [],
        "tools/monitoring/alerting": [
            "rules.yml"
        ],
        "tools/monitoring": [
            "prometheus.yml"
        ],

        # Tests
        "tests/e2e/specs": [
            "agent-workflows.spec.ts",
            "code-generation.spec.ts",
            "collaboration.spec.ts"
        ],
        "tests/e2e/fixtures": [],
        "tests/e2e/support": [],
        "tests/e2e": [],
        "tests/integration": [
            "api-integration.test.js",
            "websocket-integration.test.js"
        ],
        "tests/performance/load-tests": [],
        "tests/performance/benchmarks": [],
        "tests/performance": [],

        # Examples
        "examples/sample-projects/fastapi-todo": [],
        "examples/sample-projects/react-dashboard": [],
        "examples/sample-projects/microservices-setup": [],
        "examples/sample-projects": [],
        "examples/tutorials": [
            "getting-started.md",
            "custom-agents.md",
            "deployment-guide.md"
        ],
        "examples/demos/video-scripts": [],
        "examples/demos/screenshots": [],
        "examples/demos": [],

        # Root files
        "": [
            ".gitignore",
            ".gitattributes", 
            ".editorconfig",
            ".pre-commit-config.yaml",
            "LICENSE",
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "docker-compose.yml",
            "Makefile",
            "package.json",
            "pyproject.toml",
            ".env.example",
            "VERSION"
        ]
    }

    print(f"Creating project structure in '{root}' directory...")
    
    # Create root directory
    root_path = Path(root)
    root_path.mkdir(exist_ok=True)
    
    # Create all directories and files
    for dir_path, files in structure.items():
        if dir_path:  # If not root directory
            full_dir_path = root_path / dir_path
        else:
            full_dir_path = root_path
            
        # Create directory
        full_dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {full_dir_path}")
        
        # Create files in directory
        for file_name in files:
            file_path = full_dir_path / file_name
            file_path.touch()
            print(f"Created file: {file_path}")
    
    print(f"\n✅ Project structure created successfully!")
    print(f"📁 Root directory: {root_path.absolute()}")
    print(f"📊 Total directories created: {len([d for d in structure.keys() if d])}")
    print(f"📄 Total files created: {sum(len(files) for files in structure.values())}")
    
    print(f"\nNext steps:")
    print(f"1. cd {root}")
    print(f"2. Initialize git: git init")
    print(f"3. Install dependencies: make setup (after creating Makefile)")
    print(f"4. Start development: make dev")

if __name__ == "__main__":
    create_project_structure()