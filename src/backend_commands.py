import psycopg2

init_db = True

def execute_query(cursor,command):
    try:
        cursor.execute(command)
    except Exception as err:
        if type(err) == psycopg2.errors.DuplicateDatabase:
            global init_db
            init_db = False
        else:
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
create_db = '''CREATE database aggieeats''';
cursor = execute_query(cursor,create_db)
conn,cursor = connect_db("aggieeats")

if init_db: #create tables/schema
    cmd = ''
    with open('..\\lib\\sql.txt', 'r') as file:
        cmd += file.read().replace('\n', '')
    cursor = execute_query(cursor,cmd)

else:
    #proceed to gui, gui interfaces wuth backend to perform sql queries
    pass

conn.close()