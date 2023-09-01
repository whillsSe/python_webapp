from utils import as_dict
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,set_refresh_cookies,get_jwt_identity
from app.models import Authentication,User,Profile,RefreshToken
from app import db,bcrypt,jsonify