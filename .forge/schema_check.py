#!/usr/bin/env python3
"""Small Draft 2020-12 subset used by Forge runtime contracts.

The supported keywords match the schemas shipped in ``.forge/schemas``. Unknown
schema features fail closed so adding a keyword requires adding its runtime
implementation and tests in the same change.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
SUPPORTED = {
    "$schema", "$id", "$defs", "$ref", "title", "description", "type",
    "additionalProperties", "required", "properties", "items", "minItems",
    "uniqueItems", "minLength", "maxLength", "pattern", "format", "minimum",
    "maximum", "exclusiveMinimum", "exclusiveMaximum", "const", "enum",
    "allOf", "if", "then", "else", "not",
}


class SchemaFailure(ValueError):
    """Raised when an instance or the schema itself is unsupported."""


def load_schema(name: str) -> dict[str, Any]:
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def _resolve(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not isinstance(ref, str) or not ref.startswith("#/"):
        raise SchemaFailure(f"unsupported reference: {ref}")
    node: Any = root
    for part in ref[2:].split("/"):
        if not isinstance(node, dict) or part not in node:
            raise SchemaFailure(f"unresolved reference: {ref}")
        node = node[part]
    if not isinstance(node, dict):
        raise SchemaFailure(f"reference is not a schema: {ref}")
    return node


def _check_keywords(schema: dict[str, Any], path: str) -> None:
    unknown = set(schema) - SUPPORTED
    if unknown:
        raise SchemaFailure(f"{path}: unsupported schema keywords {sorted(unknown)}")


def _preflight(schema: dict[str, Any], path: str = "$schema") -> None:
    """Reject unsupported syntax everywhere, including branches not used by an instance."""
    if not isinstance(schema, dict):
        raise SchemaFailure(f"{path}: schema must be an object")
    _check_keywords(schema, path)
    for field in ("$defs", "properties"):
        children = schema.get(field, {})
        if not isinstance(children, dict):
            raise SchemaFailure(f"{path}.{field}: must be an object")
        for name, child in children.items():
            _preflight(child, f"{path}.{field}.{name}")
    for field in ("items", "if", "then", "else", "not"):
        if field in schema:
            _preflight(schema[field], f"{path}.{field}")
    branches = schema.get("allOf", [])
    if not isinstance(branches, list):
        raise SchemaFailure(f"{path}.allOf: must be an array")
    for index, child in enumerate(branches):
        _preflight(child, f"{path}.allOf[{index}]")


def validate(instance: Any, schema: dict[str, Any], root: dict[str, Any] | None = None,
             path: str = "$") -> None:
    if root is None:
        _preflight(schema)
        root = schema
    schema = _resolve(schema, root)
    _check_keywords(schema, path)

    for branch in schema.get("allOf", []):
        validate(instance, branch, root, path)
    if "if" in schema:
        try:
            validate(instance, schema["if"], root, path)
            matched = True
        except SchemaFailure:
            matched = False
        branch = schema.get("then") if matched else schema.get("else")
        if branch is not None:
            validate(instance, branch, root, path)
    if "not" in schema:
        try:
            validate(instance, schema["not"], root, path)
        except SchemaFailure:
            pass
        else:
            raise SchemaFailure(f"{path}: matched forbidden schema")
    if "const" in schema and instance != schema["const"]:
        raise SchemaFailure(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        raise SchemaFailure(f"{path}: unsupported value {instance!r}")

    expected = schema.get("type")
    if expected:
        kinds = [expected] if isinstance(expected, str) else expected
        checks = {
            "object": lambda value: isinstance(value, dict),
            "array": lambda value: isinstance(value, list),
            "string": lambda value: isinstance(value, str),
            "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
            "number": lambda value: isinstance(value, (int, float)) and not isinstance(value, bool),
            "boolean": lambda value: isinstance(value, bool),
            "null": lambda value: value is None,
        }
        unsupported_types = set(kinds) - set(checks)
        if unsupported_types:
            raise SchemaFailure(f"{path}: unsupported schema types {sorted(unsupported_types)}")
        if not any(checks[kind](instance) for kind in kinds):
            raise SchemaFailure(f"{path}: expected {kinds}")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = [key for key in required if key not in instance]
        if missing:
            raise SchemaFailure(f"{path}: missing {', '.join(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = set(instance) - set(properties)
            if extra:
                raise SchemaFailure(f"{path}: unknown fields {sorted(extra)}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], root, f"{path}.{key}")

    if isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise SchemaFailure(f"{path}: too few items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(value, sort_keys=True) for value in instance]
            if len(set(encoded)) != len(encoded):
                raise SchemaFailure(f"{path}: duplicate items")
        if "items" in schema:
            for index, value in enumerate(instance):
                validate(value, schema["items"], root, f"{path}[{index}]")

    if isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise SchemaFailure(f"{path}: string is too short")
        if len(instance) > schema.get("maxLength", len(instance)):
            raise SchemaFailure(f"{path}: string is too long")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], instance):
            raise SchemaFailure(f"{path}: pattern mismatch")
        if schema.get("format") == "date-time":
            try:
                datetime.fromisoformat(instance.replace("Z", "+00:00"))
            except ValueError as exc:
                raise SchemaFailure(f"{path}: invalid date-time") from exc

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            raise SchemaFailure(f"{path}: below minimum")
        if "maximum" in schema and instance > schema["maximum"]:
            raise SchemaFailure(f"{path}: above maximum")
        if "exclusiveMinimum" in schema and instance <= schema["exclusiveMinimum"]:
            raise SchemaFailure(f"{path}: below exclusive minimum")
        if "exclusiveMaximum" in schema and instance >= schema["exclusiveMaximum"]:
            raise SchemaFailure(f"{path}: above exclusive maximum")
