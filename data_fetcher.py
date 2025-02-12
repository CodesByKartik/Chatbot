# data_fetcher.py
import wikipediaapi

def fetch_wikipedia_data(query: str) -> str:
    """
    Fetch relevant information from Wikipedia based on the query.
    """
    wiki = wikipediaapi.Wikipedia("en", user_agent="Chatbot-App/1.0 (Python; no-website)")

    # Try to get the page
    page = wiki.page(query)
    
    if page.exists():
        return page.text  # Return the full content of the Wikipedia page
    else:
        return "Sorry, no relevant information found."
