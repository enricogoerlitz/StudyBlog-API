"""
Module for typ checking.
"""

from typing import Any


def is_int(obj: Any, or_float: bool = True) -> bool:
    """Checks. whether the object is int.
    
    """
    try:
        if or_float:
            return True if int(obj) else False
        return not int(obj) is None and not isinstance(obj, float)
    except:
        return False 


def is_string(obj: Any) -> bool:
    return isinstance(obj, str)


def is_float(obj: Any, or_int: bool = True):
    try:
        if or_int:
            return True if float(obj) else False
        return float(obj) and not isinstance(obj, int)
    except:
        return False 


def is_numeric(obj: Any) -> bool:
    return is_int(obj) or is_float(obj)


def is_list(obj: Any) -> bool:
    return isinstance(obj, list)


def is_tuple(obj: Any) -> bool:
    return isinstance(obj, tuple)


def is_list_or_tuple(obj: Any) -> bool:
    return is_list(obj) or is_tuple(obj)


def is_dict(obj: Any) -> bool:
    return isinstance(obj, dict)