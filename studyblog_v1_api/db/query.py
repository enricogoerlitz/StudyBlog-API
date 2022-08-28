"""
Module for custom db queries.
"""

from typing import Any, Union
from django.db import connection


def execute(query, formatter_func=None, *args, **kwargs) -> Union[list[dict[str, Any]], Any]:
    """TODO: add description"""
    cursor = connection.cursor()
    result = cursor.execute(query, *args, **kwargs)
    if formatter_func:
        return formatter_func(cursor, result)
    return serialize_query(cursor, result)


def serialize_query(cursor, result):
    """TODO: add description"""
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, obj)) for obj in result]