import functools
import inspect
import json
import re
from enum import Enum
from inspect import Parameter
from types import ModuleType
from typing import Callable, Optional

from tool2schema.parameter_schema import PARAMETER_SCHEMAS, EnumParameterSchema, ParameterSchema


class SchemaType(Enum):
    """Enum for schema types."""

    API = 0
    TUNE = 1


def FindGPTEnabled(module: ModuleType) -> list[Callable]:
    """
    Find all functions with the GPTEnabled decorator.

    :param module: Module to search for GPTEnabled functions
    """
    return [x for x in module.__dict__.values() if hasattr(x, "gpt_enabled")]


def FindGPTEnabledSchemas(
    module: ModuleType, schema_type: SchemaType = SchemaType.API
) -> list[dict]:
    """
    Find all function schemas with the GPTEnabled decorator.

    :param module: Module to search for GPTEnabled functions
    :param schema_type: Type of schema to return
    """
    return [x.schema.to_json(schema_type) for x in FindGPTEnabled(module)]


def FindGPTEnabledByName(module: ModuleType, name: str) -> Optional[Callable]:
    """
    Find a function with the GPTEnabled decorator by name.

    :param module: Module to search for GPTEnabled functions
    :param name: Name of the function to find
    """
    for func in FindGPTEnabled(module):
        if func.__name__ == name:
            return func
    return None


def FindGPTEnabledByTag(module: ModuleType, tag: str) -> list[Callable]:
    """
    Find all functions with the GPTEnabled decorator by tag.

    :param module: Module to search for GPTEnabled functions
    :param tag: Tag to search for
    """
    return [x for x in FindGPTEnabled(module) if x.has(tag)]


def SaveGPTEnabled(module: ModuleType, path: str, schema_type: SchemaType = SchemaType.API):
    """
    Save all function schemas with the GPTEnabled decorator to a file.

    :param module: Module to search for GPTEnabled functions
    :param path: Path to save the schemas to
    :param schema_type: Type of schema to return
    """
    schemas = FindGPTEnabledSchemas(module, schema_type)
    json.dump(schemas, open(path, "w"))


class _GPTEnabled:
    def __init__(self, func, **kwargs) -> None:
        self.func = func
        self.schema = FunctionSchema(func)
        self.tags = kwargs.get("tags", [])
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):

        args = list(args)  # Tuple is immutable, thus convert to list

        for i, arg in enumerate(args):
            for p in self.schema.parameter_schemas.values():
                if p.index == i:
                    # Convert the JSON value to the type expected by the method
                    args[i] = p.parse_value(arg)

        for key in kwargs:
            if key in self.schema.parameter_schemas:
                # Convert the JSON value to the type expected by the method
                kwargs[key] = self.schema.parameter_schemas[key].parse_value(kwargs[key])

        return self.func(*args, **kwargs)

    def gpt_enabled(self) -> bool:
        return True

    def has(self, tag: str) -> bool:
        return tag in self.tags


def GPTEnabled(func=None, **kwargs):
    """Decorator to generate a function schema for OpenAI."""
    if func:
        return _GPTEnabled(func, **kwargs)
    else:

        def wrapper(function):
            return _GPTEnabled(function, **kwargs)

        return wrapper


class FunctionSchema:
    """Automatically create a function schema for OpenAI."""

    def __init__(self, f: Callable):
        """
        Initialize FunctionSchema for the given function.

        :param f: The function to create a schema for;
        """
        self.f = f
        self.parameter_schemas: dict[str, ParameterSchema] = self._get_parameter_schemas()

    def to_json(self, schema_type: SchemaType = SchemaType.API) -> dict:
        """
        Convert schema to JSON.
        :param schema_type: Type of schema to return
        """
        if schema_type == SchemaType.TUNE:
            return self._get_function_schema(schema_type)

        return self._get_schema()

    def add_enum(self, n: str, enum: list) -> "FunctionSchema":
        """
        Add enum property to a particular function parameter.

        :param n: The name of the parameter with the enum values
        :param enum: The list of values for the enum parameter
        """
        p = self.parameter_schemas[n]
        self.parameter_schemas[n] = EnumParameterSchema(enum, p.parameter, p.index, p.docstring)
        return self

    def _get_schema(self) -> dict:
        """
        Get the complete schema dictionary.
        """
        # This dictionary is only used with the API schema type
        return {"type": "function", "function": self._get_function_schema(SchemaType.API)}

    def _get_function_schema(self, schema_type: SchemaType) -> dict:
        """
        Get the function schema dictionary.
        """
        schema = {"name": self.f.__name__}

        if self.parameter_schemas or schema_type == SchemaType.TUNE:
            # If the schema type is tune, add the dictionary even if there are no parameters
            schema["parameters"] = self._get_parameters_schema(schema_type)

        if (description := self._get_description()) is not None:
            # Add the function description even if it is an empty string
            schema["description"] = description

        return schema

    def _get_parameters_schema(self, schema_type: SchemaType) -> dict:
        """
        Get the parameters schema dictionary.
        """
        schema = {"type": "object"}

        if self.parameter_schemas or schema_type == SchemaType.TUNE:
            # If the schema type is tune, add the dictionary even if empty
            schema["properties"] = self._get_parameter_properties_schema()

            if required := self._get_required_parameters():
                schema["required"] = required

        return schema

    def _get_parameter_properties_schema(self) -> dict:
        """
        Get the properties schema for the function.
        """
        schema = dict()

        for n, p in self.parameter_schemas.items():
            schema[n] = p.to_json()

        return schema

    def _get_parameter_schemas(self) -> dict[str, ParameterSchema]:
        """
        Get a dictionary of parameter schemas for the function.
        Ignored parameters are not included in the dictionary.

        :return: A dictionary with parameter names as keys and
            parameter schemas as values
        """
        parameters = dict()

        for i, (n, o) in enumerate(inspect.signature(self.f).parameters.items()):
            if n == "kwargs":
                continue  # Skip kwargs

            for Param in PARAMETER_SCHEMAS:
                if Param.matches(o):
                    parameters[n] = Param(o, i, self.f.__doc__)
                    break

        return parameters

    def _get_description(self) -> Optional[str]:
        """
        Extract the function description, if present.

        :return: The function description, or None if not present
        """
        if docstring := self.f.__doc__:  # Check if docstring exists
            docstring = " ".join([x.strip() for x in docstring.replace("\n", " ").split()])
            if desc := re.findall(r"(.*?):param", docstring):
                return desc[0].strip()

            return docstring.strip()

        return None

    def _get_required_parameters(self) -> list[str]:
        """
        Get the list of required parameters.

        :return: The list of parameters without a default value
        """
        req_params = []
        for n, p in self.parameter_schemas.items():
            if p.parameter.default == Parameter.empty:
                req_params.append(n)

        return req_params
