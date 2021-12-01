import tkinter as tk
from tkinter import ttk
from functools import partial

class Application(tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    container = tk.Frame(self)
    container.pack(side='top', fill='both', expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    self.frames = {}
    self.current_recipe = None

    for F in (Login, SignUp, Home, ViewRecipe, EditRecipe):
      page_name = F.__name__
      frame = F(parent=container, controller=self)
      self.frames[page_name] = frame
      frame.grid(row=0, column=0, sticky='nsew')
    
    self.show_frame('Login')

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
    self.controller = controller
    self.controller.title('AE Electronic Cookbook')

    login_label = tk.Label(self, text='Login')
    login_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)
    
    username = tk.Label(self, text='username:')
    username.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
    username_entry = tk.Entry(self)
    username_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=4)
    self.username_content = tk.StringVar()
    username_entry['textvariable'] = self.username_content
  
    password = tk.Label(self, text='password:')
    password.grid(row=2, column=0, sticky=tk.W, padx=10, pady=4)
    password_entry = tk.Entry(self)
    password_entry.grid(row=2, column=1, sticky=tk.E, padx=10, pady=4)
    self.password_content = tk.StringVar()
    password_entry['textvariable'] = self.password_content
  
    signup_button = tk.Button(self, text='Sign Up', command=self.signup)
    signup_button.grid(row=3, column=1, sticky=tk.W, padx=10, pady=4)

    login_button = tk.Button(self, text='Login', command=self.login)
    login_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=4)

  def login(self):
    print('signing in user: ', self.username_content.get(), '\nwtih password: ', self.password_content.get())
    self.controller.show_frame('Home')
  
  def signup(self):
    self.controller.show_frame('SignUp')

class SignUp(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    signup_label = tk.Label(self, text='Sign Up')
    signup_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)
    
    username = tk.Label(self, text='username:')
    username.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
    username_entry = tk.Entry(self)
    username_entry.grid(row=1, column=1, sticky=tk.E, padx=10, pady=4)
    self.username_content = tk.StringVar()
    username_entry['textvariable'] = self.username_content
  
    password = tk.Label(self, text='password:')
    password.grid(row=2, column=0, sticky=tk.W, padx=10, pady=4)
    password_entry = tk.Entry(self)
    password_entry.grid(row=2, column=1, sticky=tk.E, padx=10, pady=4)
    self.password_content = tk.StringVar()
    password_entry['textvariable'] = self.password_content
  
    back_button = tk.Button(self, text='Back', command=self.back_to_login)
    back_button.grid(row=3, column=1, sticky=tk.W, padx=10, pady=4)

    signup_button = tk.Button(self, text='Sign Up', command=self.create_user)
    signup_button.grid(row=3, column=1, sticky=tk.E, padx=10, pady=4)
  
  def back_to_login(self):
    self.controller.show_frame('Login')

  def create_user(self):
    print('registering user: ', self.username_content.get(), '\nwtih password: ', self.password_content.get())
    self.controller.show_frame('Home')

recipes = [{'name': 'Beef Stew', 'description': 'Really yummy stew.'}, 
        {'name': 'Chicken Alfredo', 'description': 'It has spinach in it. Yum.'}, 
        {'name': 'Veggie Stew', 'description': 'This one is for the healthy eaters.'}]

class Home(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller

    signup_label = tk.Label(self, text='Home')
    signup_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)

    recipe_label = tk.Label(self, text='Recipe')
    recipe_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=4)
    description_label = tk.Label(self, text='Description')
    description_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=4)
    recipe_row = 2
    for recipe in recipes:
      recipe_title = tk.Label(self, text=recipe['name'])
      recipe_title.grid(row=recipe_row, column=0, sticky=tk.W, padx=10, pady=4)
      recipe_description = tk.Label(self, text=recipe['description'])
      recipe_description.grid(row=recipe_row, column=1, sticky=tk.W, padx=10, pady=4)
      view_button = tk.Button(self, text='View', command=partial(self.view_recipe, recipe['name']))
      view_button.grid(row=recipe_row, column=2, sticky=tk.W, padx=10, pady=4)
      recipe_row = recipe_row+1

  def view_recipe(self, recipe=None):
    self.controller.set_current_recipe(recipe)
    self.controller.show_frame('ViewRecipe')

created_by = [{'creator_user': 'Willie2018', 'recipe_name': '', 'date_created': '11/28/2021', 'last_updated': '11/29/2021'}]
contains_ingredient = [{'recipe_name': '', 'ingredient_name': 'salt', 'amount': 1, 'measurement': 'tablespoon'}, 
                      {'recipe_name': '', 'ingredient_name': 'pepper', 'amount': 2, 'measurement': 'teaspoons'},
                      {'recipe_name': '', 'ingredient_name': 'sugar', 'amount': 5, 'measurement': 'pinches'}]
steps = [{'recipe_name': '', 'num': 1, 'description': 'Add in sugar.'}, 
        {'recipe_name': '', 'num': 2, 'description': 'Add in pepper.'},
        {'recipe_name': '', 'num': 3, 'description': 'Add in salt.'}]
nutrition = [{'recipe_name': '', 'servings': 4, 'calories': 100, 'saturated_fat': 10, 'trans_fat': 11, 'cholesterol': 20, 'sodium': 5, 
        'total_carbs': 20, 'dietary_fiber': 30, 'sugars': 10, 'protein': 0}]

class ViewRecipe(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent)
    self.controller = controller
    current_recipe = self.controller.get_current_recipe()

    print('current_recipe: ', current_recipe)
    recipe_title = tk.Label(self, text=current_recipe)
    recipe_title.grid(row=0, column=0, sticky=tk.W, padx=10, pady=6)
    author_label = tk.Label(self, text='Author: ' + created_by[0]['creator_user'])
    author_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=6)
    creation_label = tk.Label(self, text='Date Created: ' + created_by[0]['date_created'])
    creation_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=6)
    updated_label = tk.Label(self, text='Last Updated: ' + created_by[0]['last_updated'])
    updated_label.grid(row=1, column=1, sticky=tk.W, padx=10, pady=6)


class EditRecipe(tk.Frame):
  def __init__(self, parent, controller):
    tk.Frame.__init__(self, parent, bg='yellow')
    self.controller = controller

    heading = tk.Label(self, text="Edit Recipe")
    heading.pack()

if __name__ == "__main__":
  app = Application()
  app.mainloop()