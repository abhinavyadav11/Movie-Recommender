import streamlit as st
import pandas as pd
import pickle
import requests
import os

def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(destination, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        st.error("Error downloading the file from Google Drive.")

# Check if file exists, and if not, download it
file_path = 'movie-recommend-dict.pkl'
if not os.path.exists(file_path):
    download_file_from_google_drive('1TZ9T5NiBwj0fBsu8HFBnb3xFbroEUspZ', file_path)

# Load the data after downloading
movies_dict = pickle.load(open(file_path, 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

option = st.selectbox('Choose a movie', movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(option)
    for i in recommendations:
        st.write(i)
