import argparse
import json
from pymongo import MongoClient

import sys
import codecs

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
 
spotify_id = ""  #INSERIR SPOTIFY ID DEV
spotify_secret = "" #INSERIR SPOTIFY SECRET

client_credentials_manager = SpotifyClientCredentials(spotify_id, spotify_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_query_filter(start_index, end_index):
    pipeline = [
	    { "$match": { "tracks.items": { "$ne": [], "$exists": True }}},
	    { "$match": { "tracks.items.external_ids.isrc" : {"$in": ['BC3PG2205040', 'BC7OL2200001', 'BC9IN2200001', 'BCA6L2200175', 'BCIH82206047', 'BCNWM2100036', 'BCNWM2100068', 'BCPAW2200089', 'BCQAL2200023', 'BCTOE2200106', 'BCVK92200525', 'BR7N61500091', 'BR9T62200043', 'BRDEP0500255', 'BRE1K1300027', 'BREHZ0300018', 'BRGRV0501290', 'BROOD2200015', 'BRSME0000066', 'BRSME2200168', 'BRWMB0500707', 'BX12K2200031', 'BX3662000014', 'BX46W2200004', 'BX7O92100005', 'BXGFC2200010', 'BXGHW2200026', 'BXIV82278674', 'BXIV82292942', 'BXKG22200985', 'BXQWK2200023', 'BXT8R2200016', 'FR10S1688247', 'FR9W12230802', 'GBDKA0300194', 'GBK3W2202199', 'GBK3W2202206', 'GBUM72206569', 'KRA381700694', 'NL5WB2200065', 'NLA322200096', 'QZEQU2222769', 'QZGLM2005681', 'QZGLS2176681', 'QZGLS2241991', 'QZHZ32181290', 'QZMEM2293178', 'QZTPX2255536', 'QZTPX2258886', 'QZTPX2299595', 'QZTVM2248333', 'USGES1611005', 'USUG12204635', 'USUG12206834', 'USUM72218110']}}},
	    { "$unwind": "$tracks.items" },
	    {
		"$group": {
		    "_id": "$tracks.items.external_ids.isrc",
		    "popularity": { "$first": "$tracks.items.popularity" },
		    "track_name": { "$first": "$tracks.items.name" },
		    "artist_name": { "$first": "$tracks.items.artists.name" },
		    "artist_id": { "$first": "$tracks.items.artists.id" },
		    "genre": { "$addToSet": "$genre_track" }
		}
	    },
	    {
		"$project": {
		    "_id": 0,
		    "isrc": "$_id",
		    "popularity": 1,
		    "track_name": 1,
		    "genre": 1,
		    "artist_id": { "$arrayElemAt": ["$artist_id", 0]},
		    "artist_name": { "$arrayElemAt": ["$artist_name", 0]}
		}
	    },
	    { "$sort": { "popularity": -1 }},
	    { "$skip": start_index },
	    { "$limit": end_index - start_index}]

    return pipeline
    
def get_query_full(start_index, end_index):
    pipeline = [
	    { "$match": { "tracks.items": { "$ne": [], "$exists": True }}},
	    { "$unwind": "$tracks.items" },
	    {
		"$group": {
		    "_id": "$tracks.items.external_ids.isrc",
		    "popularity": { "$first": "$tracks.items.popularity" },
		    "track_name": { "$first": "$tracks.items.name" },
		    "artist_name": { "$first": "$tracks.items.artists.name" },
		    "artist_id": { "$first": "$tracks.items.artists.id" },
		    "genre": { "$addToSet": "$genre_track" }
		}
	    },
	    {
		"$project": {
		    "_id": 0,
		    "isrc": "$_id",
		    "popularity": 1,
		    "track_name": 1,
		    "genre": 1,
		    "artist_id": { "$arrayElemAt": ["$artist_id", 0]},
		    "artist_name": { "$arrayElemAt": ["$artist_name", 0]}
		}
	    },
	    { "$sort": { "popularity": -1 }},
	    { "$skip": start_index },
	    { "$limit": end_index - start_index}]

    return pipeline
	 
	    
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer)

def realizar_consulta(inicio, fim, type_query):
    client = MongoClient('localhost', 27017, username='admin', password='admin')
    db = client['spotify']
    collection = db['Spotifyv3']
    if type_query == 0:
    	pipeline = get_query_filter(inicio, fim)
    else:
    	pipeline = get_query_full(inicio, fim)
    documents = collection.aggregate(pipeline)
    return documents

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Consulta mongo")
    parser.add_argument("--inicio", type=int)
    parser.add_argument("--fim", type=int)
    parser.add_argument("--genre", type=int)
    parser.add_argument("--type", type=int)
    
    args = parser.parse_args()
    inicio = args.inicio
    fim = args.fim
    genre = args.genre
    type_query = args.type

    resultado = realizar_consulta(inicio, fim, type_query)
    total = 0
    for document in resultado:
        data_spotify = dict(document)
        if genre:
            artist_id = data_spotify["artist_id"]
            artist_genre = sp.artists([artist_id])
            artist_genre = artist_genre["artists"][0]["genres"]
            
            data_spotify["artist_genres"] = artist_genre
        
        
        print(json.dumps(data_spotify, indent=4))
        total += 1
           

