from Space_ship.entidades import *
import sqlite3

if __name__ == '__main__':
    game = Game()
    conn = sqlite3.connect('mysqlite.db')
    c = conn.cursor()

    # get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='puntos' ''')

    # if the count is 1, then table exists
    if c.fetchone()[0] == 1:
        print('Table exists.')
        try:
            conn = sqlite3.connect('mysqlite.db')
            cursor = conn.cursor()
            print("Successfully Connected to SQLite")

            sqlite_insert_query = """INSERT INTO puntos
                                  (name, score) 
                                   VALUES 
                                  ('James', 100)"""

            count = cursor.execute(sqlite_insert_query)
            conn.commit()
            print("Record inserted successfully into puntos table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")
    else:
        print('Table does not exist.')
        try:
            sqlite_create_table_query = '''CREATE TABLE puntos (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        score INTEGER NOT NULL);'''
            cursor = conn.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            conn.commit()
            print("SQLite table created")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("sqlite connection is closed")

    game.irAlaPortada()
    game.bucle_principal()
