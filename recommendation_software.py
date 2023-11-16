import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Define a function that fetches the top 100 movies from a given IMDb list URL
def get_top_100_movies(url):
    # Send a GET request to the given URL and retrieve the response content
    response = requests.get(url)
    
    # Parse the response content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Create an empty list to store movie data
    movie_data = []
    
    # Find all movie containers on the page
    movie_containers = soup.find_all('div', class_='lister-item-content')
    
    # Loop through each movie container and extract relevant data
    for movie in movie_containers:
        title = movie.find('h3', class_='lister-item-header').find('a').text
        year = movie.find('span', class_='lister-item-year').text.strip('()')
        rating = float(movie.find('div', class_='ipl-rating-star').find('span', class_='ipl-rating-star__rating').text)

        genres = movie.find('span', class_='genre').text.strip().replace(', ', '|')
        
        # Add the movie data to the list
        movie_data.append({
            'title': title,
            'year': year,
            'rating': rating,
            'genres': genres
        })
    
    # Return the list of movie data
    return movie_data

# Define the URL for the IMDb top 100 movies list
url = 'https://www.imdb.com/list/ls055592025/'

# Call the get_top_100_movies function to retrieve the movie data and store it in a list
movie_data = get_top_100_movies(url)

# Convert the movie data list to a Pandas DataFrame
movies_df = pd.DataFrame(movie_data)


# Define a function that creates a similarity matrix based on movie genres
def create_similarity_matrix(df):
    # Create a vectorizer to count the frequency of words in the genres column
    vectorizer = CountVectorizer()
    
    # Transform the genres column into a matrix of word counts
    genre_matrix = vectorizer.fit_transform(df['genres'])

    # Compute the cosine similarity of the genre matrix
    cosine_sim = cosine_similarity(genre_matrix, genre_matrix)
    
    # Return the similarity matrix
    return cosine_sim

# Call the create_similarity_matrix function to create a similarity matrix for the movies DataFrame
similarity_matrix = create_similarity_matrix(movies_df)


def recommend_movies(movie_title, similarity_matrix, movies_df, top_n=10):
    # Check if the movie exists in the dataset
    if movie_title not in movies_df['title'].values:
        return f"The movie '{movie_title}' was not found in the dataset. Please try another movie."

    # Get the index of the movie
    movie_index = movies_df[movies_df['title'] == movie_title].index[0]

    # Get the similarity scores of all movies with respect to the given movie
    similarity_scores = list(enumerate(similarity_matrix[movie_index]))

    # Sort the similarity scores in descending order
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Remove the watched movie from the similarity scores
    similarity_scores = [(idx, score) for idx, score in similarity_scores if idx != movie_index]

    # Get the indices of the top_n most similar movies
    top_movie_indices = [i[0] for i in similarity_scores[1:top_n + 1]]

    # Return the titles of the top_n most similar movies
    return movies_df['title'].iloc[top_movie_indices]

def recommend_movies_by_genre(genre, movies_df, top_n=10):
    # Filter movies by the specified genre
    filtered_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]

    # Sort the movies by rating in descending order
    sorted_movies = filtered_movies.sort_values(by='rating', ascending=False)

    # Return the top N movies within the specified genre
    return sorted_movies.head(top_n)['title'].reset_index(drop=True)



# Prompts the user if they would like to get a recommendation based on movies or genres
choice = input("Would you like a recommendation based on previously watched movies or by genre? m/g\n>")

if choice == 'm': 
    movie_title = input("What was the last movie you saw: \n>")
    top_n = 10  # Number of recommendations

    # Get the recommended movies
    recommended_movies = recommend_movies(movie_title, similarity_matrix, movies_df, top_n)

    # Display the recommended movies with their correct ranking
    print("Movies similar to  {}".format(movie_title))
    for i, movie in enumerate(recommended_movies, 1):
        print(f"{i}. {movie}")
elif choice == 'g':
    genre = input("What genre would you like: \n>")
    top_n = 10
    recommended_movies = recommend_movies_by_genre(genre, movies_df, top_n)
    length_of_recommended_movies = len(recommended_movies)

    print(f"Top {length_of_recommended_movies} {genre} movies:")
    #print(recommended_movies)
    for i, movie in enumerate(recommended_movies, 1):
        print(f"{i}. {movie}")
else:
    exit()

