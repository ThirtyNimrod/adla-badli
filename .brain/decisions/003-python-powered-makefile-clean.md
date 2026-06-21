---
type: decision
date: 2026-06-22
title: Use Python inline commands for Makefile targets to ensure cross-platform compatibility
tags: [makefile, python, windows, linux]
shareable: true
---

# Use Python inline commands for Makefile targets to ensure cross-platform compatibility

## Context

We needed a unified, cross-platform `Makefile` to simplify development and testing commands (`install`, `serve`, `test`, `lint`, `e2e`, `clean`). The system needs to run on both Windows (Command Prompt, PowerShell, Git Bash) and Unix-like environments (Linux, macOS). The main challenge was implementing a shell-agnostic `clean` target; shell-specific deletion commands (like `rm -rf` vs `rmdir /s /q`) behave differently depending on the operating system and active shell, resulting in frequent errors.

## Options considered

**Option A — Shell detection and conditional execution**
Write conditional Makefile code to detect the shell/OS and branch to specific native commands:
- *Tradeoff:* Extremely verbose, hard to maintain, and prone to failures on Windows machines with custom bash/sh installations (like Git Bash) where OS returns `Windows_NT` but the shell expects Unix syntax.

**Option B — Python inline commands for OS operations**
Call Python's built-in libraries (`shutil`, `os`, `glob`) directly inside Makefile targets:
- *Tradeoff:* Requires Python to be installed and active (which is already a prerequisite for this FastAPI repository), but provides 100% shell-agnostic, reliable file/folder manipulation.

## Decision

Chose **Option B** because the project is already a Python-centric codebase, meaning Python's presence is guaranteed. Running inline Python scripts for file management inside the Makefile ensures cross-platform reliability without shell detection scripts.

## Tradeoffs accepted

- Makefile commands are slightly longer due to inline Python syntax (e.g. `python -c "..."`).
- Deletions are executed inside a Python process, adding a negligible startup overhead.

## Outcome

Successfully unified Makefile clean targets to a single command that runs cleanly in both PowerShell on Windows and standard bash on Unix environments without script execution policies blocks.
