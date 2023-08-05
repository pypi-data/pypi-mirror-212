# -*- coding: utf-8 -*-

"""
Utility functions
"""

from functools import reduce
from typing import Any, Callable, Sequence

def pipeline(
        arg: Any,
        function_pipeline: Sequence[Callable],
) -> Any:
    """A generic Unix-like pipeline

    Args:
        arg (Any): The value you want to pass through a pipeline
        function_pipeline (Sequence[Callable]): An ordered 
        list of functions that comprise your pipeline

    Returns:
        Any: A result of functions pipeline
    """
    return reduce(lambda v, f: f(v), function_pipeline, arg)
