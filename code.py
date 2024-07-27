import pandas as pd
import numpy as np

def load_data(file_path):
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def handle_missing_values(df, numeric_strategy='mean', non_numeric_strategy='mode', columns=None):
    """Handle missing values in the DataFrame."""
    if columns is None:
        columns = df.columns

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.intersection(columns)
    non_numeric_cols = df.select_dtypes(exclude=['float64', 'int64']).columns.intersection(columns)

    for column in numeric_cols:
        if numeric_strategy == 'mean':
            df[column] = df[column].fillna(df[column].mean())
        elif numeric_strategy == 'median':
            df[column] = df[column].fillna(df[column].median())
        elif numeric_strategy == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        elif numeric_strategy == 'drop':
            df = df.dropna(subset=[column])

    for column in non_numeric_cols:
        if non_numeric_strategy == 'mode':
            df[column] = df[column].fillna(df[column].mode()[0])
        elif non_numeric_strategy == 'drop':
            df = df.dropna(subset=[column])
        else:
            print(f"Warning: Non-numeric column '{column}' can only be filled with 'mode' or 'drop' strategy.")
    
    return df

def remove_duplicates(df):
    """Remove duplicates."""
    return df.drop_duplicates()

def normalize_data(df, columns=None):
    """Normalize numeric columns in the DataFrame."""
    if columns is None:
        columns = df.select_dtypes(include=['float64', 'int64']).columns

    for column in columns:
        df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())

    return df

def transform_data_types(df, column_type_mapping):
    """Transform data types of specific columns in the DataFrame."""
    for column, dtype in column_type_mapping.items():
        if column in df.columns:
            try:
                df[column] = df[column].astype(dtype)
            except ValueError:
                print(f"Warning: Unable to convert column '{column}' to {dtype}")
        else:
            print(f"Warning: Column '{column}' not found in DataFrame.")
    return df

def save_data(df, file_path):
    """Save the cleaned DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)

# Input and Output file's path
file_path = r"C:\Users\hp\OneDrive\Desktop\DEATH.csv"
output_file_path = r"C:\Users\hp\OneDrive\Desktop\Cleaned_DEATH.csv"

df = load_data(file_path)

# Handle missing values
df = handle_missing_values(df, numeric_strategy='mean', non_numeric_strategy='mode')

# Remove duplicates
df = remove_duplicates(df)

# Normalize data
df = normalize_data(df)

# Save the cleaned data
save_data(df, output_file_path)

print("Data cleaning and preprocessing complete.")
