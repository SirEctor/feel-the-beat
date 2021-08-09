import requests
import json 

def getToken(cId, secret, jsV):
    data = {'client_id': cId, 
            'client_secret': secret, 
            'grant_type':'authorization_code',
            'code':jsV,
            'redirect_uri':'http://localhost:5000/'
            }
    return requests.post('https://accounts.spotify.com/api/token',data=data)
    
def recentlyPlayed(s):
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
    
    response = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=1',headers=headers)
    s = json.loads(response.text)
    sItems = s['items']
    sTrack = sItems[0]['track']

    sAlbum = sTrack['album']
    sAT = sAlbum['album_type']
    name = sTrack['name']
    sId = sTrack['id']
    
    return(name)
