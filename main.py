import json
from extract.musicbrainz import extract_artists

data = extract_artists("Anirudh")
with open("data/raw/artists.json", "w", encoding="utf-8") as file:

    json.dump(data, file, indent=4, ensure_ascii=False)


for artist in data["artists"]:

    print("Name:", artist["name"])
    print("ID:", artist["id"])
    print("Country:", artist.get("country"))
    print("Type:", artist.get("type"))
    print("-------------------")