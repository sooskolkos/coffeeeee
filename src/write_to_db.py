import argparse
import pandas as pd
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine

def load_data() -> pd.DataFrame:
    FILE_ID = "1vpSvMbFClBkrYE7MaO7Z2OXYjDnFqEjm"
    file_url = f"https://drive.google.com/uc?id={FILE_ID}"
    
    print("Loading data directly from Google Drive...")
    df = pd.read_csv(file_url)
    print(f"Dataset shape: {df.shape}")
    return df

def load_creds(creds_path: str) -> dict:
    if not Path(creds_path).exists():
        raise FileNotFoundError(f"No file {creds_path}")
    conn = sqlite3.connect(creds_path)
    try:
        row = pd.read_sql("SELECT * FROM access LIMIT 1", conn).iloc[0].to_dict()
    finally:
        conn.close()
    return row

def make_engine(creds: dict, db_name: str | None):
    db = db_name or creds.get("db") or "homeworks"
    url = creds["url"]
    port = creds["port"]
    user = creds["user"]
    pwd = creds["pass"]
    return create_engine(f"postgresql+psycopg2://{user}:{pwd}@{url}:{port}/{db}")

def write_to_db(df: pd.DataFrame, table: str, engine):
    df_head = df.head(100)
    with engine.begin() as conn:
        df_head.to_sql(table, con=conn, schema="public", if_exists="replace", index=False, method="multi", chunksize=1000)
    print(f"Successfully wrote {len(df_head)} rows to table '{table}'")

def main():
    parser = argparse.ArgumentParser(description="Load data from Google Drive to PostgreSQL")
    parser.add_argument("--table", required=True, help="Target table name")
    parser.add_argument("--creds", default="creds.db", help="Path to credentials SQLite DB")
    parser.add_argument("--db", required=False, help="Database name (default: homeworks)")
    args = parser.parse_args()

    df = load_data()
    
    creds = load_creds(args.creds)
    print(f"Using database: {creds.get('url', 'Unknown')}")
    
    engine = make_engine(creds, args.db)
    write_to_db(df, args.table, engine)
    print("Data writing completed successfully!")

if __name__ == "__main__":
    main()