from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe import Recipe
# from flask_app import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


DATABASE = "recipes"

class User:
    def __init__(self,data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user_dict in results:
            users.append( cls(user_dict))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,user)
        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Passwords don't match","register")
        return is_valid