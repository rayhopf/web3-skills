---
description: Quick git commit with AI-generated message
allowed-tools: Bash(git *:*)
---

Create a git commit following these steps:

1. Check current changes with `git status` and `git diff`
2. Review recent commit style with `git log -5 --oneline`
3. Draft a concise commit message using conventional commit format (feat:, fix:, docs:, etc.)
4. Stage all changes with `git add .`
5. Commit using HEREDOC format, ending with: "Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
6. Verify with `git status`

Important: Never commit sensitive files (.env, credentials.json). Don't push unless explicitly requested.
