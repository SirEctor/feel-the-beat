from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    authorization_code = db.Column(db.String, default=None)
    refresh_token = db.Column(db.String, default=None)
    authenticated = db.Column(db.Boolean, default=False)
    
    def set_refresh_code(self, refresh_token):
        self.refresh_code = refresh_token
    
    def set_auth_code(self, authorization_code):
        self.authorization_code = authorization_code
        
    def give_refresh_token(self):
        return self.refresh_token
        
    def give_auth_code(self):
        return self.authorization_code
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_active(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.id

class Song(db.Model):
    __tablename__ = "songs"
    uri = db.Column(db.String, primary_key=True)
    danceability = db.Column(db.Float, nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Float, nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    speechiness = db.Column(db.Float, nullable=False)
    acousticness = db.Column(db.Float, nullable=False)
    instrumentalness = db.Column(db.Float, nullable=False)
    liveness = db.Column(db.Float, nullable=False)
    valence = db.Column(db.Float, nullable=False)
    tempo = db.Column(db.Float, nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    time_signature = db.Column(db.Integer, nullable=False)

class Daily_Record(db.Model):
    __tablename__ = "daily_records"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True, autoincrement=False)
    mood = db.Column(db.String, nullable = False)
    song_uri = db.Column(db.String, db.ForeignKey("songs.uri"))
    

