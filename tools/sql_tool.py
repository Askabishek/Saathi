import pandas as pd
import os

class SQLTool:
    def __init__(self):
    base = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base, '..', 'data', 'crime_data.csv')
    print(f"Loading CSV from: {csv_path}")  # debug
    self.df = pd.read_csv(csv_path)
        self.df.columns = [
            'report_number', 'date_reported', 'date_occurred',
            'time_occurred', 'city', 'crime_code', 'crime_type',
            'victim_age', 'victim_gender', 'weapon_used',
            'crime_domain', 'police_deployed', 'case_closed',
            'date_case_closed'
        ]

    def execute_query(self, query):
        try:
            result = self.df.query(query)
            return result.to_dict(orient='records')
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
