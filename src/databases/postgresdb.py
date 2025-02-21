from typing import Any, Dict

import psycopg2
from psycopg2 import Error


class PostgresDB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="northwind",
                user="northwind_user",
                password="northwind_pass",
                port="5432",
            )

            self.cursor = self.connection.cursor()

        except (Exception, Error) as error:
            print(f"Unknown error: {error}")

    def disconnect(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection closed")

    def execute_query(self, query) -> str:
        try:
            self.cursor.execute(query)
            self.connection.commit()

            results = self.cursor.fetchall()

            if not results:
                return "No data found."

            formatted_results = "\n".join([str(row) for row in results])
            print(f"Formatted Results:\n{formatted_results}")

            return formatted_results

        except (Exception, Error) as error:
            print(f"Error while executing query: {error}")
            self.connection.rollback()
            return "Database query failed."

    def get_tables_columns_dict(self) -> Dict[str, Any]:
        query = """
            SELECT table_name, array_agg(column_name::text) as columns
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            GROUP BY table_name
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            results = self.cursor.fetchall()

            if not results:
                return "No tables found in the database."

            formatted_tables = {table: columns for table, columns in results}
            print(f"Formatted Tables:\n{formatted_tables}")

            return formatted_tables

        except (Exception, Error) as error:
            print(f"Error while getting tables and columns: {error}")
            self.connection.rollback()
            return f"Error retrieving database schema: {error}"

    def get_columns_of_table(self, table_name: str) -> Dict[str, Any]:
        try:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
            self.cursor.execute(query)
            self.connection.commit()
            results = self.cursor.fetchall()

            if not results:
                return {}

            result = {"table_name": table_name, "columns": [column[0] for column in results]}
            return result
            
        except (Exception, Error) as error:
            print(f"Error while getting columns for table {table_name}: {error}")
            self.connection.rollback()
            return {}
    
if __name__ == "__main__":
    db = PostgresDB()
    db.connect()
    print(db.get_tables_columns_dict())
    db.disconnect()