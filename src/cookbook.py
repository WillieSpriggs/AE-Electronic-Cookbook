import tkinter as tk
from tkinter import ttk
from functools import partial
from backend_commands import backend
from datetime import datetime

global_backend = backend()

class Application(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    self.container = tk.Frame(self)
    self.container.pack(side='top', fill='both', expand=True)
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    self.current_recipe = None

    for F in (Login, SignUp):
      self.add_frame(F)
    
    self.show_frame('Login')

  def load_home_frame(self):
    self.add_frame(Home)
    self.show_frame('Home')

  def load_recipe_frame(self):
    self.add_frame(ViewRecipe)
    self.show_frame('ViewRecipe')

  def load_edit_frame(self):
    self.add_frame(EditRecipe)
    self.show_frame('EditRecipe')

  def add_frame(self, F):
    page_name = F.__name__
    frame = F(parent=self.container, controller=self)
    self.frames[page_name] = frame
    frame.grid(row=0, column=0, sticky='nsew')
  
  def remove_frame(self, page_name):
    frame = self.frames[page_name]
    del self.frames[page_name]
    frame.grid_forget()
    frame.destroy()

  def show_frame(self, page_name):
    frame=self.frames[page_name]
    frame.tkraise()

  def get_current_recipe(self):
    return self.current_recipe

  def set_current_recipe(self, recipe):
    self.current_recipe = recipe

class Login(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.pw_err = None
    self.controller = controller
    self.controller.title('AE Electronic Cookbook')

    login_label = tk.Label(self, text='Login')
    login_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)
    
    username = tk.Label(self, text='username:')
    username.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
    self.username_entry = tk.Entry(self)
    self.username_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=4)
    self.username_content = tk.StringVar()
    self.username_entry['textvariable'] = self.username_content
  
    password = tk.Label(self, text='password:')
    password.grid(row=2, column=0, sticky=tk.W, padx=10, pady=4)
    self.password_entry = tk.Entry(self)
    self.password_entry.grid(row=2, column=1, sticky=tk.E, padx=10, pady=4)
    self.password_content = tk.StringVar()
    self.password_entry['textvariable'] = self.password_content
  
    signup_button = tk.Button(self, text='Sign Up', command=self.signup)
    signup_button.grid(row=3, column=1, sticky=tk.W, padx=10, pady=4)

    login_button = tk.Button(self, text='Login', command=self.login)
    login_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=4)

  def login(self):
    usr = self.username_content.get()
    pw = self.password_content.get()
    if global_backend.login(usr,pw) == True:
      if self.pw_err != None:
        self.pw_err.after(1,self.pw_err.destroy())
        self.pw_err = None
      self.controller.load_home_frame()
    else:
      self.pw_err = tk.Label(self, text='Incorrect username/password')
      self.pw_err.grid(row=4, column=1, sticky=tk.E, padx=0, pady=0)
      self.username_entry.delete(0,'end')
      self.password_entry.delete(0,'end')
  
  def signup(self):
    if self.pw_err != None:
      self.pw_err.after(1,self.pw_err.destroy())
      self.pw_err = None
    self.password_entry.delete(0,'end')
    self.username_entry.delete(0,'end')
    self.controller.show_frame('SignUp')

