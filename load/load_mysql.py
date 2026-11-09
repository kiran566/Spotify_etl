
import pandas as pd
import os

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
load_dotenv()


def load_csv():
    file_path = Path("data/processed/artists.csv")
    return pd.read_csv(file_path)


def connect_db():

    connection_string = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )

    engine = create_engine(connection_string)

    return engine


def load_to_mysql(df):

    engine = connect_db()

    # Match CSV column names with MySQL schema
    df = df.rename(columns={
        "type": "artist_type"
    })

    # Convert Pandas missing values to None
    df = df.astype(object).where(pd.notna(df), None)

    insert_query = text("""
        INSERT INTO artists (
            id, name, sort_name, artist_type,
            gender, country, score,
            life_span_begin, life_span_end,
            disambiguation
        )
        VALUES (
            :id, :name, :sort_name, :artist_type,
            :gender, :country, :score,
            :life_span_begin, :life_span_end,
            :disambiguation
        )
        ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            sort_name = VALUES(sort_name),
            artist_type = VALUES(artist_type),
            gender = VALUES(gender),
            country = VALUES(country),
            score = VALUES(score),
            life_span_begin = VALUES(life_span_begin),
            life_span_end = VALUES(life_span_end),
            disambiguation = VALUES(disambiguation)
    """)

    records = df.to_dict(orient="records")

    try:
        with engine.begin() as connection:

            connection.execute(insert_query, records)

        print("Records processed:", len(records))
        print("MySQL UPSERT completed successfully!")

    except Exception as error:
        print("Error loading data:", error)

    finally:
        engine.dispose()


def main():

    df = load_csv()

    print("CSV records:", len(df))

    load_to_mysql(df)


if __name__ == "__main__":
    main()
