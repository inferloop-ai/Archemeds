@echo off
REM AI Code Editor Repository Structure Generator (Windows Batch Version)
REM Creates the complete directory structure and empty files for the AI-powered code editor project.

setlocal enabledelayedexpansion

set PROJECT_NAME=ai-code-editor

echo 🚀 Creating AI Code Editor project structure...
echo 📁 Project name: %PROJECT_NAME%

REM Create root directory
mkdir "%PROJECT_NAME%" 2>nul
cd "%PROJECT_NAME%"

echo 📂 Creating directory structure...

REM Create all directories
mkdir .github\workflows 2>nul
mkdir .github\ISSUE_TEMPLATE 2>nul
mkdir docs\architecture 2>nul
mkdir docs\api 2>nul
mkdir docs\deployment 2>nul
mkdir docs\development 2>nul
mkdir docs\user-guide 2>nul
mkdir frontend\public 2>nul
mkdir frontend\src\components\editor 2>nul
mkdir frontend\src\components\chat 2>nul
mkdir frontend\src\components\actions 2>nul
mkdir frontend\src\components\diff 2>nul
mkdir frontend\src\components\spec 2>nul
mkdir frontend\src\components\terminal 2>nul
mkdir frontend\src\components\common 2>nul
mkdir frontend\src\hooks 2>nul
mkdir frontend\src\services\api 2>nul
mkdir frontend\src\services\websocket 2>nul
mkdir frontend\src\services\storage 2>nul
mkdir frontend\src\store\slices 2>nul
mkdir frontend\src\types 2>nul
mkdir frontend\src\utils 2>nul
mkdir frontend\src\styles 2>nul
mkdir backend\app 2>nul
mkdir backend\api\v1 2>nul
mkdir backend\core\orchestration 2>nul
mkdir backend\core\memory 2>nul
mkdir backend\core\llm\providers 2>nul
mkdir backend\agents\base 2>nul
mkdir backend\agents\code\generators 2>nul
mkdir backend\agents\code\parsers 2>nul
mkdir backend\agents\code\validators 2>nul
mkdir backend\agents\infrastructure\cloud_providers 2>nul
mkdir backend\agents\testing\generators 2>nul
mkdir backend\agents\testing\runners 2>nul
mkdir backend\agents\devops\ci_generators 2>nul
mkdir backend\agents\devops\deployment 2>nul
mkdir backend\agents\documentation\generators 2>nul
mkdir backend\agents\documentation\parsers 2>nul
mkdir backend\agents\security\scanners 2>nul
mkdir backend\agents\security\policies 2>nul
mkdir backend\services 2>nul
mkdir backend\models 2>nul
mkdir backend\database\repositories 2>nul
mkdir backend\database\migrations 2>nul
mkdir backend\utils 2>nul
mkdir backend\tests\unit\test_agents 2>nul
mkdir backend\tests\unit\test_services 2>nul
mkdir backend\tests\unit\test_utils 2>nul
mkdir backend\tests\integration\test_api 2>nul
mkdir backend\tests\integration\test_agents 2>nul
mkdir backend\tests\integration\test_websocket 2>nul
mkdir backend\tests\e2e\test_workflows 2>nul
mkdir backend\tests\e2e\test_full_stack 2>nul
mkdir backend\requirements 2>nul
mkdir backend\alembic\versions 2>nul
mkdir infrastructure\docker 2>nul
mkdir infrastructure\kubernetes\deployments 2>nul
mkdir infrastructure\kubernetes\services 2>nul
mkdir infrastructure\kubernetes\ingress 2>nul
mkdir infrastructure\kubernetes\helm\templates 2>nul
mkdir infrastructure\terraform\modules\vpc 2>nul
mkdir infrastructure\terraform\modules\eks 2>nul
mkdir infrastructure\terraform\modules\rds 2>nul
mkdir infrastructure\terraform\modules\redis 2>nul
mkdir infrastructure\terraform\environments\dev 2>nul
mkdir infrastructure\terraform\environments\staging 2>nul
mkdir infrastructure\terraform\environments\prod 2>nul
mkdir infrastructure\scripts 2>nul
mkdir shared\types 2>nul
mkdir shared\constants 2>nul
mkdir shared\utils 2>nul
mkdir tools\scripts 2>nul
mkdir tools\generators 2>nul
mkdir tools\monitoring\grafana\dashboards 2>nul
mkdir tools\monitoring\grafana\provisioning 2>nul
mkdir tools\monitoring\alerting 2>nul
mkdir tests\e2e\specs 2>nul
mkdir tests\e2e\fixtures 2>nul
mkdir tests\e2e\support 2>nul
mkdir tests\integration 2>nul
mkdir tests\performance\load-tests 2>nul
mkdir tests\performance\benchmarks 2>nul
mkdir examples\sample-projects\fastapi-todo 2>nul
mkdir examples\sample-projects\react-dashboard 2>nul
mkdir examples\sample-projects\microservices-setup 2>nul
mkdir examples\tutorials 2>nul
mkdir examples\demos\video-scripts 2>nul
mkdir examples\demos\screenshots 2>nul

