import pandas as pd
from pathlib import Path
import os
from typing import Optional


def load_data_from_drive() -> pd.DataFrame:
    FILE_ID = "1vpSvMbFClBkrYE7MaO7Z2OXYjDnFqEjm"
    file_url = f"https://drive.google.com/uc?id={FILE_ID}"
    
    try:
        raw_data = pd.read_csv(file_url)
        print(f"Dataset loaded from Google Drive. Shape: {raw_data.shape}")
        return raw_data
    except Exception as e:
        print(f"Error loading dataset from Google Drive: {e}")
        raise


def load_data() -> pd.DataFrame:
    return load_data_from_drive()


if __name__ == "__main__":
    df = load_data()
    
    print("\nDataset Info:")
    print(df.info())
    print("\nFirst 10 rows:")
    print(df.head(10))
    print("\nDataset description:")
    print(df.describe())