from flask_app.models.painting_model import Painting  # CHANGE THIS
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app import app

bcrypt = Bcrypt(app)

@app.route('/paintings/new')
def new_painting():
      return render_template('painting_new.html')

@app.route('/paintings/create', methods = ['POST'])
def create_painting():
      if "user_id" not in session:
            return('/')
      if not Painting.validator(request.form):
            return redirect('/paintings/new')
      painting_data = {
            **request.form,
            'user_id' : session['user_id']
            }
      Painting.save_painting(painting_data)
      return redirect('/dashboard')


@app.route('/paintings/<int:id>')
def show_painting(id):
      if "user_id" not in session:
            return('/')
      data = {'id': session['user_id']
      }
      this_painting = Painting.get_by_id({'id': id})
      logged_user = User.get_by_id(data)
      return render_template('painting_show.html', this_painting = this_painting, logged_user = logged_user)


@app.route('/paintings/<int:id>/edit')
def edit_painting(id):
      if "user_id" not in session:
            return('/')
      data = {'id': id}
      one_painting = Painting.get_by_id(data)
      return render_template('painting_edit.html', one_painting = one_painting)

@app.route('/paintings/<int:id>/update', methods = ['POST'])
def update_painting(id):
      if "user_id" not in session:
            return('/')
      if not Painting.validator(request.form):
            return redirect(f'/paintings/{id}/edit')
      data = {
            **request.form,
            'id' : id,
            }
      Painting.update_painting(data)
      return redirect('/dashboard')


@app.route('/paintings/<int:id>/delete')
def delete_paintings(id):
      if "user_id" not in session:
            return('/')
      data = {'id': id}
      this_painting = Painting.get_by_id(data)
      Painting.delete_painting(data)
      return redirect('/dashboard')