---
type: concept
date: 2026-06-09
title: Dynamic Form Generation via JSON Schema
tags: [javascript, json-schema, pydantic, api-design]
shareable: true
related_docs: "https://json-schema.org/"
---

# Dynamic Form Generation via JSON Schema

## The confusion

I thought each input field in a web application had to be hardcoded in HTML and parsed explicitly in JavaScript. I assumed that adding a new options configuration to a backend service required manually duplicating the validation rules on the frontend (e.g. writing selection options in HTML and input checks in JS).

## The mental model

Instead of hardcoding inputs, treat form layout as a function of data schema. The backend is the single source of truth for configuration structures. By publishing these structures as standard JSON Schemas, the frontend client can dynamically generate form input controls (e.g., matching enums to dropdown select lists, booleans to checkbox elements, and numbers to numeric fields) in the DOM, maintaining strict consistency automatically.

## The precise version

Standard JSON Schema represents objects, properties, types, enums, enums enforcements, and default values. 
When the frontend fetches schemas:
1. It inspects the `properties` collection.
2. For each property:
   - If `enum` is defined, it renders a `<select>` dropdown.
   - If `type` is `"boolean"`, it renders a `<input type="checkbox">`.
   - If `type` is `"integer"` or `"number"`, it renders a `<input type="number">`.
   - Otherwise, it falls back to a `<input type="text">`.
3. It sets default values using the `default` field.
4. During form submission, the code queries all active dynamic inputs and serializes them to form data dynamically.

## Code example

```javascript
// Render form from JSON Schema
function renderForm(properties, container) {
  container.innerHTML = "";
  Object.entries(properties).forEach(([name, prop]) => {
    const input = document.createElement(prop.enum ? "select" : "input");
    input.name = name;
    if (prop.enum) {
      prop.enum.forEach(val => input.appendChild(new Option(val, val)));
    } else {
      input.type = prop.type === "boolean" ? "checkbox" : "text";
      input.value = prop.default || "";
    }
    container.appendChild(input);
  });
}
```

## Why it matters

Failing to dynamically generate forms leads to duplicated configuration schemas across backend models, routing layers, and frontend templates, significantly increasing maintenance overhead and causing silent breakages when definitions drift.
