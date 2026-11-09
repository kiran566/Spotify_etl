
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

    # Rename CSV column to match MySQL table
    df = df.rename(columns={
        "type": "artist_type"
    })

    try:
        df.to_sql(
            name="artists",
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=500
        )

        print("Data loaded successfully!")

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
