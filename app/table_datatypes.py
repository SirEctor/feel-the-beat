from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    authorization_code = db.Column(db.String, default=None)
    authenticated = db.Column(db.Boolean, default=False)

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