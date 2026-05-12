import pandas as pd
import numpy as np
import ast
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =========================
# 1. LOAD DATA
# =========================
movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# =========================
# 2. MERGE DATA
# =========================
movies = movies.merge(credits, on='title')

# =========================
# 3. SELECT USEFUL COLUMNS
# =========================
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# =========================
# 4. CLEAN DATA
# =========================
movies.dropna(inplace=True)

# =========================
# 5. HELPER FUNCTIONS
# =========================
def convert(text):
    L = []
    for i in ast.literal_eval(text):
        L.append(i['name'])
    return L

def get_cast(text):
    L = []
    for i in ast.literal_eval(text)[:3]:
        L.append(i['name'])
    return L

def get_director(text):
    L = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            L.append(i['name'])
    return L

# =========================
# 6. APPLY TRANSFORMATIONS
# =========================
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)
movies['cast'] = movies['cast'].apply(get_cast)
movies['crew'] = movies['crew'].apply(get_director)

# =========================
# 7. TEXT PREPROCESSING
# =========================
movies['overview'] = movies['overview'].apply(lambda x: x.split())

# remove spaces in names (important)
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

# =========================
# 8. CREATE TAGS
# =========================
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id','title','tags']]

# convert list → string
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())

# =========================
# 9. VECTORIZATION
# =========================
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

# =========================
# 10. SIMILARITY
# =========================
similarity = cosine_similarity(vectors)

# =========================
# 11. SAVE FILES
# =========================
pickle.dump(new_df, open('movies.pkl','wb'))
pickle.dump(similarity, open('similarity.pkl','wb'))

print("✅ Training completed. Files saved!")