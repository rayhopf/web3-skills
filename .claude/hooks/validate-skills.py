#!/usr/bin/env python3
"""Hook to validate skills after file changes."""

import sys
import os
import subprocess
import re
import json
from datetime import datetime

def log_to_file(message):
    """Log a message to .cache/bash-command-log.txt"""
    os.makedirs('.cache', exist_ok=True)
    with open('.cache/bash-command-log.txt', 'a') as f:
        f.write(message + '\n')

def main():
    # Read JSON input from stdin
    input_data = sys.stdin.read().strip()

    # Log input
    log_to_file(f"\n=== {datetime.now()} - validate-skills.py ===")
    log_to_file(f"INPUT: {input_data}")

    # Parse JSON to extract file path
    try:
        data = json.loads(input_data)
        # Try tool_response.filePath first, then tool_input.file_path
        file_path = data.get('tool_response', {}).get('filePath') or data.get('tool_input', {}).get('file_path')
        cwd = data.get('cwd', '')

        # Convert absolute path to relative if needed
        if file_path and cwd and file_path.startswith(cwd):
            file_path = file_path[len(cwd):].lstrip('/')
    except (json.JSONDecodeError, AttributeError, KeyError):
        log_to_file("OUTPUT: Skipped (could not parse JSON)")
        log_to_file("---")
        sys.exit(0)

    # Exit if no file path or not in skills/ directory
    if not file_path or not file_path.startswith('skills/'):
        log_to_file(f"OUTPUT: Skipped (not in skills/) - file_path={file_path}")
        log_to_file("---")
        sys.exit(0)

    # Extract skill directory (e.g., "skills/dune" from "skills/dune/references/...")
    match = re.match(r'^skills/([^/]+)', file_path)
    if not match:
        log_to_file("OUTPUT: Skipped (could not extract skill dir)")
        log_to_file("---")
        sys.exit(0)

    skill_dir = f"skills/{match.group(1)}"

    # Get project root (2 levels up from .claude/hooks)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    os.chdir(project_root)

    # Check if skill directory exists
    if not os.path.isdir(skill_dir):
        log_to_file(f"OUTPUT: Skipped (skill dir {skill_dir} not found)")
        log_to_file("---")
        sys.exit(0)

    log_to_file(f"Validating {skill_dir}...")
    print(f"🔍 Validating {skill_dir}...", file=sys.stderr)

    # Run validation using skills-ref
    try:
        result = subprocess.run(
            ['.venv/bin/skills-ref', 'validate', skill_dir],
            capture_output=True,
            text=True,
            check=False
        )

        # Print output
        if result.stdout:
            log_to_file(f"STDOUT: {result.stdout}")
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            log_to_file(f"STDERR: {result.stderr}")
            print(result.stderr, file=sys.stderr)

        # Check result
        if result.returncode == 0:
            log_to_file(f"OUTPUT: ✅ {skill_dir} validated successfully")
            log_to_file("---")
            print(f"✅ {skill_dir} validated successfully", file=sys.stderr)
            sys.exit(0)
        else:
            log_to_file(f"OUTPUT: ❌ {skill_dir}: Validation failed (exit code {result.returncode})")
            log_to_file("---")
            print(f"❌ {skill_dir}: Validation failed", file=sys.stderr)
            sys.exit(2)

    except FileNotFoundError:
        log_to_file("OUTPUT: ⚠️ skills-ref not installed")
        log_to_file("---")
        print("⚠️  Warning: skills-ref not installed. Run: pip install -r requirements-dev.txt", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        log_to_file(f"OUTPUT: ⚠️ Error running validation: {e}")
        log_to_file("---")
        print(f"⚠️  Error running validation: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == '__main__':
    main()
