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

def insert(cursor,table,cols,vals):
    l,v = len(cols),len(vals)
    assert(l == v) 
    try:
        command = ["INSERT INTO " + table, " (",") VALUES (",");"]
        for i in range(0,l):
            val = vals[i]
            if type(val) == str:
                val = "\'" + val + "\'"
            tmp = [str(cols[i]),str(val)]
            if i < l-1:
                tmp = [col + ", " for col in tmp]
            command[1] += tmp[0]
            command[2] += tmp[1]
        cursor.execute("".join(command))
    except Exception as err:
        print(err)
    finally:
        return

def search_for_recipe_by_name(cursor,search_word): #searces recipes by name
    try:
        command = "SELECT name FROM recipe WHERE name LIKE \'%" + str(search_word) + "%\';"
        cursor.execute(command)
        print_query(cursor)
    except Exception as err:
        print(err)
    finally:
        pass

def login(cursor,username,password): #takes in username and password entered into fields, checks if correct
    pass

def register(cursor,username,password): #takes in username and password entered into fields, checks if valid length, checks if already exists
    #check if username exists block
    #check if password valid block
    #check if fname and lname not empty and only char
    pass

conn,cursor = connect_db("postgres") #sign into default postgres db to create aggieeats db
execute_query(cursor,'CREATE database aggieeats;') #attempt to create aggieeats db, does nothing if already exists
conn,cursor = connect_db("aggieeats") #connect to aggieeats db

if init_db: #create tables/schema along with DB
    cmd = ''
    with open('..\\lib\\sql.txt', 'r') as file:
        cmd += file.read().replace('\n', '') #append all 7 CREATE TABLE commands to cmd
    execute_query(cursor,cmd)

#insert(cursor,"recipe",["name","description"],["john1","g"])
#search(cursor, "jo")
#proceed to gui, gui interfaces wuth backend to perform sql queries
conn.close()