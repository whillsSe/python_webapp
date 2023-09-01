from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sqlalchemy:python_basis@localhost:3306/python_basis_05'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

from . import models ,routes

with app.app_context():
    db.create_all()
if __name__ == '__main__':
    app.run(debug=True)