class SignUp(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    self.usr_taken = None
    signup_label = tk.Label(self, text='Sign Up')
    signup_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)
    
    username = tk.Label(self, text='username:')
    username.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
    self.username_entry = tk.Entry(self)
    self.username_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=4)
    self.username_content = tk.StringVar()
    self.username_entry['textvariable'] = self.username_content
  
    password = tk.Label(self, text='password:')
    password.grid(row=2, column=0, sticky=tk.W, padx=10, pady=4)
    self.password_entry = tk.Entry(self)
    self.password_entry.grid(row=2, column=1, sticky=tk.E, padx=10, pady=4)
    self.password_content = tk.StringVar()
    self.password_entry['textvariable'] = self.password_content
  
    back_button = tk.Button(self, text='Back', command=self.back_to_login)
    back_button.grid(row=3, column=1, sticky=tk.W, padx=10, pady=4)

    signup_button = tk.Button(self, text='Sign Up', command=self.create_user)
    signup_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=4)
  
  def back_to_login(self):
    if self.usr_taken != None:
      self.usr_taken.after(1,self.usr_taken.destroy())
      self.usr_taken = None
    self.password_entry.delete(0,'end')
    self.username_entry.delete(0,'end')
    self.controller.show_frame('Login')

  def create_user(self):
    usr = self.username_content.get()
    pw = self.password_content.get()
    self.password_entry.delete(0,'end')
    self.username_entry.delete(0,'end')
    if global_backend.register(usr,pw,"testf","testl") == True:
      print('registering user: ', usr, '\nwtih password: ', pw)
      if self.usr_taken != None:
        self.usr_taken.after(1000,self.usr_taken.destroy())
        self.usr_taken = None
      self.controller.show_frame('Login')
      
    else:
      self.usr_taken = tk.Label(self, text='Username taken')
      self.usr_taken.grid(row=4, column = 1, sticky=tk.W, padx=10, pady=6)

recipes = [{'name': 'Beef Stew', 'description': 'Really yummy stew.'}, 
        {'name': 'Chicken Alfredo', 'description': 'It has spinach in it. Yum.'}, 
        {'name': 'Veggie Stew', 'description': 'This one is for the healthy eaters.'}]

class Home(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    home_label = tk.Label(self, text='Home')
    home_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 0))

    recipe_label = tk.Label(self, text='Recipe')
    recipe_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=(15,0))
    description_label = tk.Label(self, text='Description')
    description_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=(15, 0))
    row_num = 2
    for recipe in recipes:
      recipe_title = tk.Label(self, text=recipe['name'])
      recipe_title.grid(row=row_num, column=0, sticky=tk.W, padx=10)
      recipe_description = tk.Label(self, text=recipe['description'])
      recipe_description.grid(row=row_num, column=1, sticky=tk.W, padx=10)
      view_button = tk.Button(self, text='View', command=partial(self.view_recipe, recipe['name']))
      view_button.grid(row=row_num, column=2, sticky=tk.W, padx=10)
      row_num = row_num+1

    create_recipe_button = tk.Button(self, text='Create Recipe', command=self.create_recipe)
    create_recipe_button.grid(row=30, column=0, sticky=tk.W, padx=10, pady=(2,10))
    
  def view_recipe(self, recipe=None):
    self.controller.set_current_recipe(recipe)
    self.controller.load_recipe_frame()
    self.controller.remove_frame('Home')

  def create_recipe(self):
    self.controller.set_current_recipe('new recipe')
    self.controller.load_recipe_frame()
    self.controller.remove_frame('Home')

created_by = [{'creator_user': 'Willie2018', 'recipe_name': '', 'date_created': '11/28/2021', 'last_updated': '11/29/2021'}]
contains_ingredient = [{'recipe_name': '', 'ingredient_name': 'salt', 'amount': 1, 'measurement': 'tablespoon'}, 
                      {'recipe_name': '', 'ingredient_name': 'pepper', 'amount': 2, 'measurement': 'teaspoons'},
                      {'recipe_name': '', 'ingredient_name': 'sugar', 'amount': 5, 'measurement': 'pinches'}]
steps = [{'recipe_name': '', 'num': 1, 'description': 'Add in sugar.'}, 
        {'recipe_name': '', 'num': 2, 'description': 'Add in pepper.'},
        {'recipe_name': '', 'num': 3, 'description': 'Add in salt.'}]
nutrition = [{'recipe_name': '', 'servings': 4, 'calories': 100, 'saturated_fat': 10, 'trans_fat': 11, 'cholesterol': 20, 'sodium': 5, 
        'total_carbs': 20, 'dietary_fiber': 30, 'sugars': 10, 'protein': 0}]
