Movie Recommendation System

This is a simple movie recommendation system that suggests movies based on user preferences. It uses The Movie Database (TMDb) API to fetch movie data and implements content-based filtering to recommend movies either similar to a given movie or within a specified genre.

Table of Contents

Features
Prerequisites
Installation
Configuration
Usage
Functions Explained
Attribution
License
Features

Fetches popular and top-rated movies from TMDb.
Recommends movies based on:
Similarity to a user-provided movie.
User-specified genre.
Enhances recommendations using movie overviews and keywords.
Simple command-line interface for user interaction.
Prerequisites

Python 3.6 or higher
TMDb API Key (free to obtain)
Installation

Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/movie-recommendation-system.git
cd movie-recommendation-system
Create a Virtual Environment (Optional but Recommended)
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
Install Required Packages
bash
Copy code
pip install -r requirements.txt
If requirements.txt is not provided, install the packages manually:

bash
Copy code
pip install tmdbv3api pandas scikit-learn
Obtain a TMDb API Key
Sign up for a free account at TMDb.
Navigate to your account settings and obtain your API key.
Configuration

Set Your TMDb API Key
In the script, locate the following line:

python
Copy code
tmdb.api_key = 'YOUR_TMDB_API_KEY'
Replace 'YOUR_TMDB_API_KEY' with your actual TMDb API key:

python
Copy code
tmdb.api_key = 'your_actual_api_key_here'
Important: Keep your API key secure. Do not share it publicly or commit it to version control systems.
Adjust the Number of Pages to Fetch (Optional)
The script fetches movie data from multiple pages. Each page contains up to 20 movies.

python
Copy code
movies_df = get_combined_movie_list(pages=2)  # Fetches up to 80 movies
Increase the pages parameter to fetch more movies:

python
Copy code
movies_df = get_combined_movie_list(pages=5)  # Fetches up to 200 movies
Note: Fetching more pages increases the number of API requests. Be mindful of TMDb's API rate limits.
Usage

Run the Script
bash
Copy code
python movie_recommendation.py
Follow the Prompts
The script will list the fetched movie titles.
Choose whether you want a recommendation based on a movie or a genre:
vbnet
Copy code
Would you like a recommendation based on previously watched movies or by genre? m/g
> m
If you choose movie-based recommendation:
markdown
Copy code
What was the last movie you saw:
> Inception
The script will display movies similar to "Inception".
If you choose genre-based recommendation:
markdown
Copy code
What genre would you like:
> Action
The script will display top-rated movies in the "Action" genre.
View Recommendations
The script will display a list of recommended movies based on your input.

markdown
Copy code
Movies similar to 'Inception':
1. Interstellar
2. The Matrix
3. The Prestige
...
Functions Explained

1. get_genre_name(genre_id)
Converts TMDb genre IDs to genre names using a predefined dictionary.

2. get_popular_movies(pages=5)
Fetches popular movies from TMDb over a specified number of pages. Collects movie data including title, year, rating, genres, overview, and keywords.

3. get_top_rated_movies(pages=5)
Fetches top-rated movies from TMDb over a specified number of pages. Similar to get_popular_movies.

4. get_movie_keywords(movie_id)
Fetches keywords associated with a movie using its TMDb ID.

5. get_combined_movie_list(pages=5)
Combines popular and top-rated movies into a single DataFrame, removing duplicates.

6. create_enhanced_similarity_matrix(df)
Creates a cosine similarity matrix using combined features of genres, overviews, and keywords.

7. recommend_movies(movie_title, similarity_matrix, movies_df, top_n=10)
Recommends movies similar to a provided movie title based on the similarity matrix.

8. recommend_movies_by_genre(genre, movies_df, top_n=10)
Recommends top-rated movies within a specified genre.

Attribution

This product uses the TMDb API but is not endorsed or certified by TMDb.

TMDb API: https://www.themoviedb.org/documentation/api
TMDb Terms of Use: https://www.themoviedb.org/terms-of-use
License

This project is licensed under the MIT License - see the LICENSE file for details.