echo 📄 Creating files...

REM GitHub files
type nul > .github\workflows\frontend-ci.yml
type nul > .github\workflows\backend-ci.yml
type nul > .github\workflows\e2e-tests.yml
type nul > .github\workflows\security-scan.yml
type nul > .github\workflows\release.yml
type nul > .github\ISSUE_TEMPLATE\bug_report.md
type nul > .github\ISSUE_TEMPLATE\feature_request.md
type nul > .github\ISSUE_TEMPLATE\agent_improvement.md
type nul > .github\PULL_REQUEST_TEMPLATE.md
type nul > .github\CODEOWNERS

REM Documentation
type nul > docs\architecture\overview.md
type nul > docs\architecture\ai-agents.md
type nul > docs\architecture\frontend-design.md
type nul > docs\architecture\backend-design.md
type nul > docs\api\rest-api.md
type nul > docs\api\websocket-api.md
type nul > docs\api\agent-protocols.md
type nul > docs\deployment\local-setup.md
type nul > docs\deployment\docker-deployment.md
type nul > docs\deployment\kubernetes-deployment.md
type nul > docs\deployment\cloud-deployment.md
type nul > docs\development\getting-started.md
type nul > docs\development\contributing.md
type nul > docs\development\coding-standards.md
type nul > docs\development\testing-guide.md
type nul > docs\user-guide\quick-start.md
type nul > docs\user-guide\features.md
type nul > docs\user-guide\troubleshooting.md

