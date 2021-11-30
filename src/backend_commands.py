import psycopg2

init_db = True #bool to check whether tables need to be created for the DB

def execute_query(cursor,command):
    try:
        cursor.execute(command)
    except Exception as err:
        if type(err) == psycopg2.errors.DuplicateDatabase: #check for preexisting DB to see if new tables need to be added
            global init_db
            init_db = False
        else:
            print(err)
    finally:
        return

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

conn,cursor = connect_db("postgres") #sign into default postgres db to create aggieeats db
create_db = '''CREATE database aggieeats''';
execute_query(cursor,create_db) #attempt to create aggieeats db, does nothing if already exists
conn,cursor = connect_db("aggieeats") #connect to aggieeats db

if init_db: #create tables/schema along with DB
    cmd = ''
    with open('..\\lib\\sql.txt', 'r') as file:
        cmd += file.read().replace('\n', '') #append all 7 CREATE TABLE commands to cmd
    execute_query(cursor,cmd)

#proceed to gui, gui interfaces wuth backend to perform sql queries

conn.close()