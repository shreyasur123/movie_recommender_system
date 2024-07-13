import streamlit as st
import pandas as pd
import requests
import gdown
import pickle
import os

TMDB_API = "3db83fa7c4e6f2ff29e56e620e05f4d3"


@st.cache_resource
def load_similarity():
    # ID of your file from Google Drive link
    file_id = '1ISsG7BM5M6jr6ZtbEI0fYsF4LBe_-6X7'

    # Destination path
    output = 'similarity.pkl'

    # Download the file if it doesn't exist
    if not os.path.exists(output):
        gdown.download(f'https://drive.google.com/uc?id={file_id}', output, quiet=False)

    # Load the similarity matrix
    with open(output, 'rb') as f:
        similarity = pickle.load(f)

    return similarity


def fetch_poster(movie_id):
    params = {
        "api_key": TMDB_API,
        "language": "en-Us"
    }
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?", params=params)
    fetched_poster_path = response.json()["poster_path"]
    complete_poster_path = "https://image.tmdb.org/t/p/original" + fetched_poster_path
    return complete_poster_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    sorted_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in sorted_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load movies dataframe
movies = pd.read_pickle('movies.pkl')
movies_list = movies['title'].values

# Load similarity matrix
similarity = load_similarity()

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Which movie have you already watched?",
    movies_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    for col, name, poster in zip([col1, col2, col3, col4, col5], names, posters):
        with col:
            st.text(name)
            st.image(poster)
