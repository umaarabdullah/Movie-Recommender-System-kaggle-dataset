import streamlit as st
import pickle
import pandas as pd
import requests

API_KEY = 'd1facc4d5f50444e9ca0fd7f3dc22d0a'

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US'.format(movie_id, API_KEY))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

# Function to recommend movies based on similarity
def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    # Use enumerate to remember indexes and select 5 most similar movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']  # Fixed indexing here
        recommended_movies.append(movies.iloc[i[0]]['title'])  # Fixed indexing here
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
def load_data():
    with open('movies_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    
    return movies, similarity

# Main function
def main():
    # Load data
    movies, similarity = load_data()

    # Streamlit UI
    st.title('Movie Recommender System')

    selected_movie_option = st.selectbox(
        'Movie Titles',
        movies['title'].values
    )

    if st.button('Recommend'):
        movie_recommend_names, movie_recommend_posters = recommend(selected_movie_option, movies, similarity)

        num_cols = len(movie_recommend_names)
        cols = st.columns(num_cols)
        for i in range(num_cols):
            with cols[i]:
                st.text(movie_recommend_names[i])
                st.image(movie_recommend_posters[i])

if __name__ == "__main__":
    main()
