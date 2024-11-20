import streamlit as st
import requests
import pickle
import pandas as pd

# URL of the file in the GitHub release
file_url = "https://github.com/abhinavyadav11/Movie-Recommender/releases/download/v1.0/similarity.pkl"

# Function to download the file
def download_file(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return True
    return False

# Download the similarity.pkl file
if download_file(file_url, 'similarity.pkl'):
    st.write("File downloaded successfully!")

    # Load the file using pickle
    with open('similarity.pkl', 'rb') as file:
        similarity = pickle.load(file)

    st.write("File loaded and ready to use!")
else:
    st.error("Failed to download the file.")

# Load the movie dictionary and create the DataFrame
movies_dict = pickle.load(open('movie-recommend-dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Streamlit interface
st.title('Movie Recommender System')

# Selectbox for choosing a movie
option = st.selectbox('Choose a movie', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    recommendations = recommend(option)
    for i in recommendations:
        st.write(i)
