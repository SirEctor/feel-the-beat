from flask import render_template
from flask_login import current_user
import requests
import json
from . import db

import datetime as dt
from .table_datatypes import *


def get_all_analytics(access_token):
    """
    Retrieves the last three played songs of a user and calculates the
    average danceability and liveness of these songs.
    Input:
        access_token (string): used to access user-specific data from the
            Spotify API
    Returns:
        storage (dict): maps labels about user-specific data to their values, ex.
            storage[average_dance] = average danceability of three last played songs
    """
    storage = {}

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    # Get recently reproduces tracks
    resTracks = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=3", headers=headers
    )
    resTracks_Text = json.loads(resTracks.text)

    trackN0 = resTracks_Text["items"][0]["track"]["name"]
    trackArtist0 = resTracks_Text["items"][0]["track"]["album"]["artists"][0]["name"]
    trackName0 = trackN0 + "  -  " + trackArtist0
    trackId0 = resTracks_Text["items"][0]["track"]["id"]

    storage["trackName0"] = trackName0

    trackN1 = resTracks_Text["items"][1]["track"]["name"]
    trackArtist1 = resTracks_Text["items"][1]["track"]["album"]["artists"][0]["name"]
    trackName1 = trackN1 + "  -  " + trackArtist1
    trackId1 = resTracks_Text["items"][1]["track"]["id"]

    storage["trackName1"] = trackName1

    trackN2 = resTracks_Text["items"][2]["track"]["name"]
    trackArtist2 = resTracks_Text["items"][2]["track"]["album"]["artists"][0]["name"]
    trackName2 = trackN2 + "  -  " + trackArtist2
    trackId2 = resTracks_Text["items"][2]["track"]["id"]

    storage["trackName2"] = trackName2

    # Get Audio Features for a Track
    track0_Charact = requests.get(
        "https://api.spotify.com/v1/audio-features/" + trackId0, headers=headers
    )
    track0_Charact_Text = track0_Charact.text.json()
    danceLevel0 = float(track0_Charact_Text["danceability"])
    liveLevel0 = float(track0_Charact_Text["liveness"])

    track1_Charact = requests.get(
        "https://api.spotify.com/v1/audio-features/" + trackId1, headers=headers
    )
    track1_Charact_Text = track1_Charact.text.json()
    danceLevel1 = float(track1_Charact_Text["danceability"])
    liveLevel1 = float(track1_Charact_Text["liveness"])

    track2_Charact = requests.get(
        "https://api.spotify.com/v1/audio-features/" + trackId2, headers=headers
    )
    track2_Charact_Text = track2_Charact.text.json()
    danceLevel2 = float(track2_Charact_Text["danceability"])
    liveLevel2 = float(track2_Charact_Text["liveness"])

    average_dance = round((danceLevel0 + danceLevel1 + danceLevel2) / 3, 3)
    average_live = round((liveLevel0 + liveLevel1 + liveLevel2) / 3, 3)

    storage["average_dance"] = average_dance
    storage["average_live"] = average_live

    return storage


def get_5_latest_songs(access_token):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }

    # Get recently reproduces tracks
    resTracks = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=5", headers=headers
    )
    resTracks_Text = resTracks.json()

    tracks = []
    for i in range(5):
<<<<<<< HEAD
        song_uri = resTracks_Text["items"][i]["track"]["album"]["artists"][0]["uri"]
        song_name = resTracks_Text["items"][i]["track"]["name"]
        song_artist = resTracks_Text["items"][i]["track"]["album"]["artists"][0]["name"]
=======
        song_uri = resTracks_Text["items"][i]["track"]["uri"]
        song_name = resTracks_Text['items'][i]['track']['name']
        song_artist = resTracks_Text['items'][i]['track']['album']['artists'][0]['name']
>>>>>>> 6c4d08ec0cdf9d6b7d62ad92979a933eeaad34a5
        song_name_and_artist = song_name + " - " + song_artist
        if not Song.query.filter_by(uri=song_uri).first():
            new_song = Song(uri=song_uri, name=song_name, artist=song_artist)
            db.session.add(new_song)
            db.session.commit()
        tracks.append(song_name_and_artist)
        tracks.append(song_uri)
    t = dt.date.today().strftime("%a, %B %d %Y")
    tracks.append(t)
    return tracks

<<<<<<< HEAD

def error_handling(r, type):
    if r.status_code == 200:
        r_text = r.json()
        access_token = r_text["access_token"]
        if type == "test_analytics":
            refresh_token = r_text["refresh_token"]
            current_user.set_refresh_token(refresh_token)
            db.session.commit()

=======
def error_handling(r):
    if r.status_code == 200:
        r_text = r.json()
        access_token = r_text['access_token']            
>>>>>>> 6c4d08ec0cdf9d6b7d62ad92979a933eeaad34a5
        storage = get_5_latest_songs(access_token)
        return render_template(
            "dashboard.html",
            track0_Name=storage[0],
            song_uri_0=storage[1],
            track1_Name=storage[2],
            song_uri_1=storage[3],
            track2_Name=storage[4],
            song_uri_2=storage[5],
            track3_Name=storage[6],
            song_uri_3=storage[7],
            track4_Name=storage[8],
            song_uri_4=storage[9],
            tday=storage[10],
        )
    return render_template("result.html")
