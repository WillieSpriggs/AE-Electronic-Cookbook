import psycopg2
import hashlib

class backend:
    init_db = True #bool to check whether tables need to be created for the DB
    user = ""
    class tables:
        recpie = ["name","description"]
        ingredient = ["name"]
        creator = ["username","password","firstname","lastname"]
        created_by = ["creator_user","recipe_name","date_created","last_updated"]
        contains_ingredient = ["recipe_name","ingredient_name","amount","measurement"]
        step = ["recipe_name","num","description"]
        nutrition = ["recipe_name", "servings" , "calories" , "saturated_fat" , "trans_fat" , "cholesterol" , "sodium" , "total_carbs", "dietary_fiber", "sugars", "protein"]
    
    def __init__(self) -> None:
        self.connect_db("postgres") #sign into default postgres db to create aggieeats db
        self.execute_query('CREATE database aggieeats;') #attempt to create aggieeats db, does nothing if already exists
        self.connect_db("aggieeats") #connect to aggieeats db
        if self.init_db: #create tables/schema along with DB
            self.populate_db()
    
    def populate_db(self):
        cmd = ''
        with open('..\\lib\\sql.txt', 'r') as file:
            cmd += file.read().replace('\n', '') #append all 7 CREATE TABLE commands to cmd
        self.execute_query(cmd)
    
    def drop_db(self):
        self.connect_db("postgres")
        self.execute_query("DROP DATABASE aggieeats;")
        exit(0)

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
            pass
            #print(err)
    
    def print_query(self):
        try:
            for r in self.results:
                print(r)
        except Exception as err:
            print(err)

    def insert(self,table,cols,vals):
        l,v = len(cols),len(vals)
        sql = ["INSERT INTO " + table, " (",") VALUES (",");"]
        assert(l == v)
        for i in range(0,l):
            val = vals[i]
            if type(val) == str:
                val = "\'" + val + "\'"
            tmp = [str(cols[i]),str(val)]
            if i < l-1:
                tmp = [col + ", " for col in tmp]
            sql[1] += tmp[0]
            sql[2] += tmp[1]
        try:
            self.cursor.execute("".join(sql))
        except Exception as err:
            print(err) 
 
    def search_for_recipe_by_name(self,search_word): #searces recipes by name
        try:
            command = "SELECT name FROM recipe WHERE name LIKE \'%" + str(search_word) + "%\';"
            self.cursor.execute(command)
            self.print_query(self.cursor)
        except Exception as err:
            print(err)

    def hash(self,password):
        return str(hashlib.sha3_512(password.encode()).hexdigest())

    def login(self,username,password): #takes in username and password entered into fields, checks if correct
        sql = "SELECT * FROM creator WHERE username = '" + username +"' AND password = '" + self.hash(password) + "';"
        try:
            self.execute_query(sql)
            if self.results == []:
                print("Password incorrect") 
            else:
                print("Password correct")
                self.user = username      
        except Exception as err:
            print(err)

    def register(self,username,password,firstname,lastname): #takes in username and password entered into fields, checks if valid length, checks if already exists
        new_username = True
        sql = "SELECT * FROM creator WHERE username = '" +  username + "';"
        try:
            self.execute_query(sql) #check if username exists
            if self.results == []:
                print("Eligible username")
            else:
                print("Username already taken")
                new_username = False     
        except Exception as err:
            print(err)

        if len(password) > 0 and len(firstname) > 0 and len(lastname) > 0 and new_username:
            self.insert("creator",self.tables.creator,[username,self.hash(password),firstname,lastname])
    
    def create_recipe(self):
        #need list of ingredients with quantities, recipe name, list of steps, nutritional value, user, current date
        pass

b = backend()
b.register("user123","password1","user","name")
b.login("user123","password1")
b.drop_db()
b.conn.close()