import sqlite3
import pandas as pd

class SQLTool:
    def __init__(self, db_path='saathi/data/crime_db.sqlite'):
        self.db_path = db_path

    def execute_query(self, query):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df.to_dict(orient='records')
        except Exception as e:
            return f"Error: {str(e)}"

    def get_schema(self):
        return """
        Table: crimes
        Columns: id (INT), case_number (TEXT), date (TEXT), type (TEXT), location (TEXT), status (TEXT), description (TEXT)
        """
