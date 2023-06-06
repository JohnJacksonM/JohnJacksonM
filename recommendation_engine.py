import numpy as np
from scipy.spatial.distance import cosine

class RecommendationEngine:
    def __init__(self, ratings):
        self.ratings = ratings

    def calculate_similarity(self, user1, user2):
        ratings_user1 = self.ratings[user1]
        ratings_user2 = self.ratings[user2]
        similarity = 1 - cosine(ratings_user1, ratings_user2)
        return similarity

    def recommend_items(self, user, num_recommendations=5):
        user_ratings = self.ratings[user]
        similarities = []

        for other_user in self.ratings:
            if other_user != user:
                similarity = self.calculate_similarity(user, other_user)
                similarities.append((other_user, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        recommendations = []
        for i in range(num_recommendations):
            similar_user, similarity = similarities[i]
            similar_user_ratings = self.ratings[similar_user]
            for j in range(len(similar_user_ratings)):
                if user_ratings[j] == 0 and similar_user_ratings[j] > 0:
                    recommendations.append((j, similar_user_ratings[j]))
        
        recommendations.sort(key=lambda x: x[1], reverse=True)
        recommended_items = [item for item, _ in recommendations]

        return recommended_items[:num_recommendations]

# Example usage:
ratings = {
    'User1': [3, 4, 0, 0, 5],
    'User2': [0, 2, 3, 1, 4],
    'User3': [1, 0, 5, 2, 0],
    'User4': [4, 2, 0, 4, 0],
    'User5': [2, 0, 4, 0, 3]
}

recommender = RecommendationEngine(ratings)

user = 'User1'
recommendations = recommender.recommend_items(user, num_recommendations=3)
print("Recommendations for", user + ":")
for item in recommendations:
    print("Item", item)
