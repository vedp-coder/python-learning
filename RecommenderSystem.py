import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

class RecommenderSystem:
    def __init__(self):
        self.movies_df = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.indices = None
        
    def load_data(self, filepath):
        """Load movie dataset"""
        self.movies_df = pd.read_csv(filepath)
        print(f"Loaded dataset with {self.movies_df.shape[0]} movies")
        
    def create_sample_data(self, size=1000):
        """Create sample movie data if no dataset is available"""
        genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 
                 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
                 'Romance', 'Science Fiction', 'Thriller', 'War', 'Western']
        
        # Generate sample movie data
        movies = []
        for i in range(size):
            # Generate random movie details
            movie_id = i + 1
            title = f"Sample Movie {movie_id}"
            year = np.random.randint(1970, 2023)
            
            # Assign 1-3 random genres
            num_genres = np.random.randint(1, 4)
            movie_genres = '|'.join(np.random.choice(genres, num_genres, replace=False))
            
            # Generate random rating
            rating = round(np.random.uniform(1.0, 10.0), 1)
            
            movies.append({
                'movieId': movie_id,
                'title': f"{title} ({year})",
                'genres': movie_genres,
                'rating': rating
            })
        
        self.movies_df = pd.DataFrame(movies)
        print(f"Created sample dataset with {size} movies")
        
    def preprocess_data(self):
        """Preprocess data and create feature vectors"""
        if self.movies_df is None:
            print("No data loaded. Please load data first.")
            return False
            
        # Create a new soup feature
        if 'genres' in self.movies_df.columns:
            # Use TF-IDF vectorizer for genre features
            tfidf = TfidfVectorizer(stop_words='english')
            self.tfidf_matrix = tfidf.fit_transform(self.movies_df['genres'].fillna(''))
            
            # Compute cosine similarity matrix
            self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
            
            # Create a reverse mapping
            self.indices = pd.Series(self.movies_df.index, index=self.movies_df['title']).drop_duplicates()
            
            return True
        else:
            print("Required columns not found in dataset")
            return False
    
    def get_recommendations(self, title, n=10):
        """Generate movie recommendations based on a movie title"""
        if self.cosine_sim is None:
            print("Model not initialized. Please preprocess data first.")
            return None
        
        # Get the index of the movie that matches the title
        if title not in self.indices:
            closest_match = self.find_closest_match(title)
            if closest_match:
                print(f"Movie '{title}' not found. Using closest match: '{closest_match}'")
                title = closest_match
            else:
                print(f"Movie '{title}' not found and no close matches.")
                return None
        
        idx = self.indices[title]
        
        # Get the pairwise similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort movies by similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N most similar movies
        sim_scores = sim_scores[1:n+1]
        
        # Get movie indices
        movie_indices = [i[0] for i in sim_scores]
        
        # Return top movies with similarity scores
        recommendations = self.movies_df.iloc[movie_indices][['title', 'genres']]
        recommendations['similarity'] = [i[1] for i in sim_scores]
        
        return recommendations
    
    def find_closest_match(self, title):
        """Find closest matching movie title"""
        titles = self.movies_df['title'].values
        closest = None
        max_sim = -1
        
        for t in titles:
            # Simple string similarity - count matching characters
            sim = sum(c1 == c2 for c1, c2 in zip(title.lower(), t.lower())) / max(len(title), len(t))
            if sim > max_sim and sim > 0.5:  # Threshold for similarity
                max_sim = sim
                closest = t
                
        return closest
    
    def visualize_recommendations(self, recommendations):
        """Visualize recommendation results"""
        if recommendations is not None and not recommendations.empty:
            plt.figure(figsize=(12, 6))
            
            # Plot similarity scores
            plt.barh(recommendations['title'], recommendations['similarity'])
            plt.xlabel('Similarity Score')
            plt.title('Movie Recommendations')
            plt.tight_layout()
            plt.show()

def main():
    recommender = RecommenderSystem()
    
    while True:
        print("\nMovie Recommender System Menu:")
        print("1. Create sample data")
        print("2. Load movie data")
        print("3. Preprocess data")
        print("4. Get recommendations")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            size = int(input("Enter number of sample movies to create: "))
            recommender.create_sample_data(size)
            
        elif choice == '2':
            filepath = input("Enter path to movie dataset CSV: ")
            try:
                recommender.load_data(filepath)
            except Exception as e:
                print(f"Error loading data: {e}")
                
        elif choice == '3':
            if recommender.preprocess_data():
                print("Data preprocessing complete!")
                
        elif choice == '4':
            if recommender.indices is not None:
                title = input("Enter a movie title for recommendations: ")
                recommendations = recommender.get_recommendations(title)
                
                if recommendations is not None:
                    print("\nTop recommendations:")
                    print(recommendations[['title', 'similarity']])
                    recommender.visualize_recommendations(recommendations)
            else:
                print("Please preprocess data first (option 3).")
                
        elif choice == '5':
            print("Thank you for using the Movie Recommender!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
