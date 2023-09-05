from datetime import timedelta
from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sqlalchemy:python_basis@localhost:3306/python_basis_06'
app.config['SQLALCHEMY_ECHO'] = True

app.config['JWT_SECRET_KEY'] = 'python_basis_06_tokenKey'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Change this to True for production
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from . import models,resources
from app.resources.authentication import AuthenticationResource
from app.resources.user import UserResource
from app.resources.profile import ProfileResource
from app.resources.login import Login


with app.app_context():
    db.create_all()

api.add_resource(AuthenticationResource,'/authentication')
api.add_resource(UserResource,'/user')
api.add_resource(ProfileResource,'/profile')
api.add_resource(Login,'/login')

if __name__ == '__main__':
    app.run(debug=True)
