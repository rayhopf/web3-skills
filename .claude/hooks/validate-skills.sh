#!/usr/bin/env bash
# Hook to extract file path if it's in skills/ directory

# Create log directory if it doesn't exist
mkdir -p .cache

# Read stdin JSON
INPUT=$(cat)

# Log input
{
    echo ""
    echo "=== $(date) - validate-skills.sh ==="
    echo "INPUT:"
    echo "$INPUT" | head -c 500
    echo ""
} >> .cache/bash-command-log.txt

# Extract file path and current working directory
FILE=$(echo "$INPUT" | jq -r '.tool_response.filePath // .tool_input.file_path // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Convert absolute path to relative path if needed
if [ -n "$CWD" ] && [[ "$FILE" == "$CWD"* ]]; then
    # Remove CWD prefix and leading slash
    FILE="${FILE#$CWD}"
    FILE="${FILE#/}"
fi

# Log output
{
    echo "OUTPUT:"
    echo "$FILE"
    echo "---"
} >> .cache/bash-command-log.txt

# Only proceed if file is in skills/ directory
if [ -n "$FILE" ] && [[ "$FILE" =~ ^skills/ ]]; then
    echo "$FILE"
fi

exit 0
