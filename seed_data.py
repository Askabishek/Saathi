import sqlite3
import pandas as pd
import os

def seed_database(db_path='saathi/data/crime_db.sqlite'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create structured crime table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crimes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT UNIQUE,
        date TEXT,
        type TEXT,
        location TEXT,
        status TEXT,
        description TEXT
    )
    ''')
    
    # Synthetic data
    crimes = [
        ('CR-2026-001', '2026-07-01', 'Theft', 'Downtown', 'Open', 'Stolen laptop from a parked car.'),
        ('CR-2026-002', '2026-07-05', 'Assault', 'Central Park', 'Closed', 'Physical altercation between two individuals.'),
        ('CR-2026-003', '2026-07-10', 'Burglary', 'North Suburbs', 'Open', 'Residential break-in during the night.'),
        ('CR-2026-004', '2026-07-12', 'Vandalism', 'West End', 'Under Investigation', 'Graffiti on public property.'),
        ('CR-2026-005', '2026-07-14', 'Theft', 'Shopping Mall', 'Open', 'Shoplifting incident reported at a retail store.')
    ]
    
    cursor.executemany('''
    INSERT OR IGNORE INTO crimes (case_number, date, type, location, status, description)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', crimes)
    
    conn.commit()
    conn.close()
    print(f"Database seeded at {db_path}")

if __name__ == "__main__":
    seed_database()
