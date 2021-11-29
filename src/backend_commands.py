import psycopg2

init_db = True

def execute_query(cursor,command):
    try:
        cursor.execute(command)
    except Exception as err:
        print(err)
    finally:
        return cursor

def connect_db(db_name):
    try:
        conn = psycopg2.connect(database=db_name, user='postgres', password='admin', host='127.0.0.1', port= '5432') #establishing the connection)
        conn.autocommit = True
        cursor = conn.cursor()
    except Exception as err:
        print(err)
    finally:
        return conn,cursor

def print_query(cursor):
    try:  
        results = cursor.fetchall()
        for r in results:
            print(r)
    except Exception as err:
        print(err)
    finally:
        return

conn,cursor = connect_db("postgres")

try:
    create_db = '''CREATE database aggieeats'''; #create the db
    cursor.execute(create_db)
    print("Database initialized")
except psycopg2.errors.DuplicateDatabase:
    print("Database already exists")
    init_db = False
finally:
    print("Closed initial DB")
    conn.close() #close initial connection


conn,cursor = connect_db("aggieeats")

create_table = '''CREATE TABLE test2 (key INTEGER, value INTEGER)''';
insert = '''INSERT INTO test2 (key,value) VALUES (5,6) ''';
search = '''SELECT * FROM test1''';
cursor = execute_query(cursor,create_table)
cursor = execute_query(cursor,insert)
cursor = execute_query(cursor,search)
print_query(cursor)
#Closing the connection
conn.close()