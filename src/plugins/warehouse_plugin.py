import json
from typing import Dict, Any
from phi.tools import Toolkit, tool
from phi.utils.log import logger
from pydantic import Field

from src.databases.postgresdb import PostgresDB

class WarehousePlugin(Toolkit):
    def __init__(self, format_type: str = "markdown"):
        super().__init__(
            name="warehouse_plugin",
        )

        if format_type not in ["markdown", "json"]:
            raise ValueError("Invalid format type")

        self.register(self.execute_query)
        self.register(self.get_table_columns)
        self.register(self.get_columns_of_table)

        self.format_type = format_type
        self.db = PostgresDB()
        self.db.connect()

    def execute_query(self, query: str) -> str:
        """
        Execute a query on the database and format the results based on format_type

        Args:
            query (str): The query to execute

        Returns:
            str: The formatted results of the query
        """
        logger.info(f"Executing query: {query}")
        results = self.db.execute_query(query)
        logger.info(f"Results: {results}")
        
        if results is None:
            return "[]" if self.format_type == "json" else "No results found"
            
        if self.format_type == "json":
            return json.dumps(results)
        else:  # markdown format
            if isinstance(results, (list, dict)):
                return str(results)
            return str(results)

    def get_table_columns(self) -> str:
        """
        Get the table columns from the database
        Returns a JSON string of table names and their columns
        """
        logger.info("Getting table columns")
        tables_columns_dict = self.db.get_tables_columns_dict()
        logger.info(f"Tables columns dict: {tables_columns_dict}")

        if tables_columns_dict is None:
            tables_columns_dict = {}

        return json.dumps({"tables_columns_dict": tables_columns_dict, "completed": "Done"})

    def get_columns_of_table(self, table_name: str) -> str:
        """
        Get the columns of a table from the database
        """
        logger.info(f"Getting columns of table: {table_name}")
        columns = self.db.get_columns_of_table(table_name)

        return json.dumps({"table_name": table_name, "columns": columns, "completed": "Done"})

    def disconnect(self):
        self.db.disconnect()

    def __del__(self):
        if hasattr(self, "db"):
            self.db.disconnect()
