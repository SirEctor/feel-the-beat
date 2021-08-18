from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import requests
import json 
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import urllib.parse 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.urls import url_parse


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{table}".format(
    user=os.getenv("POSTGRES_USER"),
    passwd=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    table=os.getenv("POSTGRES_DB"),
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .table_datatypes import *
from .util import *

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=int(id)).first()

@app.route('/')
def home():
    logout_user()
    return render_template('index.html')
	
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('login.html')

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('register.html')
    
@app.route('/add_user', methods= ['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uname = request.form.get('uname')
        psw = request.form.get('psw')
        msg = None
        
        if not uname:
            msg = 'Username is required.'
        elif not psw:
            msg = 'Password is required.'
        elif User.query.filter_by(username=uname).first() is not None:
            msg= f"User {uname} is already registered."

        if not msg:
            new_user = User(username=uname, password=generate_password_hash(psw))
            session['uname'] = uname
            print(session.get('uname'))
            session['password'] = new_user.password
            db.session.add(new_user)
            db.session.commit()
            
            BASE_URL = "https://accounts.spotify.com/authorize"

            url_parameters = {
                    'client_id': os.getenv("CLIENT_ID"), 
                    'response_type': 'code',
                    'redirect_uri': os.getenv("REDIRECT_URI"),
                    'scope': "user-read-private,user-read-recently-played"
            }

            url = BASE_URL + "?" + urllib.parse.urlencode(url_parameters)
            return redirect(url)

        flash(msg)
        return render_template("register.html")

@app.route('/confirm_login', methods= ['POST'])
def confirm_login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        psw = request.form.get('psw')
        msg = None
        user = User.query.filter_by(username=uname).first()
        
        if not uname:
            msg = "Username is required."
        elif not uname:
            msg = "Password is required."

        if user is None:
            msg = 'Incorrect username.'
        elif not check_password_hash(user.password, psw):
            msg = 'Incorrect password.'

        if not msg:
            msg = "Login Successful"
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                refreshToken = user.give_refresh_token()
                
                data = {'client_id':os.getenv("CLIENT_ID"), 
                        'client_secret':os.getenv("CLIENT_SECRET"), 
                        'grant_type':'refresh_token',
                        'refresh_token': refreshToken,
                        'redirect_uri':os.getenv("REDIRECT_URI")
                }
                r = requests.post('https://accounts.spotify.com/api/token',data=data)
                error_handling(r, 'confirm_login')
		
            return redirect(next_page)
        flash(msg)
        return render_template("login.html")


@app.route('/logout')
def logout():  
    logout_user()
    return render_template('index.html')

""" @app.route('/dashboard')
def dashboard():
    if 'code' in request.url:
        equalIndex = request.url.index('=')
        authorization_code = request.url[equalIndex+1:]  
        currentUser = User.query.filter_by(username=session.get('uname')).first()
        print(session.get('uname'))
        session['authorization_code'] = authorization_code
        print(currentUser.username)
        currentUser.set_auth_code(authorization_code)

        db.session.commit()
        login_user(currentUser)
        return redirect('/test_analytics')
        
    return render_template('dashboard.html') """


@app.route('/dashboard/')
def dashboard():
    data = {'client_id':os.getenv("CLIENT_ID"), 
        'client_secret':os.getenv("CLIENT_SECRET"), 
        'grant_type':'authorization_code',
        'code':jsvar,
        'redirect_uri':os.getenv("REDIRECT_URI")
        }
    r = requests.post('https://accounts.spotify.com/api/token',data=data)
    

    if r.status_code == 200:
        s = json.loads(r.text)
    
    
        access_token = s['access_token']
    
        token_type = s['token_type']
        expires_in = s['expires_in']
        refresh_token = s['refresh_token']
        currentUser = User.query.filter_by(username= session.get('username')).first()
        
    
        currentUser.set_refresh_token(refresh_token)
        session['refresh_token'] = refresh_token
        db.session.commit()
        scope = s['scope']
    
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
    
        # Get recently reproduces tracks
        resTracks = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=3',headers=headers)
        resTracks_Text = json.loads(resTracks.text)

        trackN0 = resTracks_Text['items'][0]['track']['name']
        trackArtist0 = resTracks_Text['items'][0]['track']['album']['artists'][0]['name']
        trackName0 = trackN0 + "  -  " + trackArtist0
        trackId0 = resTracks_Text['items'][0]['track']['id']

        trackN1 = resTracks_Text['items'][1]['track']['name']
        trackArtist1 = resTracks_Text['items'][1]['track']['album']['artists'][0]['name']
        trackName1 = trackN1 + "  -  " + trackArtist1
        trackId1 = resTracks_Text['items'][1]['track']['id']
        
        trackN2 = resTracks_Text['items'][2]['track']['name']
        trackArtist2 = resTracks_Text['items'][2]['track']['album']['artists'][0]['name']
        trackName2 = trackN2 + "  -  " + trackArtist2
        trackId2 = resTracks_Text['items'][2]['track']['id']
        
        trackN3 = resTracks_Text['items'][3]['track']['name']
        trackArtist3 = resTracks_Text['items'][3]['track']['album']['artists'][0]['name']
        trackName3 = trackN3 + "  -  " + trackArtist3
        trackId3 = resTracks_Text['items'][3]['track']['id']

        trackN4 = resTracks_Text['items'][4]['track']['name']
        trackArtist4 = resTracks_Text['items'][4]['track']['album']['artists'][0]['name']
        trackName4 = trackN4 + "  -  " + trackArtist4
        trackId4 = resTracks_Text['items'][4]['track']['id']
        
        
        return render_template('dashboard.html', track0_Name=trackName0, track1_Name=trackName1, track2_Name=trackName2, track3_Name=trackName3, track4_Name=trackName4)
    else:
        return render_template('result.html')

@app.route('/test_analytics')
def test_analytics():
    authorization_code = session['authorization_code']
    data = {'client_id':os.getenv("CLIENT_ID"), 
            'client_secret':os.getenv("CLIENT_SECRET"), 
            'grant_type':'authorization_code',
            'code': authorization_code,
            'redirect_uri':os.getenv("REDIRECT_URI")
            }
    r = requests.post('https://accounts.spotify.com/api/token',data=data)
    error_handling(r, 'test_analytics')
if __name__ == '__main__':
    app.run(debug=True)
