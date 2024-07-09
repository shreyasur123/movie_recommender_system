import streamlit as st
import pandas as pd
import requests

TMDB_API = "3db83fa7c4e6f2ff29e56e620e05f4d3"


# headers = {
#     "accept": "application/json",
#     "Authorization": "Bearer 3db83fa7c4e6f2ff29e56e620e05f4d3"
# }


def fetch_poster(movie_id):
    params = {
        "api_key": TMDB_API,
        "language": "en-Us"
    }
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?", params=params)
    fetched_poster_path = response.json()["poster_path"]
    complete_poster_path = "https://image.tmdb.org/t/p/original" + fetched_poster_path
    # print(complete_poster_path)
    return complete_poster_path


# print(fetch_poster('19995'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    sorted_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in sorted_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from id
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies = pd.read_pickle('movies.pkl')
movies_list = movies['title'].values

similarity = pd.read_pickle('similarity.pkl')
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Which movie have you already watched?",
    movies_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text((names[1]))
        st.image(posters[1])

    with col3:
        st.text((names[2]))
        st.image(posters[2])

    with col4:
        st.text((names[3]))
        st.image(posters[3])

    with col5:
        st.text((names[4]))
        st.image(posters[4])
