import sqlite3

try:
    connection = sqlite3.connect('data.db')
    create_table_query = '''
            CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL);
        '''

    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    add_admin =(1,"vlad","12345")
    add_query = '''
        INSERT INTO users values (?,?,?);
    '''
    test_users = [
        (2,"carl","1234555"),
        (3,"kreng","12345666"),
        (4,"bob","123457777")
    ]
    cursor.execute(add_query, add_admin)
    cursor.executemany(add_query,test_users)
    connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if connection:
        connection.close()