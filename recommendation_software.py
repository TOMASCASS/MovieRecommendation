from tmdbv3api import TMDb, Movie
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time

# Initialize TMDb with your API key
tmdb = TMDb()
# Replace with your actual TMDb API key
tmdb.api_key = 'a80f52582b3095d4b51cf9f2a0980f04'
tmdb.language = 'en'
tmdb.debug = True

movie = Movie()

# Function to fetch popular movies from TMDb


def get_genre_name(genre_id):
    genre_dict = {
        28: 'Action',
        12: 'Adventure',
        16: 'Animation',
        35: 'Comedy',
        80: 'Crime',
        99: 'Documentary',
        18: 'Drama',
        10751: 'Family',
        14: 'Fantasy',
        36: 'History',
        27: 'Horror',
        10402: 'Music',
        9648: 'Mystery',
        10749: 'Romance',
        878: 'Science Fiction',
        10770: 'TV Movie',
        53: 'Thriller',
        10752: 'War',
        37: 'Western'
    }
    return genre_dict.get(genre_id, 'Unknown')

# Function to fetch popular movies from TMDb


def get_popular_movies(pages=5):
    try:
        movie_data = []
        for page in range(1, pages + 1):
            popular_movies = movie.popular(page=page)

            if not popular_movies:
                print(f"No popular movies were retrieved on page {page}.")
                continue  # Skip to the next page

            for m in popular_movies:
                title = m.title or 'N/A'
                year = m.release_date.split(
                    '-')[0] if m.release_date else 'N/A'
                rating = m.vote_average or 0.0
                genre_ids = m.genre_ids or []
                genres = [get_genre_name(genre_id) for genre_id in genre_ids]
                genres_str = "|".join(genres) if genres else 'N/A'
                overview = m.overview or ''
                # Fetch keywords (requires additional API call)
                keywords = get_movie_keywords(m.id)
                keywords_str = " ".join(keywords)
                # Collect movie data
                movie_data.append({
                    'title': title,
                    'year': year,
                    'rating': rating,
                    'genres': genres_str,
                    'overview': overview,
                    'keywords': keywords_str
                })
                time.sleep(0.3)  # Sleep to respect rate limits
        return pd.DataFrame(movie_data)

    except Exception as e:
        print(f"An error occurred while fetching popular movies: {e}")
        return pd.DataFrame()

# Function to fetch top-rated movies from TMDb


def get_top_rated_movies(pages=5):
    try:
        movie_data = []
        for page in range(1, pages + 1):
            top_rated_movies = movie.top_rated(page=page)

            if not top_rated_movies:
                print(f"No top-rated movies were retrieved on page {page}.")
                continue

            for m in top_rated_movies:
                title = m.title or 'N/A'
                year = m.release_date.split(
                    '-')[0] if m.release_date else 'N/A'
                rating = m.vote_average or 0.0
                genre_ids = m.genre_ids or []
                genres = [get_genre_name(genre_id) for genre_id in genre_ids]
                genres_str = "|".join(genres) if genres else 'N/A'
                overview = m.overview or ''
                # Fetch keywords (requires additional API call)
                keywords = get_movie_keywords(m.id)
                keywords_str = " ".join(keywords)
                # Collect movie data
                movie_data.append({
                    'title': title,
                    'year': year,
                    'rating': rating,
                    'genres': genres_str,
                    'overview': overview,
                    'keywords': keywords_str
                })
                time.sleep(0.3)  # Sleep to respect rate limits
        return pd.DataFrame(movie_data)

    except Exception as e:
        print(f"An error occurred while fetching top-rated movies: {e}")
        return pd.DataFrame()

# Function to fetch keywords for a movie


def get_movie_keywords(movie_id):
    try:
        keywords_response = movie.keywords(movie_id)
        keywords = [kw['name'] for kw in keywords_response.get('keywords', [])]
        return keywords
    except Exception as e:
        print(
            f"An error occurred while fetching keywords for movie ID {movie_id}: {e}")
        return []

# Function to combine popular and top-rated movies


def get_combined_movie_list(pages=5):
    movies_popular = get_popular_movies(pages)
    movies_top_rated = get_top_rated_movies(pages)
    # Combine DataFrames and remove duplicates
    movies_df = pd.concat([movies_popular, movies_top_rated]).drop_duplicates(
        subset='title').reset_index(drop=True)
    return movies_df

# Function to create an enhanced similarity matrix


def create_enhanced_similarity_matrix(df):
    # Fill NaN values with empty strings
    df['overview'] = df['overview'].fillna('')
    df['keywords'] = df['keywords'].fillna('')
    df['genres'] = df['genres'].fillna('')

    # Combine genres, overview, and keywords into a single string
    df['combined_features'] = df['genres'] + \
        " " + df['overview'] + " " + df['keywords']

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Function to recommend movies based on similarity


def recommend_movies(movie_title, similarity_matrix, movies_df, top_n=10):
    if movie_title not in movies_df['title'].values:
        return f"The movie '{movie_title}' was not found in the dataset. Please try another movie."

    movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    similarity_scores = list(enumerate(similarity_matrix[movie_index]))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = [(idx, score)
                         for idx, score in similarity_scores if idx != movie_index]

    top_movie_indices = [i[0] for i in similarity_scores[:top_n]]
    return movies_df['title'].iloc[top_movie_indices]

# Function to recommend movies by genre


def recommend_movies_by_genre(genre, movies_df, top_n=10):
    filtered_movies = movies_df[movies_df['genres'].str.contains(
        genre, case=False, na=False)]

    if filtered_movies.empty:
        return f"No movies found for genre: {genre}"

    sorted_movies = filtered_movies.sort_values(by='rating', ascending=False)
    return sorted_movies.head(top_n)['title'].reset_index(drop=True)


# Main script
if __name__ == "__main__":
    # Fetch the movies (adjust the number of pages as needed)
    movies_df = get_combined_movie_list(pages=2)  # Fetches up to 400 movies

    # Check if the DataFrame is empty or missing 'genres'
    if movies_df.empty or 'genres' not in movies_df.columns:
        print("No valid movie data was retrieved. Exiting.")
    else:
        # Create the enhanced similarity matrix
        similarity_matrix = create_enhanced_similarity_matrix(movies_df)
        for title in movies_df['title']:
            print(title)
            print("")
        # Prompt the user for input
        choice = input(
            "Would you like a recommendation based on previously watched movies or by genre? m/g\n> ").lower()

        if choice == 'm':
            movie_title = input("What was the last movie you saw: \n> ")
            recommended_movies = recommend_movies(
                movie_title, similarity_matrix, movies_df)

            if isinstance(recommended_movies, str):
                print(recommended_movies)
            else:
                print(f"\nMovies similar to '{movie_title}':")
                for i, movie in enumerate(recommended_movies, 1):
                    print(f"{i}. {movie}")

        elif choice == 'g':
            genre = input("What genre would you like: \n> ")
            recommended_movies = recommend_movies_by_genre(genre, movies_df)

            if isinstance(recommended_movies, str):
                print(recommended_movies)
            else:
                print(f"\nTop {len(recommended_movies)} '{genre}' movies:")
                for i, movie in enumerate(recommended_movies, 1):
                    print(f"{i}. {movie}")
        else:
            print("Invalid choice. Please enter 'm' for movies or 'g' for genres.")

# Attribution notice
print("\nThis product uses the TMDb API but is not endorsed or certified by TMDb.")
