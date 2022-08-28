"""
Module for custom db queries.
"""

from typing import Any, Callable

from django.db import connection
from django.db.backends.utils import CursorWrapper


def execute(query: str, formatter_func: Callable[[CursorWrapper, Any], Any] = None, *args, **kwargs) -> Any:
    """Execute a custom SQL query on the database. Returns the prepared result."""
    cursor = connection.cursor()
    result = cursor.execute(query, *args, **kwargs)
    
    if formatter_func:
        return formatter_func(cursor, result)
    return serialize_query(cursor, result)


def serialize_query(cursor: CursorWrapper, result: Any) -> list[dict[str, Any]]:
    """Returns a prepared db query result"""
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, obj)) for obj in result]