from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
DATABASE = 'recipes'

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        if "first_name" in data:
            self.user = data['first_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, under30, date_made, user_id, first_name) VALUES (%(name)s,%(description)s,%(instructions)s,%(under30)s,%(date_made)s,%(user_id)s, %(first_name)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        # query = "SELECT * FROM recipes;"
        results =  connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for recipe_dict in results:
            print(recipe_dict['date_made'])
            recipes.append( cls(recipe_dict) )
        return recipes
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s, date_made=%(date_made)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['date_made'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid