import json

def format_markdown(tables_columns_dict: dict) -> str:
    """
    Format the table columns in markdown format
    """
    markdown_str = "Here is the database schema:\n\n"
    for table_name, columns in tables_columns_dict.items():
        markdown_str += f"### Table: {table_name}\n"
        markdown_str += f"Columns: {columns}\n\n"
        markdown_str += "-----------------------------------\n\n"
    return markdown_str

def format_json(tables_columns_dict: dict) -> str:
    """
    Format the table columns in json format
    """
    return json.dumps(tables_columns_dict, indent=4)

