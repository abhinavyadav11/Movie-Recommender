import streamlit as st
import pandas as pd
import pickle
import requests
import gdown
import os


# def fetch_poster(movie_id):
#    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265d1679663a7ea12ac168da84d2e8&language=en-US'.format(id))
#    data = response.json()
#    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']



# Download the file from Google Drive if it doesn't exist
file_path = 'similarity.pkl'
if not os.path.exists(file_path):
    url = 'https://drive.google.com/uc?id=1TZ9T5NiBwj0fBsu8HFBnb3xFbroEUspZ'
    gdown.download(url, file_path, quiet=False)

def recommend (movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies  #recommended_poster

movies_dict = pickle.load(open('movie-recommend-dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')


option = st.selectbox('Choose a movie', movies['title'].values)

if st.button('Recommend'):

    recommendations = recommend(option)
    for i in recommendations:
        st.write(i)
