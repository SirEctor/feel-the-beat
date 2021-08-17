import requests
import json

def get_all_analytics(access_token):
    '''
    Retrieves the last three played songs of a user and calculates the 
    average danceability and liveness of these songs.

    Input: 
        access_token (string): used to access user-specific data from the 
            Spotify API

    Returns:
        storage (dict): maps labels about user-specific data to their values, ex.
            storage[average_dance] = average danceability of three last played songs
    '''
    storage = {}
    
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

    
    storage['trackName0'] = trackName0
    
    trackN1 = resTracks_Text['items'][1]['track']['name']
    trackArtist1 = resTracks_Text['items'][1]['track']['album']['artists'][0]['name']
    trackName1 = trackN1 + "  -  " + trackArtist1
    trackId1 = resTracks_Text['items'][1]['track']['id']

    storage['trackName1'] = trackName1

    trackN2 = resTracks_Text['items'][2]['track']['name']
    trackArtist2 = resTracks_Text['items'][2]['track']['album']['artists'][0]['name']
    trackName2 = trackN2 + "  -  " + trackArtist2
    trackId2 = resTracks_Text['items'][2]['track']['id']

    storage['trackName2'] = trackName2

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

    average_dance = round((danceLevel0 + danceLevel1 + danceLevel2) / 3, 3)
    average_live = round((liveLevel0 + liveLevel1 + liveLevel2) / 3, 3)

    storage['average_dance'] = average_dance
    storage['average_live'] = average_live
    
    return storage