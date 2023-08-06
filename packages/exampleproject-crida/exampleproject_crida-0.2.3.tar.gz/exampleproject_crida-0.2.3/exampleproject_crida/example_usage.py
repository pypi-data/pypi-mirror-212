"""
Example of the proposed architecture for Python projects

Author: smas
Last update: 05/06/2023
"""


def hello_world(return_string: bool = False) -> str | None:
    """
    Example of function definition

    Args:
        return_string: if True, returns a string, else prints a string

    Returns:
        str: "Hello World!" if return_string is True
    """

    if return_string:
        return "Hello World!"
    else:
        print("Hello World!")
        return None
