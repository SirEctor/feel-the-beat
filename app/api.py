import flask
from flask import request, jsonify
from datetime import datetime
from . import app
from .table_datatypes import *
import json

@app.route('/api/daily-record', methods=['POST'])
def request_daily_record():
    request_data = json.loads(request.json)
    if not request_data:
        return "Bad Request", 400
    user_id = request_data["user_id"]
    date = request_data["date"]
    json_return = {}
    json_return["name"] = None
    json_return["artist"] = None
    json_return["mood"] = None
    
    if request_data:
        if 'user_id' and 'date' in request_data:
            datetime_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            record = Daily_Record.query.filter_by(user_id=user_id, date=datetime_date).first()
            if not record:
                return None
            uri = record.song_uri
            days_song = Song.query.filter_by(uri=uri).first()
            json_return["name"] = days_song.name
            json_return["artist"] = days_song.artist
            json_return["mood"] = record.mood

            return flask.jsonify(json_return)
            
    return "Bad Request", 400

