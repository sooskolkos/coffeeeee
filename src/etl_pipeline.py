import pandas as pd
import os
from pathlib import Path
import click
from typing import Dict, Any
import numpy as np

from data_loader import load_data


def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    df_converted = df.copy()
    
    type_conversions = {
        'Age': 'int32',
        'Coffee_Intake': 'int32', 
        'Sleep_Hours': 'float32',
        'BMI': 'float32',
        'Stress_Level': 'int32',
        'Sleep_Quality': 'int32',
        'Income': 'float32',
    }
    
    for col, dtype in type_conversions.items():
        if col in df_converted.columns:
            try:
                if df_converted[col].isnull().any():
                    if 'int' in dtype:
                        df_converted[col] = df_converted[col].fillna(df_converted[col].median()).round()
                    else:
                        df_converted[col] = df_converted[col].fillna(df_converted[col].median())
                
                df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')
                
                if np.issubdtype(df_converted[col].dtype, np.number):
                    df_converted[col] = df_converted[col].replace([np.inf, -np.inf], np.nan)
                    if df_converted[col].isnull().any():
                        df_converted[col] = df_converted[col].fillna(df_converted[col].median())
                
                df_converted[col] = df_converted[col].astype(dtype)
                
            except Exception as e:
                print(f"Warning: Could not convert column '{col}' to {dtype}: {e}")
    
    categorical_columns = ['Gender', 'Country', 'Occupation']
    for col in categorical_columns:
        if col in df_converted.columns:
            try:
                if df_converted[col].isnull().any():
                    mode_val = df_converted[col].mode()
                    df_converted[col] = df_converted[col].fillna(
                        mode_val[0] if len(mode_val) > 0 else 'Unknown'
                    )
                df_converted[col] = df_converted[col].astype('category')
            except Exception as e:
                print(f"Warning: Could not convert column '{col}' to category: {e}")
    
    return df_converted


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    
    print("Cleaning data...")
    
    for col in df_clean.columns:
        missing_count = df_clean[col].isnull().sum()
        if missing_count > 0:
            print(f"  - Column '{col}': {missing_count} missing values")
            
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            else:
                mode_values = df_clean[col].mode()
                if len(mode_values) > 0:
                    df_clean[col] = df_clean[col].fillna(mode_values[0])
                else:
                    df_clean[col] = df_clean[col].fillna('Unknown')

    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed_duplicates = initial_rows - len(df_clean)
    if removed_duplicates > 0:
        print(f"Removed {removed_duplicates} duplicate rows")

    df_clean = convert_data_types(df_clean)
    
    return df_clean


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df_featured = df.copy()
    
    print("Performing feature engineering...")
    
    object_columns = df_featured.select_dtypes(include=['object']).columns
    
    for col in object_columns:
        try:
            if col in ['Gender', 'Country', 'Occupation']:
                continue
                
            temp_series = pd.to_datetime(df_featured[col], errors='coerce')
            if temp_series.notna().any():
                df_featured[col] = temp_series
                print(f"  Converted column '{col}' to datetime")

                df_featured[f'{col}_year'] = df_featured[col].dt.year.astype('int32')
                df_featured[f'{col}_month'] = df_featured[col].dt.month.astype('int32')
                df_featured[f'{col}_day'] = df_featured[col].dt.day.astype('int32')
        except Exception as e:
            print(f"  Could not process column '{col}' as datetime: {e}")
    
    return df_featured


@click.command()
def run_etl_pipeline():
    print("Starting ETL pipeline...")
    
    df = load_data()
    
    df_clean = clean_data(df)
    df_final = feature_engineering(df_clean)
    
    print("ETL pipeline completed successfully!")
    print(f"Final dataset shape: {df_final.shape}")
    
    return df_final


if __name__ == "__main__":
    run_etl_pipeline()