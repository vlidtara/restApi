import sqlite3

con = sqlite3.connect('mydata.db')
query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username text,
        password text
    );
    CREATE TABLE IF NOT EXISTS items (
        name text,
        price real
    );
    INSERT INTO items VALUES('test', 2000.33);
'''
cursor = con.cursor()
cursor.executescript(query)
con.commit()
con.close()
