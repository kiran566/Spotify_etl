import requests

def extract_artists(query):

    url = "https://musicbrainz.org/ws/2/artist/"

    params = {
        "query": query,
        "fmt": "json",
        "limit": 10
    }

    headers = {
        "User-Agent": "SpotifyETLProject/1.0 (your_email@example.com)"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.json()