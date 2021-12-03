import psycopg2
import hashlib

class backend:
    init_db = True #bool to check whether tables need to be created for the DB
    recpie = ["name","description"]
    ingredient = ["name"]
    creator = ["username","password","firstname","lastname"]
    created_by = ["creator_user","recipe_name","date_created","last_updated"]
    contains_ingredient = ["recipe_name","ingredient_name","amount","measurement"]
    step = ["recipe_name","num","description"]
    nutrition = ["recipe_name", "servings" , "calories" , "saturated_fat" , "trans_fat" , "cholesterol" , "sodium" , "total_carbs", "dietary_fiber", "sugars", "protein"]
    table_map = {"recipe":recpie,"ingredient":ingredient,"creator":creator,"created_by":created_by,"contains_ingredient":contains_ingredient,"step":step,"nutrition":nutrition}
    
    def __init__(self) -> None:
        self.connect_db("postgres") #sign into default postgres db to create aggieeats db
        self.execute_query('CREATE database aggieeats;') #attempt to create aggieeats db, does nothing if already exists
        self.connect_db("aggieeats") #connect to aggieeats db
        if self.init_db: #create tables/schema along with DB
            cmd = ''
            with open('..\\lib\\sql.txt', 'r') as file:
                cmd += file.read().replace('\n', '') #append all 7 CREATE TABLE commands to cmd
            self.execute_query(cmd)

    def execute_query(self,command):
        try:
            self.cursor.execute(command)
            self.get_results()
        except Exception as err:
            if type(err) == psycopg2.errors.DuplicateDatabase: #check for preexisting DB to see if new tables need to be added
                self.init_db = False
            else:
                print(err)

    def connect_db(self,db_name):
        try:
            self.conn = psycopg2.connect(database=db_name, user='postgres', password='admin', host='127.0.0.1', port= '5432') #establishing the connection)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(err)
    
    def get_results(self):
        try:  
            self.results = self.cursor.fetchall()
        except Exception as err:
            print(err)
    
    def print_query(self):
        try:  
            self.get_results()
            for r in self.results:
                print(r)
        except Exception as err:
            print(err)

    def insert(self,table,vals):
        cols = self.table_map[table]
        l,v = len(cols),len(vals)
        assert(l == v)
        try:
            command = ["INSERT INTO " + table + " (",") VALUES (",");"]
            for (col,val) in zip(cols,vals):
                command[0] += col
                command[1] += val if type(val) != str else "\'" + val + "\'" 
                if col != cols[-1]:
                    command[0] += ", "  
                    command[1] += ", "
            self.execute_query("".join(command))
        except Exception as err:
            print(err) 
 
    def search_for_recipe_by_name(self,search_word): #searces recipes by name
        try:
            command = "SELECT name FROM recipe WHERE name LIKE \'%" + str(search_word) + "%\';"
            self.execute_query(command)
            self.print_query(self.cursor)
        except Exception as err:
            print(err)

    def hash(self,password):
        return str(hashlib.sha3_512(password.encode()).hexdigest())

    def login(self,username,password): #takes in username and password entered into fields, checks if correct
        sql = "SELECT * FROM creator WHERE username = '" + username +"' AND password = '" + self.hash(password) + "';"
        try:
            self.execute_query(sql)
            self.get_results()
            print("Password incorrect") if self.results == [] else print("Password correct")             
        except Exception as err:
            print(err)

    def register(self,username,password,firstname,lastname): #takes in username and password entered into fields, checks if valid length, checks if already exists
        new_username = True
        try:#check if username exists block
            sql = "SELECT * FROM creator WHERE username = '" +  username + "';"
            self.execute_query(sql)
            self.get_results()
            if self.results == []:
                print("Eligible username")
            else:
                print("Username already taken")
                new_username = False     
        except Exception as err:
            print(err)

        if len(password) > 0 and len(firstname) > 0 and len(lastname) > 0 and new_username:
            self.insert("creator",[username,self.hash(password),firstname,lastname])

b = backend()
b.register("user12112113","password1","user","name")
b.login("user12213","password1")
b.conn.close()