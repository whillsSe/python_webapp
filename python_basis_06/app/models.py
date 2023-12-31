from app import db
from datetime import datetime, timedelta
from sqlalchemy_utils import UUIDType
import uuid

class Authentication(db.Model):
    __tablename__ = 'authentications'
    account_uuid = db.Column(UUIDType(binary=False),primary_key=True,default=uuid.uuid4)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(64),nullable=False)
    is_active = db.Column(db.Boolean,default=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    deactivated_at = db.Column(db.DateTime)

    user = db.relationship('User',back_populates='auth',uselist=False)

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_uuid(cls,uuid):
        return cls.query.filter_by(account_uuid=uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __init__(self,email,password):
        self.email = email
        self.password = password

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType(binary=False),db.ForeignKey('authentications.account_uuid'),primary_key=True)
    user_id = db.Column(db.String(64),unique=True,nullable=False)
    username = db.Column(db.String(30),unique=True,nullable=False)
    is_active = db.Column(db.Boolean,default=True)
    auth = db.relationship('Authentication',back_populates='user',uselist=False)
    prof = db.relationship('Profile',back_populates='user',uselist=False)

    def __repr__(self):
        return f'<User {self.user_id}>'
    
    @classmethod
    def find_by_user_id(cls,userId):
        return cls.query.filter_by(user_id=userId).first()
    
    def __init__(self,uuid,user_id,username):
        self.id = uuid
        self.user_id = user_id
        self.username = username

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(UUIDType(binary=False),db.ForeignKey('users.id'),primary_key=True)
    bio = db.Column(db.String(200))
    location = db.Column(db.String(50))
    link = db.Column(db.String(200))
    user = db.relationship('User',back_populates='prof',uselist=False)

class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    jti = db.Column(db.String(255),unique=True,nullable=False)
    uuid = db.Column(UUIDType(binary=False),db.ForeignKey('authentications.account_uuid'),nullable=False)
    is_active = db.Column(db.Boolean,default=True)
    expiration = db.Column(db.DateTime,nullable=False)

    @classmethod
    def find_by_jti(cls,jti):
        return cls.query.filter_by(jti=jti).first()
    
    @classmethod
    def disable_tokens_by_uuid(cls,uuid):
        tokens = cls.query.filter_by(uuid=uuid).all()
        for token in tokens:
            token.is_active = False
        db.session.commit()

    def __init__(self,jti,uuid):
        self.jti = jti
        self.uuid = uuid
        self.expiration = datetime.utcnow() + timedelta(days=30)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()