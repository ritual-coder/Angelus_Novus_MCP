import logging
from twitter.client import search_trend_images

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_search():
    # Use a generic, likely-to-have-images term
    query = "Art" 
    print(f"Testing image search for query: {query}")
    
    results = search_trend_images(query, max_results=10)
    
    if not results:
        print("No results found.")
        return

    print(f"Found {len(results)} results:")
    for i, res in enumerate(results, 1):
        print(f"\n--- Result {i} ---")
        print(f"Text: {res.get('text')}")
        print(f"Image Used: {res.get('image_url')}")
        print(f"Author ID: {res.get('author_id')}")

if __name__ == "__main__":
    test_search()
