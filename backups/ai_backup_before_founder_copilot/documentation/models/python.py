from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PythonArgument:
    """
    Represents a Python function argument.
    """

    name: str

    annotation: str = ""

    default_value: str = ""

    kind: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class PythonFunction:
    """
    Represents a Python function or method.
    """

    name: str

    qualified_name: str = ""

    line_start: int = 0
    line_end: int = 0

    docstring: str = ""

    return_type: str = ""

    arguments: list[PythonArgument] = field(
        default_factory=list
    )

    decorators: list[str] = field(
        default_factory=list
    )

    is_async: bool = False

    is_method: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_argument(
        self,
        argument: PythonArgument
    ) -> None:
        self.arguments.append(argument)


@dataclass(slots=True)
class PythonClass:
    """
    Represents a Python class discovered by AST analysis.
    """

    name: str

    qualified_name: str = ""

    line_start: int = 0
    line_end: int = 0

    docstring: str = ""

    bases: list[str] = field(
        default_factory=list
    )

    decorators: list[str] = field(
        default_factory=list
    )

    methods: list[PythonFunction] = field(
        default_factory=list
    )

    attributes: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_method(
        self,
        method: PythonFunction
    ) -> None:
        self.methods.append(method)


@dataclass(slots=True)
class PythonModule:
    """
    Represents a Python module.
    """

    name: str

    path: str

    classes: list[PythonClass] = field(
        default_factory=list
    )

    functions: list[PythonFunction] = field(
        default_factory=list
    )

    imports: list[str] = field(
        default_factory=list
    )

    docstring: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def add_class(
        self,
        cls: PythonClass
    ) -> None:
        self.classes.append(cls)

    def add_function(
        self,
        function: PythonFunction
    ) -> None:
        self.functions.append(function)
