from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout

from django.contrib import messages

from .models import Movie, Like

from .ml_model import recommend, recommend_for_user

from django.http import JsonResponse

from .ml_model import movies,fetch_poster,fetch_trailer

from .models import Watchlist

import requests



def trending(request):

    response = requests.get(

        'https://api.themoviedb.org/3/trending/movie/day?api_key=cc2d1357cd9468cd1d8ef53e36305602&language=en-US')

    data = response.json()



    movies_list = []



    for m in data['results'][:12]:

        movies_list.append({

            "title": m['title'],

            "poster": "https://image.tmdb.org/t/p/w500" + m['poster_path'],

            "id": m['id']

        })



    return render(request, 'trending.html', {'movies': movies_list})



@login_required

def add_to_watchlist(request, movie_id, title):



    Watchlist.objects.get_or_create(

        user=request.user,

        movie_id=movie_id,

        title=title

    )



    return redirect('watchlist')





@login_required

def watchlist(request):



    items = Watchlist.objects.filter(user=request.user)



    movies = []



    for item in items:

        movies.append({

            "movie_id": item.movie_id,

            "title": item.title,

            "poster": fetch_poster(item.movie_id),

            "trailer": fetch_trailer(item.movie_id)

        })



    return render(request, 'watchlist.html', {'movies': movies})



@login_required

def remove_from_watchlist(request, movie_id):

    try:

        item = Watchlist.objects.get(user=request.user, movie_id=movie_id)

        item.delete()

        messages.success(request, 'Movie removed from watchlist!')

    except Watchlist.DoesNotExist:

        messages.error(request, 'Movie not found in your watchlist.')


    return redirect('watchlist')



def movie_detail(request, movie_id):



    API_KEY = "YOUR_TMDB_API_KEY"



    response = requests.get(

        'http://api.themoviedb.org/3/movie/{}?api_key=cc2d1357cd9468cd1d8ef53e36305602&language=en-US'.format(

            movie_id))

    data = response.json()



    context = {

        "movie_id": movie_id,

        "title": data.get("title"),

        "overview": data.get("overview"),

        "rating": data.get("vote_average"),

        "year": str(data.get("release_date", ""))[:4],

        "poster": "https://image.tmdb.org/t/p/w500" + data.get("poster_path", ""),

    }



    return render(request, "movie_detail.html", context)



def autocomplete(request):

    query = request.GET.get('q', '')



    if query:

        results = movies[movies['title'].str.lower().str.contains(query.lower())]['title'].head(7)

        suggestions = list(results)

    else:

        suggestions = []



    return JsonResponse(suggestions, safe=False)



def home(request):

    return render(request, 'home.html')





def signup(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'User registered successfully! Please login.')

            return redirect('login')

    return render(request, 'signup.html', {'form': form})





def recommend_view(request):

    movie = request.GET.get('movie')



    if not movie:

        return redirect('home')



    results = recommend(movie)



    return render(request, 'recommend.html', {'movies': results})







@login_required

def user_recommendations(request):



    likes = Like.objects.filter(user=request.user)



    liked_movies = [like.movie.title for like in likes]



    recommended_titles = recommend_for_user(liked_movies)



    results = []



    for title in recommended_titles:

        try:

            row = movies[movies['title'] == title].iloc[0]

            movie_id = row['movie_id']



            results.append({

                "title": title,

                "poster": fetch_poster(movie_id),

                "trailer": fetch_trailer(movie_id)

            })

        except:

            continue



    return render(request, 'user_recommend.html', {

        'movies': results

    })



@login_required

def like_movie(request, movie_id):

    movie_row = movies[movies['movie_id'] == movie_id]



    if movie_row.empty:

        return redirect('home')



    title = movie_row.iloc[0]['title']



    movie_obj, created = Movie.objects.get_or_create(

        movie_id=movie_id,

        defaults={'title': title, 'poster': ''}

    )



    Like.objects.get_or_create(user=request.user, movie=movie_obj)



    return redirect('home')



def user_logout(request):

    logout(request)

    return redirect('login')