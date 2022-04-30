from . import db 
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func


class Snippet(db.Model): # Users' snippets
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.String(128))
    title = db.Column(db.String(50))
    content = db.Column(db.String(3000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    lang = db.Column(db.String(10))
    public = db.Column(db.Boolean, default=True, nullable=False)
  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Profile(db.Model): # User's profile, not important rn
    id = db.Column(db.Integer, primary_key=True)
    pfp = db.Column(db.String(500))
    about_me = db.Column(db.String(2000))
  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin): # user information, username, password, etc
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(150))
  
    snippet = db.relationship('Snippet')
    profile = db.relationship('Profile')