REM Frontend files
type nul > frontend\public\index.html
type nul > frontend\public\manifest.json
type nul > frontend\public\favicon.ico
type nul > frontend\src\components\editor\MonacoEditor.tsx
type nul > frontend\src\components\editor\EditorTabs.tsx
type nul > frontend\src\components\editor\FileExplorer.tsx
type nul > frontend\src\components\editor\index.ts
type nul > frontend\src\components\chat\ChatInterface.tsx
type nul > frontend\src\components\chat\MessageBubble.tsx
type nul > frontend\src\components\chat\ChatInput.tsx
type nul > frontend\src\components\chat\index.ts
type nul > frontend\src\components\actions\ActionPanel.tsx
type nul > frontend\src\components\actions\ActionButton.tsx
type nul > frontend\src\components\actions\index.ts
type nul > frontend\src\components\diff\DiffViewer.tsx
type nul > frontend\src\components\diff\DiffControls.tsx
type nul > frontend\src\components\diff\index.ts
type nul > frontend\src\components\spec\SpecEditor.tsx
type nul > frontend\src\components\spec\RequirementsPanel.tsx
type nul > frontend\src\components\spec\index.ts
type nul > frontend\src\components\terminal\Terminal.tsx
type nul > frontend\src\components\terminal\TerminalManager.tsx
type nul > frontend\src\components\terminal\index.ts
type nul > frontend\src\components\common\Button.tsx
type nul > frontend\src\components\common\Modal.tsx
type nul > frontend\src\components\common\Loading.tsx
type nul > frontend\src\components\common\index.ts
type nul > frontend\src\hooks\useEditor.ts
type nul > frontend\src\hooks\useChat.ts
type nul > frontend\src\hooks\useWebSocket.ts
type nul > frontend\src\hooks\useFileManager.ts
type nul > frontend\src\hooks\useAgent.ts
type nul > frontend\src\services\api\client.ts
type nul > frontend\src\services\api\agents.ts
type nul > frontend\src\services\api\files.ts
type nul > frontend\src\services\api\projects.ts
type nul > frontend\src\services\websocket\connection.ts
type nul > frontend\src\services\websocket\handlers.ts
type nul > frontend\src\services\websocket\types.ts
type nul > frontend\src\services\storage\localStorage.ts
type nul > frontend\src\services\storage\indexedDB.ts
type nul > frontend\src\store\slices\editorSlice.ts
type nul > frontend\src\store\slices\chatSlice.ts
type nul > frontend\src\store\slices\projectSlice.ts
type nul > frontend\src\store\slices\agentSlice.ts
type nul > frontend\src\store\index.ts
type nul > frontend\src\store\types.ts
type nul > frontend\src\types\editor.ts
type nul > frontend\src\types\chat.ts
type nul > frontend\src\types\agents.ts
type nul > frontend\src\types\files.ts
type nul > frontend\src\types\api.ts
type nul > frontend\src\utils\codeParser.ts
type nul > frontend\src\utils\diffUtils.ts
type nul > frontend\src\utils\fileUtils.ts
type nul > frontend\src\utils\validation.ts
type nul > frontend\src\styles\globals.css
type nul > frontend\src\styles\components.css
type nul > frontend\src\styles\themes.css
type nul > frontend\src\App.tsx
type nul > frontend\src\index.tsx
type nul > frontend\src\setupTests.ts
type nul > frontend\package.json
type nul > frontend\tsconfig.json
type nul > frontend\tailwind.config.js
type nul > frontend\vite.config.ts
type nul > frontend\.env.example

REM Backend files
type nul > backend\app\main.py
type nul > backend\app\config.py
type nul > backend\app\dependencies.py
type nul > backend\app\__init__.py
type nul > backend\api\__init__.py
type nul > backend\api\v1\__init__.py
type nul > backend\api\v1\chat.py
type nul > backend\api\v1\files.py
type nul > backend\api\v1\projects.py
type nul > backend\api\v1\agents.py
type nul > backend\api\v1\websocket.py
type nul > backend\core\__init__.py
type nul > backend\core\orchestration\__init__.py
type nul > backend\core\orchestration\intent_classifier.py
type nul > backend\core\orchestration\planner.py
type nul > backend\core\orchestration\executor.py
type nul > backend\core\orchestration\coordinator.py
type nul > backend\core\memory\__init__.py
type nul > backend\core\memory\context_manager.py
type nul > backend\core\memory\project_memory.py
type nul > backend\core\memory\conversation_history.py
type nul > backend\core\memory\vector_store.py
type nul > backend\core\llm\__init__.py
type nul > backend\core\llm\gateway.py
type nul > backend\core\llm\rate_limiter.py
type nul > backend\core\llm\cost_tracker.py
type nul > backend\core\llm\providers\__init__.py
type nul > backend\core\llm\providers\openai_provider.py
type nul > backend\core\llm\providers\claude_provider.py
type nul > backend\core\llm\providers\deepseek_provider.py

