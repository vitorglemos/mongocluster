import shutup;
shutup.please()

import os
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
spotify_id = "..." #seu client id no spotify for developers
spotify_secret = "..." #seu client secret no spotify for developers
client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)

data_json = []
path = r'C:\PROJETO GERENCIA DE DADOS\JSON_FILES'
files = os.listdir(path)
files_json = [path + "\\" + i for i in files if i[-4:] == "json"] 
for i in files_json:
    data = json.load(open(i, encoding='utf-8'))
    for i_1 in data:   
        if 'tracks' in i_1 and len(i_1['tracks']['items']) > 0:
            result = i_1['tracks']['items']
            for i_2 in result:
                if i_2['external_ids'].get('isrc','') == i[-17:-5]:
                    dicio = {}
                    dicio['isrc'] = i_2['external_ids'].get('isrc','')
                    dicio['track_id'] = i_2['id']
                    dicio['track_name'] = i_2['name']
                    dicio['album_name'] = i_2['album']['name']
                    dicio['artist_id'] = i_2['artists'][0]['id'] if index_exists(i_2['artists'], 0) else ''
                    dicio['artist_name'] = i_2['artists'][0]['name'][:100] if index_exists(i_2['artists'], 0) else ''
                    dicio['genre_track'] = i_1['genre_track']
                    dicio['audio'] = str(i_2['preview_url'])
                    data_json.append(dicio) 
                    
df_json = pd.DataFrame(data_json)
df = pd.DataFrame({'genres_music': df_json.groupby(['isrc','track_name','artist_id','artist_name','album_name']).apply(lambda group: ', '.join(group['genre_track']))}).reset_index()
df.sort_values(by=['isrc'], inplace=True)
df.reset_index(drop=True)
df['genres_music'] = [list(set(i.split(', '))) for i in df['genres_music']]
df['genres_artist'] = [sp.artists([i])['artists'][0]['genres'] for i in df['artist_id']]
df['tam'] = [len(i) for i in df['genres_music']]
df.sort_values(by=['tam', 'isrc'], inplace=True, ascending=False)
df.drop(columns=["tam", "artist_id"], inplace=True)
df




