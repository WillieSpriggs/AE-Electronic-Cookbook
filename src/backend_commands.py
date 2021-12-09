import psycopg2
import hashlib

class backend:
    init_db = True #bool to check whether tables need to be created for the DB
    recipe = ["name","description"]
    ingredient = ["name"]
    creator = ["username","password"]
    created_by = ["creator_user","recipe_name","date_created","last_updated"]
    contains_ingredient = ["recipe_name","ingredient_name","amount","measurement"]
    step = ["recipe_name","num","description"]
    nutrition = ["recipe_name", "servings" , "calories" , "saturated_fat" , "trans_fat" , "cholesterol" , "sodium" , "total_carbs", "dietary_fiber", "sugars", "protein"]
    table_map = {"recipe":recipe,"ingredient":ingredient,"creator":creator,"created_by":created_by,"contains_ingredient":contains_ingredient,"step":step,"nutrition":nutrition}
    
    def __init__(self) -> None:
        self.connect_db("postgres") #sign into default postgres db to create aggieeats db
        self.execute_query('CREATE database aggieeats;') #attempt to create aggieeats db, does nothing if already exists
        self.connect_db("aggieeats") #connect to aggieeats db
        if self.init_db: #create tables/schema along with DB
            cmd = ''
            with open('..\\lib\\sql.txt', 'r') as file:
                cmd += file.read().replace('\n', '') #append all 7 CREATE TABLE commands to cmd
            self.execute_query(cmd) #init tables

    def execute_query(self,command):
        try:
            self.cursor.execute(command)
            self.get_results() #automatically refreshes results
        except Exception as err:
            if type(err) == psycopg2.errors.DuplicateDatabase: #check for preexisting DB to see if new tables need to be added
                self.init_db = False #this is used to say that an existing db was detected, do not init tables
            else:
                print(err) #for any other type of error, print it out for debugging

    def connect_db(self,db_name):
        try:  #login function to postgres, assumes password is ADMIN. YOU MAY (PROBABLY WILL) NEED TO CHANGE THIS!!!!
            self.conn = psycopg2.connect(database=db_name, user='postgres', password='1722', host='127.0.0.1', port= '5432') #establishing the connection)
            self.conn.autocommit = True #reduce total loc by autocommitting
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(err)
    
    def close_connection(self):
        try:
            self.conn.close()
        except Exception as err:
            print(err)

    def drop_db(self):
        try:
            self.close_connection()
            self.connect_db("postgres")
            self.execute_query("drop database aggieeats;")
            self.close_connection()
        except Exception as err:
            pass
    
    def get_results(self): #this function refreshes the result set and stores it in the class for later references
        try:  
            self.results = self.cursor.fetchall()
        except Exception as err:
            return
    
    def parenth_util(self,lst,table_val = False): #returns a (x,y,z,..) as str of insterted or updated vals
        ret = ""
        str_delim = "\'" if not table_val else "" #get delimiter for strings to conv to sql string format UNLESS its the table column names

        for i in range(0,len(lst)):
            ret += str(lst[i]) if type(lst[i]) != str else str_delim + lst[i] + str_delim #add ele
            ret += ", " if i < len(lst)-1 else "" #add comma if not last
        return "("+ret+")"

    def insert(self,table,vals): #NEED TO UPDATE: add capability to take in a cols, vals list < max len of cols list
        cols = self.table_map[table]
        l,v = len(cols),len(vals) #assert same number of cols and rows
        assert(l == v)
        try:
            command = "INSERT INTO " + table + " " + self.parenth_util(cols,True) +" VALUES " + self.parenth_util(vals) + ";"
            self.execute_query(command)
        except Exception as err:
            raise(err)

    def update(self, tables, attribute, new_value, key):
        original_attribute = attribute
        print("Updating: ")
        for i in range(0, len(tables)):
            table_key = "recipe_name"
            attribute = original_attribute
            
            if(tables[i] == "recipe"):
                table_key = "name"
                if(attribute == "recipe_name"):
                    attribute = "name"
            sql = "UPDATE " + tables[i] + " SET " + attribute + "='" + new_value + "' WHERE " + table_key + "='" + key +"';"
            self.execute_query(sql)

    def hash(self,password):
        return str(hashlib.sha3_512(password.encode()).hexdigest()) #hash password, maybe add salting in future to look good?

    def login(self,username,password): #takes in username and password entered into fields, checks if correct
        sql = "SELECT * FROM creator WHERE username = '" + username +"' AND password = '" + self.hash(password) + "';"
        try:
            self.execute_query(sql)
            if self.results == []: #check resultset, if empty that means no match for usr and pw was found
                return False
            else:   
                return True #match found, meaning that usr + password was correct       
        except Exception as err:
            print(err)

    def register(self,username,password,firstname,lastname): #takes in username and password entered into fields, checks if valid length, checks if already exists
        try:#check if username exists block
            self.execute_query("SELECT * FROM creator WHERE username = '" +  username + "';")
            if self.results == []:
                if len(password) > 0 and len(firstname) > 0 and len(lastname) > 0: #could improve field constraints in future
                    self.insert("creator",[username,self.hash(password),firstname,lastname])
                    return True
            else:
                return False
        except Exception as err:
            print(err)
