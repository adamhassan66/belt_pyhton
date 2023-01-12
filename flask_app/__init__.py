from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "painting_schema" # CHANGE THIS
