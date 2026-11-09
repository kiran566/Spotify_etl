
import requests

BASE_URL = "https://musicbrainz.org/ws/2"

HEADERS = {
    "User-Agent": "MusicETLPipeline/1.0 (your-real-email@example.com)"
}


def extract_artists(query):

    url = f"{BASE_URL}/artist/"

    params = {
        "query": query,
        "fmt": "json",
        "limit": 10
    }

    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.json()
