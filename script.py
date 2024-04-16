import pandas as pd
import requests
import pickle
import time

df = pd.DataFrame(columns=['id', 'title','genre', 'original_language', 'overview', 'popularity', 'release_date', 'vote_average', 'vote_count'])

# Your request
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&vote_average.gte=6&with_original_language=tr"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer ***YOUR ACCSESS TOKEN AUTH***"
}

response = requests.get(url, headers=headers)
response =  response.json()

total_pages = response['total_pages']

genres_url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
genres_response =  requests.get(genres_url, headers=headers).json()

def genre_transformer(genre_ids):
    id_names=[]
    for find_genre in genres_response['genres']:
        for ids in genre_ids:
            if ids == find_genre['id']:
                id_names.append(find_genre['name'])
                
    id_names =', '.join(id_names)
    return id_names


for page in range(1,total_pages+1):
    
    #Your Request
    response = requests.get(f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&vote_average.gte=6&with_original_language=tr', headers=headers)
    data = response.json()
    
    for movie in data['results']:
        
        #Filters
        if movie['overview'] == "":
            continue
        elif movie['vote_count'] < 25:
            continue
        
        movie_info = {
            'id': movie['id'],
            'title': movie['original_title'],
            'genre': genre_transformer(movie['genre_ids']),
            'original_language': movie['original_language'],
            'overview': movie['overview'],
            'popularity': movie['popularity'],
            'release_date': movie['release_date'],
            'vote_average': movie['vote_average'],
            'vote_count': movie['vote_count']
        }
        df = df._append(movie_info, ignore_index=True)
        
    print(df)    
    time.sleep(0.5)


pickle.dump(df, open('your_doc_name.pkl', 'wb'))

