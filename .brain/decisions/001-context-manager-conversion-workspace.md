---
type: decision
date: 2026-06-09
title: Context Manager based Conversion Workspace with Deferred Cleanup Handoff
tags: [fastapi, python, architecture, testing]
shareable: true
---

# Context Manager based Conversion Workspace with Deferred Cleanup Handoff

## Context

In our file conversion web service, each file upload requires creating temporary input files, executing the conversion, generating output files, streaming them back to the client, and unlinking them afterwards. 
If conversion fails, or if the client disconnects, we must ensure these files are safely cleaned up to prevent disk bloat. 
However, since FastAPI streams files asynchronously after the request handler exits, immediate cleanup inside a standard context manager would delete the output file before it is sent.

## Options considered

**Option A — Manual Controller-Managed Cleanup**
Inject path generation and unlinking logic directly into the controller routes, catching exceptions and using `BackgroundTasks` to trigger unlinking. 
* *Tradeoff:* Leaks filesystem details into the HTTP transport layer, creates repetitive error-handling boilerplate, and makes mock testing hard.

**Option B — Context Manager with Deferred Handoff**
Create a context manager wrapper (`ConversionWorkspace`) that generates a sandboxed folder. If execution fails, it unlinks everything. If successful, the controller calls `.release()` to prevent exit-time deletion, and registers `.get_cleanup_task()` as a background task.
* *Tradeoff:* Extremely clean controller logic. Guarantees safety under errors, isolates file operations, but adds slight complexity via the release handshake.

## Decision

Chose **Option B** (Context Manager with Deferred Handoff) because it maximizes **locality** and safety. The filesystem details reside entirely inside the workspace module. 

## Tradeoffs accepted

- The controller must remember to call `workspace.release()` and register `get_cleanup_task()`. Failing to do so causes the context exit to delete the file before the response is finished, breaking downloads.

## Outcome

The design held up perfectly. Workspace unit tests validated that errors trigger immediate cleanup, while normal flows hand over file deletion successfully.
