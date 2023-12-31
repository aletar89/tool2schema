from typing import Optional, List
from gpt2schema import GPTEnabled

###########################################
#  Example function to test with no tags  #
###########################################

@GPTEnabled
def function(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function.schema.to_json() == expected_schema
    assert function.tags == []

########################################
#  Example function to test with tags  #
########################################

@GPTEnabled(tags=["test"])
def function_tags(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function_tags():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_tags",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_tags.schema.to_json() == expected_schema
    assert function_tags.tags == ["test"]

########################################
#  Example function to test with enum  #
########################################

@GPTEnabled
def function_enum(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d
function_enum.schema.add_enum("a", [1, 2, 3])


def test_function_enum():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_enum",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                        "enum": [1, 2, 3],
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_enum.schema.to_json() == expected_schema
    assert function_enum.tags == []

#########################################
#  Example function with no parameters  #
#########################################

@GPTEnabled
def function_no_params():
    """
    This is a test function.
    """
    return


def test_function_no_params():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_no_params",
            "description": "This is a test function.",
        },
    }
    assert function_no_params.schema.to_json() == expected_schema
    assert function_no_params.tags == []

##########################################
#  Example function with no description  #
##########################################

@GPTEnabled
def function_no_description(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function_no_description():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_no_description",
            "description": "",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_no_description.schema.to_json() == expected_schema
    assert function_no_description.tags == []

###################################################
#  Example function with no parameter docstrings  #
###################################################

@GPTEnabled
def function_no_param_docstrings(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    This is a test function.
    """
    return a, b, c, d


def test_function_no_param_docstrings():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_no_param_docstrings",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                    },
                    "b": {
                        "type": "string",
                    },
                    "c": {
                        "type": "boolean",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_no_param_docstrings.schema.to_json() == expected_schema
    assert function_no_param_docstrings.tags == []

#####################################################
#  Example function with no parameter descriptions  #
#####################################################

@GPTEnabled
def function_no_param_descriptions(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    """
    This is a test function.

    :param a:
    :param b:
    :param c:
    :param d:
    """
    return a, b, c, d


def test_function_no_param_descriptions():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_no_param_descriptions",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                    },
                    "b": {
                        "type": "string",
                    },
                    "c": {
                        "type": "boolean",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_no_param_descriptions.schema.to_json() == expected_schema
    assert function_no_param_descriptions.tags == []

########################################
#  Example function with no docstring  #
########################################

@GPTEnabled
def function_no_docstring(a: int, b: str, c: bool = False, d: list[int] = [1, 2, 3]):
    return a, b, c, d


def test_function_no_docstring():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_no_docstring",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                    },
                    "b": {
                        "type": "string",
                    },
                    "c": {
                        "type": "boolean",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_no_docstring.schema.to_json() == expected_schema
    assert function_no_docstring.tags == []

#######################################################
#  Example function with list annotation but no type  #
#######################################################

@GPTEnabled
def function_list_no_type(a: int, b: str, c: bool = False, d: list = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function_list_no_type():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_list_no_type",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_list_no_type.schema.to_json() == expected_schema
    assert function_list_no_type.tags == []

####################################################
#  Example function with Optional type annotation  #
####################################################

@GPTEnabled
def function_optional(a: int, b: str, c: bool = False, d: Optional[int] = None):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is an optional parameter;
    """
    return a, b, c, d


def test_function_optional():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_optional",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "integer",
                        "description": "This is an optional parameter",
                        "default": None,
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_optional.schema.to_json() == expected_schema
    assert function_optional.tags == []

##################################################
#  Example function with typing.List annotation  #
##################################################

@GPTEnabled
def function_typing_list(a: int, b: str, c: bool = False, d: List[int] = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function_typing_list():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_typing_list",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "items": {
                            "type": "integer",
                        },
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_typing_list.schema.to_json() == expected_schema
    assert function_typing_list.tags == []

##############################################################
#  Example function with typing.List annotation but no type  #
##############################################################

@GPTEnabled
def function_typing_list_no_type(a: int, b: str, c: bool = False, d: List = [1, 2, 3]):
    """
    This is a test function.

    :param a: This is a parameter;
    :param b: This is another parameter;
    :param c: This is a boolean parameter;
    :param d: This is a list parameter;
    """
    return a, b, c, d


def test_function_typing_list_no_type():
    # Check schema
    expected_schema = {
        "type": "function",
        "function": {
            "name": "function_typing_list_no_type",
            "description": "This is a test function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "This is a parameter",
                    },
                    "b": {
                        "type": "string",
                        "description": "This is another parameter",
                    },
                    "c": {
                        "type": "boolean",
                        "description": "This is a boolean parameter",
                        "default": False,
                    },
                    "d": {
                        "type": "array",
                        "description": "This is a list parameter",
                        "default": [1, 2, 3],
                    },
                },
                "required": ["a", "b"],
            },
        },
    }
    assert function_typing_list_no_type.schema.to_json() == expected_schema
    assert function_typing_list_no_type.tags == []
