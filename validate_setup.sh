#!/bin/bash

# Sims 4 AI Gaming Assistant - Setup Validation Script
# This script validates that the development environment is properly configured

set -e

echo "🔍 Validating Sims 4 AI Gaming Assistant setup..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Python package is installed
python_package_exists() {
    python -c "import $1" 2>/dev/null
}

# Function to run validation test
run_validation() {
    local test_name="$1"
    local command="$2"
    local description="$3"
    
    echo -n "  ✓ $description... "
    
    if eval "$command" >/dev/null 2>&1; then
        echo "✅ PASS"
        return 0
    else
        echo "❌ FAIL"
        return 1
    fi
}

echo ""
echo "🐍 Python Environment Validation:"

# Check Python version
run_validation "python_version" "python --version | grep -E 'Python 3\.(1[1-9]|[2-9][0-9])'" "Python 3.11+ installed"

# Check virtual environment
run_validation "virtual_env" "test -d venv" "Virtual environment exists"

# Check if we're in virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "  ✓ Virtual environment activated... ✅ PASS"
else
    echo "  ⚠️  Virtual environment not activated (run: source venv/bin/activate)"
fi

echo ""
echo "📦 Critical Python Packages Validation:"

# Core packages for Sims 4 AI Assistant
packages=(
    "fastapi" "FastAPI framework"
    "uvicorn" "ASGI server"
    "pydantic" "Data validation"
    "sqlalchemy" "Database ORM"
    "sounddevice" "Audio capture"
    "PIL" "Image processing"
    "requests" "HTTP client"
    "aiohttp" "Async HTTP client"
    "httpx" "Modern HTTP client"
    "pytest" "Testing framework"
    "responses" "HTTP mocking"
    "faker" "Test data generation"
)

