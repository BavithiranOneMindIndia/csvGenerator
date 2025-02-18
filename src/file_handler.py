import pandas as pd
import io

def process_uploaded_file(uploaded_file):
    """Reads an uploaded CSV file and returns a DataFrame"""
    return pd.read_csv(uploaded_file)

def save_csv(df):
    """Converts DataFrame to CSV format"""
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode()
