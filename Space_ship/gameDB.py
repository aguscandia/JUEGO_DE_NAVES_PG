import sqlite3

class GameDB:
    def __init__(self, name):
        self.conn = sqlite3.connect(name)

    # metodo para saber si existe una tabla

    def table_exist(self):
        c = self.conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='puntos' ''')
        return c.fetchone()[0] == 1

    # metodo para crear la tabla

    def create_table(self):
        if not self.table_exist():
            try:
                sqlite_create_table_query = '''CREATE TABLE puntos (
                                                 id INTEGER PRIMARY KEY,
                                                 name TEXT NOT NULL,
                                                 score INTEGER NOT NULL);'''
                cursor = self.conn.cursor()
                print("Successfully Connected to SQLite")
                cursor.execute(sqlite_create_table_query)
                self.conn.commit()
                print("SQLite table created")

                cursor.close()

            except sqlite3.Error as error:
                print("Error while creating a sqlite table", error)
        else:
            print("Table exist")

        # metodo para insertar los puntos

    def insert_score(self, name, score):
        try:
            cursor = self.conn.cursor()
            print("Successfully Connected to SQLite")
            values = (name, score)
            sqlite_insert_query = "INSERT INTO puntos (name, score)  VALUES (?, ?)"

            count = cursor.execute(sqlite_insert_query, values)
            self.conn.commit()
            print("Record inserted successfully into puntos table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def get_all_score(self):
        try:
            cursor = self.conn.cursor()
            print("Connected to SQLite")
            # mostrar de puntos de mayor a menor
            sqlite_select_query = """SELECT * FROM puntos ORDER BY score DESC"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            cursor.close()
            return records

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
