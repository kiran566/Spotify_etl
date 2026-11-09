# Music ETL Pipeline — MusicBrainz API to MySQL

A Python-based ETL pipeline that extracts artist information from the MusicBrainz API, stores the raw API response as JSON, transforms and cleans the data using Pandas, and loads the processed records into a MySQL database.

## Project Overview

This project demonstrates a basic end-to-end **ETL (Extract, Transform, Load)** workflow.

- **Extract:** Fetch artist information from the MusicBrainz API.
- **Store:** Save the original API response as a JSON file.
- **Transform:** Flatten nested JSON, select required fields, handle missing values, remove duplicates, and convert data types using Pandas.
- **Load:** Load cleaned records into MySQL using SQLAlchemy.
- **Upsert:** Update existing artist records or insert new ones using MySQL's `ON DUPLICATE KEY UPDATE`.

## Architecture

```text
              MusicBrainz API
                     |
                     v
              EXTRACT DATA
                     |
                     v
           data/raw/artists.json
                (Bronze)
                     |
                     v
            TRANSFORM DATA
             Using Pandas
                     |
                     v
        data/processed/artists.csv
                 (Silver)
                     |
                     v
              LOAD DATA
             SQLAlchemy
                     |
                     v
               MySQL DB
                (Gold)
```

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline development |
| MusicBrainz API | Source of music artist data |
| Requests | API requests |
| JSON | Raw data storage |
| Pandas | Data transformation and cleaning |
| MySQL | Structured data storage |
| SQLAlchemy | Database connectivity and execution |
| PyMySQL | MySQL database driver |
| python-dotenv | Environment variable management |

## Project Structure

```text
Spotify_etl/
│
├── extract/
│   └── musicbrainz.py
│
├── transform/
│   └── transform_data.py
│
├── load/
│   └── load_mysql.py
│
├── data/
│   ├── raw/
│   │   └── artists.json
│   │
│   └── processed/
│       └── artists.csv
│
├── logs/
│
├── main.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Spotify_etl
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=music_db
DB_USER=root
DB_PASSWORD=your_mysql_password
```

Replace the password with your local MySQL password.

### 5. Create the MySQL database

Execute this SQL in MySQL Workbench:

```sql
CREATE DATABASE music_db;

USE music_db;

CREATE TABLE artists (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sort_name VARCHAR(255),
    artist_type VARCHAR(100),
    gender VARCHAR(50),
    country VARCHAR(100),
    score INT,
    life_span_begin DATE,
    life_span_end DATE,
    disambiguation TEXT
);
```

### 6. Run the pipeline

```bash
python main.py
```

The pipeline will extract artist information, save the raw JSON response, transform and clean the data, and load the results into MySQL.

## Data Transformation

The transformation stage performs the following operations:

- Flattens JSON records using `pandas.json_normalize()`.
- Selects the required artist attributes.
- Handles missing values.
- Removes duplicate records using artist IDs.
- Removes records without essential IDs or names.
- Standardizes artist names.
- Converts score and life-span fields into appropriate data types.
- Saves the processed data as a CSV file.

## Database Loading Strategy

The pipeline uses MySQL **UPSERT** logic:

```sql
INSERT INTO artists (...)
VALUES (...)
ON DUPLICATE KEY UPDATE
    name = VALUES(name),
    country = VALUES(country);
```

This prevents duplicate artist records when the pipeline runs repeatedly. Existing records are updated when their primary key already exists.

## Data Layers

| Layer | Storage | Description |
|---|---|---|
| Bronze | JSON | Original API response |
| Silver | CSV | Cleaned and transformed data |
| Gold | MySQL | Structured, queryable artist records |

## Future Improvements

- Add structured logging and robust exception handling.
- Implement incremental data loading.
- Add automated data quality checks.
- Schedule pipeline execution.
- Introduce Apache Airflow for orchestration.
- Add Docker support.
- Build analytical dashboards using the loaded data.

## Learning Outcomes

Through this project, I practiced:

- Working with REST APIs.
- Extracting and storing raw data.
- Handling JSON and nested data structures.
- Data cleaning and transformation using Pandas.
- Connecting Python applications to MySQL.
- Implementing database UPSERT operations.
- Organizing an ETL pipeline into modular components.

## Data Source

MusicBrainz API: https://musicbrainz.org/doc/MusicBrainz_API

**Note:** MusicBrainz requests should use a meaningful User-Agent and respect the API's rate limit of approximately one request per second.