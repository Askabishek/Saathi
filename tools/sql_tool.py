import sqlite3
import pandas as pd
import os

class SQLTool:
    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base, '..', 'data', 'crime_db.sqlite')

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
            report_number, date_reported, date_occurred,
            time_occurred, city, crime_code, crime_type,
            victim_age, victim_gender, weapon_used,
            crime_domain, police_deployed, case_closed,
            date_case_closed
        """
