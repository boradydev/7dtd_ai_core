# get_tools_json

## Purpose

Return a JSON document containing all available tools for the requested category.

## Use when

- The user asks which tools belong to a category.
- The user wants to list available tools.
- The user requests all tools from a specific category.

## Never use when

- The user asks for information about a single tool.
- The user asks how to use a tool.
- The user asks for recommendations.

## Parameters

The category must be one of the supported values.

## Returns

A JSON object containing a single field named `tools`.

The `tools` field is an array of tool names.

## Examples

User:

> Show all mining tools.

Tool:

```text
get_tools_json(
    category="mining"
)
```

---

User:

> List woodworking tools.

Tool:

```text
get_tools_json(
    category="woodcutting"
)
```

## Important

Always use one of the allowed category values defined by the tool schema.

Never invent new category names.