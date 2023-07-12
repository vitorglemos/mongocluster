
import shutup;
shutup.please()

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
import concurrent.futures
import time
from bs4 import BeautifulSoup
import json
import base64
path = 'C:/PROJETO GERENCIA DE DADOS/JSON_FILES'


list_isrc = pd.read_csv(r'C:\PROJETO GERENCIA DE DADOS\ISRCS CONSULTA.csv')['isrc'].to_list()
list_genres = pd.read_csv(r'C:\PROJETO GERENCIA DE DADOS\GENEROS CONSULTA.csv')['genres'].to_list()

def get_tracks_genres(isrc=None, second=None):
    global list_genres

    clientId = ["Id_1","Id_2","Id_3","Id_4","Id_5","Id_6","Id_7","Id_8","Id_9","Id_10","Id_11","Id_12","Id_13","Id_14","Id_15","Id_16","Id_17","Id_18","Id_19","Id_20"]
    clientSecret = ["Secret_1","Secret_2","Secret_3","Secret_4","Secret_5","Secret_6","Secret_7","Secret_8","Secret_9","Secret_10","Secret_11","Secret_12","Secret_13","Secret_14","Secret_15","Secret_16","Secret_17","Secret_18","Secret_19","Secret_20"]
            
    vetor = []
    try:
        count1 = 0
        while count1 < len(list_genres):
            while True:
                count = 0
                while count < len(clientId):
                    url = "https://accounts.spotify.com/api/token"
                    headers = {}
                    data = {}

                    encode = base64.b64encode(f"{clientId[count]}:{clientSecret[count]}".encode('ascii')).decode('ascii')
                    headers['Authorization'] = f"Basic {encode}"
                    data['grant_type'] = "client_credentials"
                    r = requests.post(url, headers=headers, data=data)
                    token = r.json()['access_token']
                    headers = {"Authorization": "Bearer " + token,
                    "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            
                    url_get_track = "https://api.spotify.com/v1/search?query=genre%3A"+list_genres[count1]+"+isrc%3A"+isrc+"&type=track&market=BR&locale=pt-BR%2Cpt%3Bq%3D0.9%2Cen-US%3Bq%3D0.8%2Cen%3Bq%3D0.7&offset=0&limit=50"
                    html =  session.get(url=url_get_track, headers=headers, timeout=5).content
                    soup = json.loads(BeautifulSoup(html, 'html.parser').text)
                    soup['genre_track'] = list_genres[count1]
                    vetor.append(soup)
                    
                    count = count + 1
                    count1 = count1 + 1
                    time.sleep(second)
    except:
        pass
    
    with open (path + "\\" + str(isrc) + ".json", "w", encoding="utf-8") as jsonfile:
        json.dump(vetor, jsonfile, ensure_ascii=False)

second = 10
with concurrent.futures.ThreadPoolExecutor(max_workers=len(list_isrc)) as executor:
    executor.map(get_tracks_genres, list_isrc, [second for i in list_isrc])


