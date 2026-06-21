---
type: decision
date: 2026-06-09
title: Pydantic-based dynamic options schemas for format converters
tags: [fastapi, python, pydantic, javascript, architecture]
shareable: true
---

# Pydantic-based dynamic options schemas for format converters

## Context

Different converters require different conversion options (e.g., SVG-to-JPG requires background colors, while Markdown-to-DOCX does not). In our original implementation, the options were hardcoded as explicit parameters in both the FastAPI route parameters and the client-side JavaScript. This meant that introducing new converter options or formats required modifying three separate layers: the converter class, the HTTP controller, and the frontend JS code.

## Options considered

**Option A — Declarative Option Schemas using custom dictionary definitions**
Each converter class exposes a custom dictionary detailing option names, enums, enforcements, and default values. 
* *Tradeoff:* Requires building a custom type validator, parser, and schema exporter, which introduces home-grown validation complexity.

**Option B — Class-Bound Pydantic Models**
Each converter associates a `pydantic.BaseModel` subclass directly with the converter class representation. The registry serializes the options schema to JSON Schema via Pydantic's `model_json_schema()`, and the endpoint executes runtime type coercion and validation via `model_validate()`.
* *Tradeoff:* Extremely powerful. Inherits standard JSON Schema generation, automatic validation, type coercion, and enums out-of-the-box, but depends heavily on the Pydantic library ecosystem.

## Decision

Chose **Option B** (Class-Bound Pydantic Models) because it maximizes **depth** and **leverage**. Because Pydantic is already a transitive dependency of FastAPI, utilizing it directly allows us to leverage complex validations and automatic serialization without writing custom parser code.

## Tradeoffs accepted

- The frontend JavaScript must parse JSON Schema formats dynamically to render inputs. If a converter defines highly customized or layout-dependent options, the generic JSON Schema form generator will require extensions.

## Outcome

Successfully implemented. Adding or modifying converter options now requires updating only the target converter class file; the rest of the application adapts dynamically without code modifications.
