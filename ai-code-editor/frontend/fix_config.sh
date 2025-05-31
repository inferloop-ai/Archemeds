#!/bin/bash
# Fix Frontend Configuration Files
# Run this from the ai-code-editor/frontend directory

echo "🔧 Fixing frontend configuration files..."

# 1. Create tsconfig.json
echo "📄 Creating tsconfig.json..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

# 2. Create tsconfig.node.json
echo "📄 Creating tsconfig.node.json..."
cat > tsconfig.node.json << 'EOF'
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
EOF

# 3. Create postcss.config.js for Tailwind
echo "📄 Creating postcss.config.js..."
cat > postcss.config.js << 'EOF'
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

# 4. Create .eslintrc.cjs
echo "📄 Creating .eslintrc.cjs..."
cat > .eslintrc.cjs << 'EOF'
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    '@typescript-eslint/recommended-requiring-type-checking',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
  },
}
EOF

# 5. Check if root package.json exists and fix it
if [ -f "../package.json" ]; then
    if [ ! -s "../package.json" ]; then
        echo "📄 Creating root package.json..."
        cat > ../package.json << 'EOF'
{
  "name": "ai-code-editor",
  "version": "0.1.0",
  "description": "AI-powered code editor with multi-agent system",
  "scripts": {
    "dev:frontend": "cd frontend && npm run dev",
    "dev:backend": "cd backend && python -m app.main",
    "install:frontend": "cd frontend && npm install",
    "install:backend": "cd backend && pip install -r requirements.txt"
  },
  "keywords": ["ai", "code-editor", "agents", "fastapi", "react"],
  "license": "MIT"
}
EOF
    fi
fi

# 6. Ensure package.json has correct content
echo "📄 Verifying frontend package.json..."
if [ ! -s "package.json" ]; then
    cat > package.json << 'EOF'
{
  "name": "ai-code-editor-frontend",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@monaco-editor/react": "^4.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.0",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5",
    "typescript": "^5.2.2",
    "vite": "^4.5.0"
  },
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  }
}
EOF
fi

# 7. Create index.html if it doesn't exist or is empty
if [ ! -s "index.html" ]; then
    echo "📄 Creating index.html..."
    cat > index.html << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Code Editor</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
EOF
fi

# 8. Fix main entry point
if [ ! -f "src/main.tsx" ]; then
    echo "📄 Creating src/main.tsx..."
    mkdir -p src
    cat > src/main.tsx << 'EOF'
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
EOF
fi

echo ""
echo "✅ Configuration files fixed!"
echo ""
echo "🚀 Now try:"
echo "1. npm install"
echo "2. npm run dev"
echo ""
echo "If you still get errors, try:"
echo "rm -rf node_modules package-lock.json && npm install"