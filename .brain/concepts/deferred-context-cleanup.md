---
type: concept
date: 2026-06-09
title: Deferred Context Manager Cleanup Handshake
tags: [python, fastapi, architecture, state-management]
shareable: true
---

# Deferred Context Manager Cleanup Handshake

## The confusion

I assumed context managers (`with` blocks in Python) had to clean up their resources immediately upon exiting the block scope. I thought it was impossible to use a context manager if a resource (like a temporary file) needed to survive the block scope to be returned asynchronously by a web server response.

## The mental model

A context manager is just an object that runs logic on entry (`__enter__`) and exit (`__exit__`). We can explicitly model a "resource release" state. If the caller calls `.release()` inside the block, it sets an internal boolean. On exit, the context manager checks this flag and skips unlinking. The controller can then safely hand over the cleanup task callback (via `.get_cleanup_task()`) to the framework's background task runner. Under errors/exceptions, the release flag remains false, ensuring automatic cleanup.

## The precise version

In Python:
1. `__init__` sets `self._released = False`.
2. `__exit__` only deletes the workspace folder if `not self._released`.
3. The controller accesses workspace paths inside the context. If everything succeeds, it extracts a cleanup callback `task = workspace.get_cleanup_task()`, registers it in FastAPI's `BackgroundTasks`, and calls `workspace.release()`.
4. Upon exit, the folder survives. Once the file finishes streaming to the client browser, FastAPI's runner executes the background task, purging the directory safely.

## Code example

```python
class ConversionWorkspace:
    def __enter__(self):
        # Create resources...
        return self
        
    def release(self):
        self._released = True
        
    def get_cleanup_task(self):
        return lambda: shutil.rmtree(self.workspace_dir)
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._released:
            shutil.rmtree(self.workspace_dir)
```

## Why it matters

Without a deferred cleanup handshake, context managers cannot be used for asynchronous web server responses, forcing authors to write verbose manual resource management code in every controller route.
