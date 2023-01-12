from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
from flask_app.models import user_model

# ======================================================

class Painting:
  def __init__(self,data):
    self.id = data['id']
    self.title = data['title']
    self.description = data['description']
    self.price = data['price']
    self.created_at = data['created_at']
    self.updated_at = data['updated_at']
    self.user_id = data['user_id']

#============================================
  @classmethod
  def get_all(cls):
    query = """
    SELECT * FROM paintings
    JOIN users ON paintings.user_id = users.id
    """
    results = connectToMySQL(DATABASE).query_db(query)
    all_paintings =[]
    if results:
      for row in results:
        this_painting = cls(row)
        user_data = {
          **row,
          'id': row['users.id'],
          'created_at': row['users.created_at'],
          'updated_at': row['users.updated_at']
        }
        this_user = user_model.User(user_data)
        this_painting.planner = this_user
        all_paintings.append(this_painting)
    return all_paintings
# ===============================================
  @classmethod
  def save_painting(cls, data):
      query = """
      INSERT INTO paintings (title, description, price, user_id)
      VALUES (%(title)s, %(description)s, %(price)s, %(user_id)s);
      """
      return connectToMySQL(DATABASE).query_db(query, data)
# =================================================

  @classmethod 
  def get_by_id(cls,data):
      query = """
      SELECT * FROM paintings JOIN users ON paintings.user_id = users.id
      WHERE paintings.id = %(id)s
      """
      results = connectToMySQL(DATABASE).query_db(query, data)
      if results:
        this_painting = cls(results[0])
        row = results[0]
        user_data = {
          **row,
          'id': row['users.id'],
          'created_at': row['users.created_at'],
          'updated_at': row['users.updated_at']
        }
        this_user = user_model.User(user_data)
        this_painting.writer = this_user
        return this_painting
      return False
# =================================================

  @classmethod
  def update_painting(cls, data):
      query = """
      UPDATE paintings SET title=%(title)s, description=%(description)s, 
      price=%(price)s WHERE id = %(id)s
      """
      return connectToMySQL(DATABASE).query_db(query, data)

# =====================================================

  @classmethod
  def delete_painting(cls,data):
    query ="""
    DELETE FROM paintings WHERE id = %(id)s;
    """
    return connectToMySQL(DATABASE).query_db(query,data)

# =====================================================

  @staticmethod
  def validator(form_data):
    is_valid = True

    # this is validation for  title
    if len(form_data['title']) < 2:
      flash('Title must be atleast 2 characters')
      is_valid = False

      # validation for description
    if len(form_data['description']) < 10:
      flash('description must be atleast 10 characters')  
      is_valid = False

  # validation for price
    if len(form_data['price']) < 0:
      flash('price must be greated 0 character')
      is_valid= False
    
    return is_valid

