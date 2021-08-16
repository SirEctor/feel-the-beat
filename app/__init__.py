from flask import Flask, render_template, request, flash, url_for, redirect, session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import requests
import json 
import os
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

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
            session['username'] = new_user.username
            session['password'] = new_user.password
            db.session.add(new_user)
            db.session.commit()
            
            return render_template("userauth.html", redirect_link = os.getenv("REDIRECT_URI"))     

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
                refreshCode = user.give_refresh_code()
                
                data = {'client_id':os.getenv("CLIENT_ID"), 
                        'client_secret':os.getenv("CLIENT_SECRET"), 
                        'grant_type':'refresh_token',
                        'refresh_token': refreshCode,
                        'redirect_uri':os.getenv("REDIRECT_URI")
                }
                r = requests.post('https://accounts.spotify.com/api/token',data=data)
                
                if r.status_code == 200:
                    s = json.loads(r.text)
                    access_token = s['access_token']
                    
                    storage = getAllAnalytics(access_token)
                    return render_template('testanalytics.html', track0_Name=storage['trackName0'], track1_Name=storage['trackName1'], track2_Name=storage['trackName2'], averageDanceability=storage['averageDance'], averageLiveness=storage['averageLive'])
                else:
                    return render_template('result.html')
            return redirect(next_page)
        flash(msg)
        return render_template("login.html")


@app.route('/logout')
def logout():  
    logout_user()
    return render_template('index.html')

            
@app.route('/testanalytics/', methods = ['POST'])
def access():
    accesstoken = request.form['lastmood']
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accesstoken
    }
    
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played',headers=headers)
    s = json.loads(response.text)

    return render_template('testanalytics.html', recentlyplayed=s)


@app.route('/userauth')
def userauth():
    return render_template('userauth.html')

@app.route('/dashboard/')
def dashboard():
    if 'code' in request.url:
        equalIndex = request.url.index('=')
        authcode = request.url[equalIndex+1:]
		
	
        
        
        currentUser = User.query.filter_by(username= session.get('username')).first()
        
        session['authorization_code'] = authcode
        currentUser.set_auth_code(authcode)
        db.session.commit()
        login_user(currentUser)
        
        return redirect(url_for('get_jsvar', jsvar=authcode))

    

    return render_template('dashboard.html')

@app.route('/getjs/<jsvar>')
def get_jsvar(jsvar):
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
        session['authorization_code'] = access_token
        token_type = s['token_type']
        expires_in = s['expires_in']
        refresh_token = s['refresh_token']
        currentUser = User.query.filter_by(username= session.get('username')).first()
        currentUser.set_refresh_code(refresh_token)
        db.session.commit()
        scope = s['scope']
    
        
        storage = getAllAnalytics(access_token)
        return render_template('testanalytics.html', track0_Name=storage['trackName0'], track1_Name=storage['trackName1'], track2_Name=storage['trackName2'], averageDanceability=storage['averageDance'], averageLiveness=storage['averageLive'])
    else:
        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
