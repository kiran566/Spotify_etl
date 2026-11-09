
import json
from pathlib import Path

from extract.musicbrainz import extract_artists
from transform.transform_data import run_transformation
from load.load_mysql import load_to_mysql


def main():

    print("=" * 45)
    print("       MUSIC ETL PIPELINE STARTED")
    print("=" * 45)

    # STEP 1: EXTRACT
    print("\nSTEP 1: Extracting data...")

    raw_data = extract_artists("balu")

    print("Extraction completed!")

    # STEP 2: SAVE RAW JSON
    print("\nSTEP 2: Saving raw data...")

    raw_path = Path("data/raw/artists.json")
    raw_path.parent.mkdir(parents=True, exist_ok=True)

    with open(raw_path, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, indent=4, ensure_ascii=False)

    print("Raw JSON saved successfully!")

    # STEP 3: TRANSFORM
    print("\nSTEP 3: Transforming data...")

    df = run_transformation(raw_data)

    print("Transformation completed!")

    # STEP 4: LOAD
    print("\nSTEP 4: Loading data into MySQL...")

    load_to_mysql(df)

    print("\n" + "=" * 45)
    print("       MUSIC ETL PIPELINE FINISHED")
    print("=" * 45)


if __name__ == "__main__":
    main()
