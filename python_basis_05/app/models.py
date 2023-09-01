from app import db
from datetime import datetime
from sqlalchemy_utils import UUIDType
import uuid

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUIDType(binary=False),primary_key=True,default=uuid.uuid4)
    username = db.Column(db.String(30),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(64),nullable=False)
    articles = db.relationship('Article',back_populates='author')

    def __repr__(self):
        return f'<User {self.username}>'
    
    
article_tag = db.Table('article_tag',db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),nullable=False,primary_key=True),db.Column('article_id',UUIDType(binary=False),db.ForeignKey('articles.id',ondelete='CASCADE'),nullable=False,primary_key=True))

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(UUIDType(binary=False),primary_key=True,default=uuid.uuid4)
    title = db.Column(db.VARCHAR(255))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    last_updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    user_id = db.Column(UUIDType(binary=False),db.ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    author = db.relationship('User',back_populates='articles')
    tags = db.relationship('Tag',secondary=article_tag,backref='articles')

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    tag = db.Column(db.String(32),primary_key=True)