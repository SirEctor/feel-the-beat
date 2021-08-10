from flask import Flask, render_template, request, flash, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import sqlite3 as sql
import requests
import json 
from . import db
import os
from app.db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import urllib.parse


load_dotenv()
app = Flask(__name__)
app.secret_key = "test"

db.init_app(app)


@app.route('/')
def home():
    return render_template('index.html')
	
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')
    
@app.route('/add_user', methods= ['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        uname = request.form.get('uname')
        psw = request.form.get('psw')
        db = get_db()
        cur = db.cursor()
        msg = None

        if not uname:
            msg = 'Username is required.'
        elif not psw:
            msg = 'Password is required.'
        elif db.execute(
            'SELECT id FROM users WHERE username = ?', (uname,)
        ).fetchone() is not None:
            msg = f"User {uname} is already registered."

        if not msg:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (uname, generate_password_hash(psw))
            )
            db.commit()
            msg = f"User {uname} created successfully"
            
            return render_template("userauth.html")        
        flash(msg)
        return render_template("register.html")

@app.route('/confirm_login', methods= ['POST'])
def confirm_login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        psw = request.form.get('psw')
        db = get_db()
        cur = db.cursor()
        msg = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (uname,)
        ).fetchone()

        if user is None:
            msg = 'Incorrect username.'
        elif not check_password_hash(user['password'], psw):
            msg = 'Incorrect password.'

        if not msg:
            msg = "Login Successful"
            return render_template(url_for("dashboard"))
        flash(msg)
        return render_template("login.html")

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
    print("S!")
    print(s)
    return render_template('testanalytics.html', recentlyplayed=s)

@app.route('/userauth')
def userauth():
    return render_template('userauth.html')

@app.route('/dashboard')
def dashboard():
    return "Dashboard should be implemented here shortly. Come again soon."

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
