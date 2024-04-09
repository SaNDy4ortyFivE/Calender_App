import sqlite3
import os
import configparser

#Check later with main

# Read database name from config file
config = configparser.ConfigParser()
config.read('config.properties')
DB_FILE = config['database']['db_name']
SAMPLE_SQL = 'database/sample_rows_insert.sql'

def push_records():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    with open(SAMPLE_SQL, 'r') as f:
        stmt = f.readlines()
        for line in stmt:
            if line.startswith("--"):
                continue
            cursor.execute(line)
    conn.commit()
    conn.close()


def create_database():
    """Create SQLite database if it doesn't exist."""
    #if os.path.exists(DB_FILE):
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE Person (
                id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE Meeting (
                id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                from_time TEXT NOT NULL,
                to_time TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE MeetingRoom (
                id INTEGER PRIMARY KEY,
                room_name TEXT NOT NULL,
                room_number INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE MeetingMember (
                meeting_id INTEGER,
                person_id INTEGER,
                FOREIGN KEY(meeting_id) REFERENCES Meeting(id),
                FOREIGN KEY(person_id) REFERENCES Person(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE MeetingDetails (
                id INTEGER PRIMARY KEY,
                room_id INTEGER,
                FOREIGN KEY(room_id) REFERENCES MeetingRoom(id)
            )
        ''')

        conn.commit()
        conn.close()

if __name__ == '__main__':
    create_database()
    push_records()