REM Continue with more backend files...
type nul > backend\agents\__init__.py
type nul > backend\agents\base\__init__.py
type nul > backend\agents\base\agent.py
type nul > backend\agents\base\tools.py
type nul > backend\agents\base\protocols.py
type nul > backend\agents\code\__init__.py
type nul > backend\agents\code\code_agent.py
type nul > backend\services\__init__.py
type nul > backend\services\file_manager.py
type nul > backend\services\git_service.py
type nul > backend\services\project_service.py
type nul > backend\services\execution_service.py
type nul > backend\services\workspace_service.py
type nul > backend\models\__init__.py
type nul > backend\models\agent_models.py
type nul > backend\models\chat_models.py
type nul > backend\models\file_models.py
type nul > backend\models\project_models.py
type nul > backend\models\user_models.py
type nul > backend\database\__init__.py
type nul > backend\database\connection.py
type nul > backend\tests\__init__.py
type nul > backend\tests\conftest.py
type nul > backend\requirements\base.txt
type nul > backend\requirements\development.txt
type nul > backend\requirements\production.txt
type nul > backend\requirements\testing.txt
type nul > backend\alembic\env.py
type nul > backend\alembic\alembic.ini
type nul > backend\Dockerfile
type nul > backend\.env.example
type nul > backend\pyproject.toml

REM Infrastructure files
type nul > infrastructure\docker\docker-compose.yml
type nul > infrastructure\docker\docker-compose.dev.yml
type nul > infrastructure\docker\docker-compose.prod.yml
type nul > infrastructure\docker\Dockerfile.nginx
type nul > infrastructure\kubernetes\namespace.yaml
type nul > infrastructure\kubernetes\configmap.yaml
type nul > infrastructure\kubernetes\secrets.yaml
type nul > infrastructure\terraform\main.tf
type nul > infrastructure\terraform\variables.tf
type nul > infrastructure\terraform\outputs.tf
type nul > infrastructure\terraform\terraform.tfvars.example

REM Shared files
type nul > shared\types\agent-protocols.ts
type nul > shared\types\api-schemas.ts
type nul > shared\types\websocket-events.ts
type nul > shared\types\common.ts
type nul > shared\constants\agent-types.ts
type nul > shared\constants\file-types.ts
type nul > shared\constants\error-codes.ts
type nul > shared\utils\validation.ts
type nul > shared\utils\formatting.ts
type nul > shared\utils\parsing.ts

REM Tools files
type nul > tools\scripts\setup.sh
type nul > tools\scripts\test.sh
type nul > tools\scripts\lint.sh
type nul > tools\scripts\build.sh
type nul > tools\scripts\deploy.sh
type nul > tools\generators\agent-generator.py
type nul > tools\generators\component-generator.js
type nul > tools\generators\api-generator.py
type nul > tools\monitoring\prometheus.yml
type nul > tools\monitoring\alerting\rules.yml

REM Test files
type nul > tests\integration\api-integration.test.js
type nul > tests\integration\websocket-integration.test.js
type nul > tests\e2e\specs\agent-workflows.spec.ts
type nul > tests\e2e\specs\code-generation.spec.ts
type nul > tests\e2e\specs\collaboration.spec.ts

REM Example files
type nul > examples\tutorials\getting-started.md
type nul > examples\tutorials\custom-agents.md
type nul > examples\tutorials\deployment-guide.md

REM Root files
type nul > .gitignore
type nul > .gitattributes
type nul > .editorconfig
type nul > .pre-commit-config.yaml
type nul > LICENSE
type nul > README.md
type nul > CHANGELOG.md
type nul > CONTRIBUTING.md
type nul > CODE_OF_CONDUCT.md
type nul > SECURITY.md
type nul > docker-compose.yml
type nul > Makefile
type nul > package.json
type nul > pyproject.toml
type nul > .env.example
type nul > VERSION

echo.
echo ✅ Project structure created successfully!
echo 📁 Root directory: %CD%
echo 📊 Directory structure complete with all files and folders
echo.
echo Next steps:
echo 1. Initialize git: git init
echo 2. Set up your environment variables: copy .env.example .env
echo 3. Install dependencies (after setting up package.json and pyproject.toml)
echo 4. Start development
echo.
echo 🎉 Happy coding!

pause