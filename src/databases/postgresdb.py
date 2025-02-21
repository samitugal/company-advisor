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
                port="5432"             
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
            
            if not results:  # Eğer sonuç boşsa
                return "No data found."

            # 🔥 Sonuçları düz string olarak formatla
            formatted_results = "\n".join([str(row) for row in results])
            print(f"Formatted Results:\n{formatted_results}")  # Debugging için

            return formatted_results

        except (Exception, Error) as error:
            print(f"Error while executing query: {error}")
            return "Database query failed."

        except (Exception, Error) as error:
            print(f"Error while executing query: {error}")
            return None

    def get_tables_columns_dict(self) -> str:
        query = """
            SELECT table_name, array_agg(column_name::text) as columns
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            GROUP BY table_name
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                return "No tables found in the database."

            formatted_tables = "\n".join([f"{table}: {', '.join(columns)}" for table, columns in results])
            print(f"Formatted Tables:\n{formatted_tables}")

            return formatted_tables

        except (Exception, Error) as error:
            print(f"Error while getting tables and columns: {error}")
            return "Error retrieving database schema."
