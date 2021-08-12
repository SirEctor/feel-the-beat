from flask import Flask, render_template, request, flash, url_for, redirect
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
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
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
            db.session.add(new_user)
            
            return render_template("userauth.html")     

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
            login_user(user, remember=form.remember_me.data)
            authCode = user.give_auth_code()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('get_jsvar', jsvar=authCode)
            return redirect(next_page)
        flash(msg)
        return render_template("login.html")


@app.route('/logout')
def logout():  
    logout_user()
    return render_template('index.html')

@app.route('/analytics', methods = ['POST','GET'])
def analyze():
    if request.method == "POST":
        flash("Mood/Song Personal Matrix updated!")
        return render_template('analytics.html')

    else:
        if request.referrer != None and (('getjs' in request.referrer) or ('analytics' in request.referrer)):
            return render_template('analytics.html')
        else:
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
        baseurl = "https://feelthebeat.tech/dashboard/?code="
        adjustmentfactor = 14
        authcode = request.url[len(baseurl)-adjustmentfactor:]
	
        currentUser = User.query.filter_by(username= current_user.username).first()
        currentUser.set_auth_code(authcode)
        db.session.commit()
        login_user(user)
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
        token_type = s['token_type']
        expires_in = s['expires_in']
        refresh_token = s['refresh_token']
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
        
     
        # Get Audio Features for a Track 
        track0_Charact = requests.get('https://api.spotify.com/v1/audio-features/' + trackId0, headers=headers)
        track0_Charact_Text = json.loads(track0_Charact.text)
        danceLevel0 = float(track0_Charact_Text['danceability'])
        liveLevel0 = float(track0_Charact_Text['liveness'])

        track1_Charact = requests.get('https://api.spotify.com/v1/audio-features/' + trackId1, headers=headers)
        track1_Charact_Text = json.loads(track1_Charact.text)
        danceLevel1 = float(track1_Charact_Text['danceability'])
        liveLevel1 = float(track1_Charact_Text['liveness'])

        track2_Charact = requests.get('https://api.spotify.com/v1/audio-features/' + trackId2, headers=headers)
        track2_Charact_Text = json.loads(track2_Charact.text)
        danceLevel2 = float(track2_Charact_Text['danceability'])
        liveLevel2 = float(track2_Charact_Text['liveness'])

        averageDance = round((danceLevel0 + danceLevel1 + danceLevel2) / 3, 3)
        averageLive = round((liveLevel0 + liveLevel1 + liveLevel2) / 3, 3)
       

        return render_template('testanalytics.html', track0_Name=trackName0, track1_Name=trackName1, track2_Name=trackName2, averageDanceability=averageDance, averageLiveness=averageLive)
    else:
        return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
