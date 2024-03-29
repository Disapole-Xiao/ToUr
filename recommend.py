class Destination:
    def __init__(self, name, category, keywords, popularity, rating):
        self.name = name
        self.category = category
        self.keywords = keywords
        self.popularity = popularity
        self.rating = rating

# Sample destinations data
destinations = [
    Destination("Great Wall", "Historical", ["history", "culture"], 95, 4.5),
    Destination("Eiffel Tower", "Landmark", ["architecture", "view"], 90, 4.3),
    Destination("Grand Canyon", "Natural", ["nature", "scenery"], 88, 4.4),
    Destination("Harvard University", "Education", ["university", "history"], 92, 4.6),
    Destination("Oxford University", "Education", ["college", "study"], 89, 4.5),
    Destination("Disneyland", "Entertainment", ["theme park", "fun"], 94, 4.7),
    Destination("Louvre Museum", "Art", ["art", "painting"], 91, 4.4),
]

def recommend_destinations(destinations, sort_key):
    sorted_destinations = sorted(destinations, key=lambda x: x.popularity if sort_key == 'popularity' else x.rating, reverse=True)
    return sorted_destinations[:10]

def search_destinations(destinations, keyword, sort_key):
    results = [dest for dest in destinations if keyword.lower() in [kw.lower() for kw in dest.keywords]]
    sorted_results = sorted(results, key=lambda x: x.popularity if sort_key == 'popularity' else x.rating, reverse=True)
    return sorted_results

# Sample usage
recommended_destinations = recommend_destinations(destinations, 'popularity')
print("Recommended Destinations:")
for dest in recommended_destinations:
    print(dest.name, dest.popularity, dest.rating)

search_results = search_destinations(destinations, "history", 'rating')
print("\nSearch Results for 'history':")
for dest in search_results:
    print(dest.name, dest.popularity, dest.rating)
