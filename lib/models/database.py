import sqlite3

class Database:
    DATABASE = 'restaurant.db'
    
    def __init__(self):
        self.connection = sqlite3.connect(self.DATABASE)
    
    def get_cursor(self):
        return self.connection.cursor()
    
    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()

    def execute(self, query, params=()):
        cursor = self.get_cursor()
        cursor.execute(query, params)
        self.commit()
        return cursor

    def fetchall(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetchone(self, query, params=()):
        cursor = self.execute(query, params)
        return cursor.fetchone()
