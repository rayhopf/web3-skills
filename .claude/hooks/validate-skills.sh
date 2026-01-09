#!/usr/bin/env bash
# Post-write hook to validate skills after changes

# Enable async processing and set timeout
echo '{"async":true,"asyncTimeout":30000}'

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to project root
cd "$PROJECT_ROOT" || exit 1

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "⚠️  Warning: Virtual environment not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements-dev.txt"
    exit 0
fi

# Check if skills-ref is installed
if ! command -v skills-ref &> /dev/null; then
    echo "⚠️  Warning: skills-ref not installed. Run: pip install -r requirements-dev.txt"
    exit 0
fi

# Find all skill directories
SKILLS_DIRS=$(find skills -maxdepth 1 -mindepth 1 -type d 2>/dev/null)

if [ -z "$SKILLS_DIRS" ]; then
    echo "ℹ️  No skills found in skills/ directory"
    exit 0
fi

# Validate each skill
echo "🔍 Validating skills..."
HAS_ERRORS=0

while IFS= read -r skill_dir; do
    if [ -d "$skill_dir" ]; then
        # Run validation
        if skills-ref validate "$skill_dir" 2>&1; then
            echo "✅ $skill_dir"
        else
            echo "❌ $skill_dir: Validation failed"
            HAS_ERRORS=1
        fi
    fi
done <<< "$SKILLS_DIRS"

if [ $HAS_ERRORS -eq 0 ]; then
    echo "✅ All skills validated successfully"
else
    echo "⚠️  Some skills have validation errors"
fi
