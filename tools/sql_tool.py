import sqlite3
import pandas as pd

class SQLTool:
    def __init__(self, db_path='data/crime_db.sqlite'):
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
        Columns:
            report_number (TEXT),
            date_reported (TEXT),
            date_occurred (TEXT),
            time_occurred (TEXT),
            city (TEXT),
            crime_code (INT),
            crime_type (TEXT),
            victim_age (INT),
            victim_gender (TEXT),
            weapon_used (TEXT),
            crime_domain (TEXT),
            police_deployed (INT),
            case_closed (TEXT),
            date_case_closed (TEXT)
        """
