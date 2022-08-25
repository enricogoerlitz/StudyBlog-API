"""
Module for typ checking
"""



def is_int(obj, or_float=True):
    try:
        if or_float:
            return True if int(obj) else False
        return int(obj) and not isinstance(obj, float)
    except:
        return False 


def is_string(obj):
    return isinstance(obj, str)


def is_float(obj, or_int=True):
    try:
        if or_int:
            return True if float(obj) else False
        return float(obj) and not isinstance(obj, int)
    except:
        return False 


def is_numeric(obj):
    return is_int(obj) or is_float(obj)


def is_list(obj):
    return isinstance(obj, list)


def is_tuple(obj):
    return isinstance(obj, tuple)


def is_list_or_tuple(obj):
    return is_list(obj) or is_tuple(obj)


def is_dict(obj):
    return isinstance(obj, dict)