failed_packages=0
for ((i=0; i<${#packages[@]}; i+=2)); do
    package="${packages[i]}"
    description="${packages[i+1]}"
    
    if ! run_validation "package_$package" "python_package_exists $package" "$description ($package)"; then
        ((failed_packages++))
    fi
done

echo ""
echo "🔧 Development Tools Validation:"

# Development tools
dev_tools=(
    "black" "Code formatter"
    "isort" "Import sorter"
    "flake8" "Linter"
    "mypy" "Type checker"
    "bandit" "Security scanner"
)

failed_tools=0
for ((i=0; i<${#dev_tools[@]}; i+=2)); do
    tool="${dev_tools[i]}"
    description="${dev_tools[i+1]}"
    
    if ! run_validation "tool_$tool" "python_package_exists $tool" "$description ($tool)"; then
        ((failed_tools++))
    fi
done

echo ""
echo "📁 Client-Server Project Structure Validation:"

# Check directory structure
directories=(
    "server/src" "Server source directory"
    "server/src/api" "API directory"
    "server/src/core" "Core business logic"
    "server/src/models" "Database models"
    "server/src/services" "Business services"
    "client/src" "Client source directory"
    "client/src/ui" "UI components"
    "shared" "Shared utilities"
    "tests/unit" "Unit tests"
    "tests/integration" "Integration tests"
    "tests/mocks" "Mock implementations"
    "config" "Configuration directory"
)

failed_dirs=0
for ((i=0; i<${#directories[@]}; i+=2)); do
    dir="${directories[i]}"
    description="${directories[i+1]}"
    
    if ! run_validation "dir_$dir" "test -d $dir" "$description"; then
        ((failed_dirs++))
    fi
done

echo ""
echo "📄 Configuration Files Validation:"

# Check configuration files
files=(
    "AGENTS.md" "Agent guidelines file"
    "requirements.txt" "Python requirements"
    "pyproject.toml" "Tool configuration"
    ".gitignore" "Git ignore file"
    ".env.example" "Environment template"
    ".pre-commit-config.yaml" "Pre-commit config"
)

failed_files=0
for ((i=0; i<${#files[@]}; i+=2)); do
    file="${files[i]}"
    description="${files[i+1]}"
    
    if ! run_validation "file_$file" "test -f $file" "$description"; then
        ((failed_files++))
    fi
done

echo ""
echo "🧪 Testing Framework Validation:"

# Run sample tests
if run_validation "sample_tests" "python -m pytest tests/test_environment.py -v" "Environment tests run successfully"; then
    test_status="✅ PASS"
else
    test_status="❌ FAIL"
    ((failed_tests++))
fi

echo ""
echo "🔊 Audio System Validation:"

# Check audio system
if python -c "import sounddevice as sd; devices = sd.query_devices(); assert len(devices) > 0" 2>/dev/null; then
    echo "  ✓ Audio system available... ✅ PASS"
    python -c "import sounddevice as sd; devices = sd.query_devices(); print(f'  📊 Found {len(devices)} audio devices')"
else
    echo "  ⚠️  Audio system not available or no devices found"
fi

echo ""
echo "📸 Screenshot System Validation:"

# Check screenshot capability
if python -c "from PIL import ImageGrab; img = ImageGrab.grab(); print(f'Screenshot size: {img.size}')" 2>/dev/null; then
    echo "  ✓ Screenshot system available... ✅ PASS"
else
    echo "  ⚠️  Screenshot system not available (may be normal on headless systems)"
fi

echo ""
echo "🗄️ Database System Validation:"

# Check SQLite
if run_validation "sqlite_system" "python -c 'import sqlite3; conn = sqlite3.connect(\":memory:\"); conn.close()'" "SQLite system working"; then
    db_status="✅ PASS"
else
    db_status="❌ FAIL"
fi

echo ""
echo "🎭 Mock System Validation:"

# Check mocking capabilities
if python -c "import responses, faker; from unittest.mock import Mock, patch; print('Mock system ready')" 2>/dev/null; then
    echo "  ✓ Mock system available... ✅ PASS"
else
    echo "  ❌ Mock system not available"
fi

echo ""
echo "🔧 Development Tools Validation:"

# Check if pre-commit is configured
if test -f ".pre-commit-config.yaml"; then
    echo "  ✓ Pre-commit configuration exists... ✅ PASS"
    
    # Try to run pre-commit (if installed)
    if command_exists pre-commit; then
        if run_validation "pre_commit" "pre-commit run --all-files" "Pre-commit hooks run successfully"; then
            precommit_status="✅ PASS"
        else
            precommit_status="⚠️  WARN"
        fi
    else
        echo "  ⚠️  Pre-commit not installed (will be available after setup.sh)"
    fi
else
    echo "  ❌ Pre-commit configuration missing"
fi

echo ""
echo "🎮 Sims 4 AI Assistant Specific Validation:"

# Check environment variables template
if grep -q "SIMS4_INSTALL_PATH" .env.example 2>/dev/null; then
    echo "  ✓ Sims 4 specific environment variables... ✅ PASS"
else
    echo "  ⚠️  Sims 4 environment variables not found in .env.example"
fi

# Check for gaming-specific directories in gitignore
if grep -q "screenshots/" .gitignore && grep -q "recordings/" .gitignore 2>/dev/null; then
    echo "  ✓ Gaming-specific ignore patterns... ✅ PASS"
else
    echo "  ⚠️  Gaming-specific directories not in .gitignore"
fi

echo ""
echo "📊 Validation Summary:"
echo "===================="

total_checks=$((${#packages[@]}/2 + ${#dev_tools[@]}/2 + ${#directories[@]}/2 + ${#files[@]}/2 + 5))
failed_checks=$((failed_packages + failed_tools + failed_dirs + failed_files))

if [[ $failed_checks -eq 0 ]]; then
    echo "🎉 All validation checks passed! ($total_checks/$total_checks)"
    echo ""
    echo "✅ Your Sims 4 AI Gaming Assistant development environment is ready!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Activate virtual environment: source venv/bin/activate"
    echo "2. Read AGENTS.md for development workflow"
    echo "3. Start the server: make server"
    echo "4. Start coding with AI assistance for Sims 4!"
    echo ""
    echo "🎮 Gaming-specific features ready:"
    echo "- Voice recording system"
    echo "- Screenshot capture system"
    echo "- LLM integration (mocked for offline development)"
    echo "- Client-server architecture"
    
    exit 0
else
    echo "⚠️  Some validation checks failed: $((total_checks - failed_checks))/$total_checks passed"
    echo ""
    echo "Issues found:"
    echo "- $failed_packages critical package(s) missing"
    echo "- $failed_tools development tool(s) missing"
    echo "- $failed_dirs directory(ies) missing" 
    echo "- $failed_files configuration file(s) missing"
    echo ""
    echo "💡 Try running './setup.sh' to fix these issues"
    echo "   Note: Some audio/visual features may require system-level packages"
    
    exit 1
fi 