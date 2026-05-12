import pickle
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

movies_path = os.path.join(BASE_DIR, 'movies.pkl')
similarity_path = os.path.join(BASE_DIR, 'similarity.pkl')

movies = pickle.load(open(movies_path, 'rb'))
similarity = pickle.load(open(similarity_path, 'rb'))

def fetch_poster(movie_id):
    response = requests.get(
        'http://api.themoviedb.org/3/movie/{}?api_key=cc2d1357cd9468cd1d8ef53e36305602&language=en-US'.format(
            movie_id))
    data = response.json()
    print(data)
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

def fetch_trailer(movie_id):
    response = requests.get(
        'http://api.themoviedb.org/3/movie/{}/videos?api_key=cc2d1357cd9468cd1d8ef53e36305602&language=en-US'.format(
            movie_id))
    data = response.json()

    results = data.get("results", [])

    for video in results:
        if video["type"] == "Trailer" and video["site"] == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        results.append({
            'title': movies.iloc[i[0]].title,
            'poster': fetch_poster(movie_id),
            'movie_id': movie_id
        })

    return results


def recommend_for_user(liked_movies):
    recommended = set()

    for movie in liked_movies:
        try:
            index = movies[movies['title'] == movie].index[0]
            distances = similarity[index]

            movie_list = sorted(list(enumerate(distances)),
                                reverse=True, key=lambda x: x[1])[1:4]

            for i in movie_list:
                recommended.add(movies.iloc[i[0]].title)
        except:
            continue

    return list(recommended)[:10]