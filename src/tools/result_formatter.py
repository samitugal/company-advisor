import json
from typing import Any, Dict


def format_markdown(tables_columns_dict: str) -> str:
    """
    Format the table columns in markdown format

    Args:
        tables_columns_dict: Dictionary containing table names and their columns

    Returns:
        Formatted markdown string

    Raises:
        TypeError: If input is not a dictionary
    """
    if not isinstance(tables_columns_dict, dict):
        raise TypeError(
            f"Expected dictionary input, got {type(tables_columns_dict).__name__}"
        )

    markdown_str = "Here is the database schema:\n\n"
    for table_name, columns in tables_columns_dict.items():
        markdown_str += f"### Table: {table_name}\n"
        markdown_str += f"Columns: {columns}\n\n"
        markdown_str += "-----------------------------------\n\n"
    return markdown_str


def format_json(tables_columns_dict: Dict[str, Any]) -> str:
    """
    Format the table columns in json format

    Args:
        tables_columns_dict: Dictionary containing table names and their columns

    Returns:
        Formatted JSON string

    Raises:
        TypeError: If input is not a dictionary
    """
    if not isinstance(tables_columns_dict, dict):
        raise TypeError(
            f"Expected dictionary input, got {type(tables_columns_dict).__name__}"
        )

    return json.dumps(tables_columns_dict, indent=4)
