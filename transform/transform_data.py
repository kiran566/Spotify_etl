import pandas as pd
import json
from pathlib import Path


def load_raw_data():

    file_path = Path("data/raw/artists.json")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def transform_artists(artists):

    df = pd.json_normalize(artists)

    required_columns = [
        "id",
        "name",
        "sort-name",
        "type",
        "gender",
        "country",
        "score",
        "life-span.begin",
        "life-span.end",
        "disambiguation"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df = df[required_columns]

    return df


def clean_artists(df):

    df.columns = (
        df.columns
        .str.lower()
        .str.replace("-", "_")
        .str.replace(".", "_")
    )

    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=["id", "name"])

    df["name"] = df["name"].str.strip()

    df["country"] = df["country"].fillna("Unknown")
    df["gender"] = df["gender"].fillna("Unknown")

    df["score"] = pd.to_numeric(
        df["score"], errors="coerce"
    )

    df["life_span_begin"] = pd.to_datetime(
        df["life_span_begin"], errors="coerce"
    )

    df["life_span_end"] = pd.to_datetime(
        df["life_span_end"], errors="coerce"
    )

    return df


def save_processed_data(df):

    output_path = Path("data/processed/artists.csv")

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(output_path, index=False)

    print("Processed data saved:", output_path)


def main():

    data = load_raw_data()

    artists = data.get("artists", [])

    print("Raw records:", len(artists))

    df = transform_artists(artists)

    df = clean_artists(df)

    print("\nCleaned DataFrame:")
    print(df.head())

    print("\nDataFrame information:")
    print(df.info())

    print("\nMissing values:")
    print(df.isnull().sum())

    save_processed_data(df)


if __name__ == "__main__":
    main()