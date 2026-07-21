import sqlite3
import pandas as pd
import os

class SQLTool:
    def __init__(self):
        self.db_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..', 'data', 'crime_db.sqlite'
        )
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS crimes (
            id INTEGER PRIMARY KEY,
            city TEXT,
            crime_type TEXT,
            crime_domain TEXT,
            weapon_used TEXT,
            victim_age INTEGER,
            victim_gender TEXT,
            case_closed TEXT,
            year INTEGER
        )''')
        # Synthetic data
        conn.execute("DELETE FROM crimes")
        data = [
            (1,'Chennai','Theft','Other Crime','Knife',25,'M','Yes',2023),
            (2,'Chennai','Assault','Violent Crime','None',30,'F','No',2023),
            (3,'Mumbai','Homicide','Violent Crime','Firearm',40,'M','Yes',2022),
            (4,'Delhi','Fraud','Other Crime','None',35,'F','Yes',2023),
            (5,'Bangalore','Robbery','Violent Crime','Knife',28,'M','No',2023),
            (6,'Chennai','Cybercrime','Other Crime','None',22,'F','Yes',2024),
            (7,'Mumbai','Theft','Other Crime','None',19,'M','Yes',2024),
            (8,'Delhi','Assault','Violent Crime','Blunt Object',45,'M','No',2022),
        ]
        conn.executemany("INSERT INTO crimes VALUES (?,?,?,?,?,?,?,?,?)", data)
        conn.commit()
        conn.close()

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
        Columns: id, city, crime_type, crime_domain,
            weapon_used, victim_age, victim_gender,
            case_closed, year
        """
