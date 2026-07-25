from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Any

import pydantic
from ollama import Tool

from src.app.common.utils.func_name_getter import get_func_name


@dataclass(slots=True, frozen=True)
class RegisteredTool:
    tool: Tool


class ToolRegistry:
    def __init__(self, base_dir: PathLike[str] | str) -> None:
        self._base_dir = Path(base_dir)
        self._tools: dict[str, RegisteredTool] = {}

    def register(
        self,
        file_path: str,
        func: Callable[..., Any],
    ) -> None:
        """Регистрирует инструмент."""
        name = get_func_name(func)

        description = self._load_description(file_path)

        schema = self._build_parameters_schema(
            model_name=name,
            func=func,
        )

        tool = self._build_tool(
            name=name,
            description=description,
            parameters_schema=schema,
        )

        self._tools[name] = RegisteredTool(
            tool=tool,
        )

    def get(self, name: str) -> Tool:
        """Возвращает описание инструмента для Ollama."""
        return self._get_registered(name).tool

    def get_all(self) -> list[Tool]:
        """Возвращает все зарегистрированные инструменты."""
        return [registered_tool.tool for registered_tool in self._tools.values()]

    def _get_registered(self, name: str) -> RegisteredTool:
        tool = self._tools.get(name)

        if tool is None:
            raise ValueError(f"Tool '{name}' is not registered.")

        return tool

    def _load_description(self, file_path: str) -> str:
        return (self._base_dir / file_path).read_text(encoding="utf-8")

    def _build_parameters_schema(
        self,
        model_name: str,
        func: Callable[..., Any],
    ) -> dict[str, Any]:
        fields = self._build_model_fields(func)

        try:
            model = pydantic.create_model(
                model_name,
                **fields,
            )
        except Exception as exc:
            raise ValueError(f"Cannot generate schema for tool '{model_name}'") from exc

        schema = model.model_json_schema()

        schema.pop("title", None)

        return schema

    def _build_model_fields(
        self,
        func: Callable[..., Any],
    ) -> dict[str, Any]:
        signature = inspect.signature(func)

        fields: dict[str, Any] = {}

        for parameter in signature.parameters.values():
            if parameter.name in {"self", "cls"}:
                continue

            annotation = self._resolve_annotation(parameter)
            default = self._resolve_default(parameter)

            fields[parameter.name] = (
                annotation,
                default,
            )

        return fields

    @staticmethod
    def _resolve_annotation(
        parameter: inspect.Parameter,
    ) -> Any:
        if parameter.annotation is inspect.Signature.empty:
            return str

        return parameter.annotation

    @staticmethod
    def _resolve_default(
        parameter: inspect.Parameter,
    ) -> Any:
        if parameter.default is inspect.Signature.empty:
            return ...

        return parameter.default

    @staticmethod
    def _build_tool(
        *,
        name: str,
        description: str,
        parameters_schema: dict[str, Any],
    ) -> Tool:
        return Tool(
            type="function",
            function=Tool.Function(
                name=name,
                description=description,
                parameters=Tool.Function.Parameters(
                    **parameters_schema,
                ),
            ),
        )
