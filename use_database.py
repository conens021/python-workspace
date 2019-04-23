import mysql.connector as db

class UseDatabase:

    def __init__(self,dbconfig:dict) -> None:
        self.configuration = dbconfig
        
    def __enter__(self) -> 'cursor':
        self.conn = db.connect( **self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self,exc_type,exc_value,exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