nutrition_measurement = {'servings': '', 'calories': '', 'saturated_fat': 'g', 'trans_fat': 'g', 'cholesterol': 'mg', 'sodium': 'mg', 
        'total_carbs': '', 'dietary_fiber': 'g', 'sugars': 'g', 'protein': 'g'}

class ViewRecipe(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    current_recipe = self.controller.get_current_recipe()
    recipe_title = tk.Label(self, text=current_recipe)
    recipe_title.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 0))
    author_label = tk.Label(self, text='Author: ' + created_by[0]['creator_user'])
    author_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=(10, 0))
    creation_label = tk.Label(self, text='Date Created: ' + created_by[0]['date_created'])
    creation_label.grid(row=1, column=0, sticky=tk.W, padx=10)
    updated_label = tk.Label(self, text='Last Updated: ' + created_by[0]['last_updated'])
    updated_label.grid(row=1, column=1, sticky=tk.W, padx=10)
    description_label = tk.Label(self, text='Description: ' + recipes[1]['description'])
    description_label.grid(row=2, column=0, sticky=tk.W, padx=10)
    
    ingredients_title = tk.Label(self, text="Ingredients")
    ingredients_title.grid(row=3, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    row_num = 4
    for I in contains_ingredient:
      ingredient = tk.Label(self, text=I['ingredient_name']+': '+str(I['amount'])+' '+I['measurement'])
      ingredient.grid(row=row_num, column=0, sticky=tk.W, padx=10)
      row_num = row_num + 1

    steps_title = tk.Label(self, text='Steps')
    steps_title.grid(row=row_num, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    row_num = row_num + 1

    for S in steps:
      recipe_step = tk.Label(self, text=str(S['num'])+'. '+S['description'])
      recipe_step.grid(row=row_num, column=0, sticky=tk.W, padx=10)
      row_num = row_num + 1

    nutrition_title = tk.Label(self, text='Nutrition Facts')
    nutrition_title.grid(row=row_num, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    row_num = row_num + 1

    # iterates through dictionary keys
    for N in nutrition[0]:
      if (N != 'recipe_name'):
        nutrition_fact = tk.Label(self, text=N+': '+ str(nutrition[0][N])+nutrition_measurement[N])
        nutrition_fact.grid(row=row_num, column=0, sticky=tk.W, padx=10)
        row_num = row_num + 1
    
    back_button = tk.Button(self, text='Back', command=self.back_to_home)
    back_button.grid(row=row_num, column=1, sticky=tk.E, padx=(0,50), pady=(2,10))
    edit_button = tk.Button(self, text='Edit', command=self.edit_recipe)
    edit_button.grid(row=row_num, column=1, sticky=tk.E, padx=10, pady=(2,10))

  def back_to_home(self):
    self.controller.load_home_frame()
    self.controller.remove_frame('ViewRecipe')

  def edit_recipe(self):
    self.controller.load_edit_frame()

class EditRecipe(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    current_recipe = self.controller.get_current_recipe()

    recipe_title = tk.Entry(self)
    recipe_title.grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 0))
    self.recipe_title_contents = tk.StringVar()
    self.recipe_title_contents.set(current_recipe)
    recipe_title['textvariable'] = self.recipe_title_contents
    author_label = tk.Label(self, text='Author: ' + created_by[0]['creator_user'])
    author_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=(10, 0))
    creation_label = tk.Label(self, text='Date Created: ' + created_by[0]['date_created'])
    creation_label.grid(row=1, column=0, sticky=tk.W, padx=10)
    updated_label = tk.Label(self, text='Last Updated: ' + created_by[0]['last_updated'])
    updated_label.grid(row=1, column=1, sticky=tk.W, padx=10)
    description = tk.Entry(self)
    description.grid(row=2, column=0, sticky=tk.W, padx=10)
    self.description_contents = tk.StringVar()
    self.description_contents.set(recipes[1]['description'])
    description['textvariable'] = self.description_contents
    
    ingredients_title = tk.Label(self, text="Ingredients")
    ingredients_title.grid(row=3, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    amounts_title = tk.Label(self, text="Amounts")
    amounts_title.grid(row=3, column=1, sticky=tk.W, padx=10, pady=(15, 0))
    measurements_title = tk.Label(self, text="Measurements")
    measurements_title.grid(row=3, column=2, sticky=tk.W, padx=10, pady=(15, 0))
    base_row = 10
    self.ingredient_id = 0
    self.ingredients_dict = {}
    for I in contains_ingredient:
      self.add_ingredient(I, base_row)
    add_ingredient_button = tk.Button(self, text='Add Ingredient', command=partial(self.add_ingredient, {'recipe_name': '', 'ingredient_name': '', 'amount': 0, 'measurement': ''}, base_row))
    add_ingredient_button.grid(row=30, column=0, sticky=tk.W, padx=10, pady=4)
 
    steps_title = tk.Label(self, text='Steps')
    steps_title.grid(row=31, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    base_row = 32
    self.step_id = 0
    self.steps_dict = {}
    for S in steps:
      self.add_step(S, base_row)
    add_step_button = tk.Button(self, text='Add Step', command=partial(self.add_step, {'recipe_name': '', 'num': self.step_id+1, 'description': ''}, base_row))
    add_step_button.grid(row=52, column=0, sticky=tk.W, padx=10, pady=4)

    nutrition_title = tk.Label(self, text='Nutrition Facts')
    nutrition_title.grid(row=53, column=0, sticky=tk.W, padx=10, pady=(15, 0))
    row_num = 54
    nutrition_id = 0
    self.nutritition_dict = {}
    # iterates through dictionary keys
    for N in nutrition[0]:
      if (N != 'recipe_name'):
        label = N
        if (nutrition_measurement[N] != ''):
          label = N +'('+nutrition_measurement[N]+')'
        nutrition_fact_label = tk.Label(self, text=label+': ')
        nutrition_fact_label.grid(row=row_num, column=0, sticky=tk.W, padx=10)
        nutrition_fact = tk.Entry(self)
        nutrition_fact.grid(row=row_num, column=1, sticky=tk.W, padx=10)
        nutrition_fact_contents = tk.StringVar()
        nutrition_fact_contents.set(str(nutrition[0][N]))
        nutrition_fact['textvariable'] = nutrition_fact_contents
        self.nutritition_dict[N] = nutrition_fact_contents
        row_num = row_num + 1
    
    back_button = tk.Button(self, text='Back', command=self.back_to_recipe)
    back_button.grid(row=70, column=2, sticky=tk.E, padx=0, pady=(2,10))
    submit_button = tk.Button(self, text='Submit', command=self.submit_edits)
    submit_button.grid(row=70, column=3, sticky=tk.W, padx=10, pady=(2,10))

  def back_to_recipe(self):
    self.controller.show_frame('ViewRecipe')
    self.controller.remove_frame('EditRecipe')

  def list_util(self,dict,table):
    tmp = []
    for ele in global_backend.table_map[table]:
      if ele in dict:
        tmp.append(dict[ele])
    return tmp

  def submit_edits(self):
    self.controller.remove_frame('ViewRecipe')
    
    date = str(datetime.now().strftime('%m/%d/%Y'))
    recipe = {'name': self.recipe_title_contents.get(), 'description': self.description_contents.get()}
    recipe = self.list_util(recipe,"recipe")
    global_backend.insert("recipe",recipe) #update original insert
    
    created_by = {'creator_user': 'a', 'recipe_name': self.recipe_title_contents.get(), 'date_created': date, 'last_updated': date}
    created_by = self.list_util(created_by,"created_by")
    global_backend.insert("created_by",created_by)

    for ingredient_id in self.ingredients_dict:
      global_backend.execute_query("select * from ingredient where name = '" + self.ingredients_dict[ingredient_id]['i_var'].get() + "';")
      if len(global_backend.results) == 0:
        global_backend.insert("ingredient",[self.ingredients_dict[ingredient_id]['i_var'].get()])
      dct = {
        'recipe_name': self.recipe_title_contents.get(), 
        'ingredient_name': self.ingredients_dict[ingredient_id]['i_var'].get(), 
        'amount': float(self.ingredients_dict[ingredient_id]['a_var'].get()), 
        'measurement': self.ingredients_dict[ingredient_id]['m_var'].get()
        }
      global_backend.insert("contains_ingredient",self.list_util(dct,"contains_ingredient"))
    
    for nutrition_fact in self.nutritition_dict:
      self.nutritition_dict[nutrition_fact] = float(self.nutritition_dict[nutrition_fact].get())
    self.nutritition_dict["recipe_name"] = self.recipe_title_contents.get()
    global_backend.insert("nutrition",self.list_util(self.nutritition_dict,"nutrition"))
    
    for step_id in self.steps_dict:
      tmp = int(step_id) + 1
      dict = {
        'recipe_name': self.recipe_title_contents.get(), 
        'num': str(tmp), 
        'description': self.steps_dict[step_id]['var'].get()
        }
      global_backend.insert("step",self.list_util(dict,"step"))

    self.controller.load_recipe_frame()
    self.controller.remove_frame('EditRecipe')

  def delete_ingredient(self, ingredient_id):
    ingredient = self.ingredients_dict.pop(ingredient_id)
    for key in ingredient:
      if key in ['i_entry', 'a_entry', 'm_entry', 'button']:
        ingredient[key].grid_remove()

  def delete_step(self, step_id):
    step = self.steps_dict.pop(step_id)
    for key in step:
      if key != 'var':
        step[key].grid_remove()

  def add_ingredient(self, I, base_row):
    if ((base_row+self.ingredient_id) < 30):
      ingredient = tk.Entry(self)
      ingredient.grid(row=base_row+self.ingredient_id, column=0, sticky=tk.W, padx=10)
      ingredient_contents = tk.StringVar()
      ingredient_contents.set(I['ingredient_name'])
      ingredient['textvariable'] = ingredient_contents
      amount = tk.Entry(self)
      amount.grid(row=base_row+self.ingredient_id, column=1, sticky=tk.W, padx=10)
      amount_contents = tk.StringVar()
      amount_contents.set(I['amount'])
      amount['textvariable'] = amount_contents
      measurement = tk.Entry(self)
      measurement.grid(row=base_row+self.ingredient_id, column=2, sticky=tk.W, padx=10)
      measurement_contents = tk.StringVar()
      measurement_contents.set(I['measurement'])
      measurement['textvariable'] = measurement_contents
      delete_button = tk.Button(self, text='Delete', command=partial(self.delete_ingredient, self.ingredient_id))
      delete_button.grid(row=base_row+self.ingredient_id, column=3, sticky=tk.W, padx=10)
      self.ingredients_dict[self.ingredient_id] = {'i_entry': ingredient, 'i_var': ingredient_contents, 'a_entry': amount, 'a_var': amount_contents, 'm_entry': measurement, 'm_var': measurement_contents, 'button': delete_button}
      self.ingredient_id = self.ingredient_id + 1

  def add_step(self, S, base_row):
    if ((base_row+self.step_id) < 52):
      recipe_step = tk.Entry(self)
      recipe_step.grid(row=base_row+self.step_id, column=0, sticky=tk.W, padx=10)
      step_contents = tk.StringVar()
      step_contents.set(S['description']) 
      recipe_step['textvariable'] = step_contents
      delete_button = tk.Button(self, text='Delete', command=partial(self.delete_step, self.step_id))
      delete_button.grid(row=base_row+self.step_id, column=1, sticky=tk.W, padx=10)
      self.steps_dict[self.step_id] = {'entry': recipe_step, 'var': step_contents, 'button': delete_button}
      self.step_id = self.step_id + 1

if __name__ == "__main__":
  app = Application()
  app.mainloop()
  #global_backend.drop_db()

