import sqlite3
from sqlite3 import Error


class SQLiteDBConnection:
    '''
        Represent a SQLite DB Connection
    '''
    _instance = None

    def __new__(cls, db_file):
        if cls._instance is None:
            cls._instance = super(SQLiteDBConnection, cls).__new__(cls)
            cls._db_file = db_file
            try:
                cls._instance.connection = sqlite3.connect(db_file)
                print(f"SQLite version: {sqlite3.version}. Connection established to {db_file}")
            except Error as e:
                print(f"Failed to connect to the database. Error: {e}")
        return cls._instance

    @property
    def conn(self):
        return self.connection

    @classmethod
    def close_connection(cls):
        if cls._instance and cls._instance.connection:
            cls._instance.connection.close()
            cls._instance = None
            print("Database connection closed.")