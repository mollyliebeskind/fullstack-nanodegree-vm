import psycopg2

connection = psycopg2.connect('dbname=example')

def add_new_row():

    cursor = connection.cursor()

    SQL_Drop = "DROP TABLE IF EXISTS table2"

    SQL_Create = """
        CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        description VARCHAR NOT NULL)
        """

    SQL_insert = """
        INSERT INTO table2 (id, description)
        VALUES (%s, %s)
        """
    
    data_1 = (1, "First test")
    data_2 = (2, "Second test")

    cursor.execute(SQL_Drop)
    cursor.execute(SQL_Create)
    cursor.execute(SQL_insert, data_1)
    cursor.execute(SQL_insert, data_2)

    cursor.execute("SELECT * FROM table2")

    result =cursor.fetchall()
    print(result)

    connection.commit()

    connection.close()
    cursor.close()

add_new_row()


