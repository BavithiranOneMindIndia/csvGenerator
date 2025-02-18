import streamlit as st
import pandas as pd
import faker
import random
import string
import numpy as np
import io
from datetime import datetime, timedelta

# Initialize Faker
fake = faker.Faker()

# Streamlit App
st.title("📄 CSV Data Generator")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Step 1: Select Data Types for Each Column")

    # Define data type options
    data_type_options = ["Same Value", "Random", "Number Range", "Date", "Text"]
    column_types = {}
    data_config = {}

    # User selects data type for each column
    for col in df.columns:
        col_type = st.selectbox(f"Select type for **{col}**", data_type_options, key=f"type_{col}")
        column_types[col] = col_type

        # Configure settings based on selection
        if col_type == "Same Value":
            value = st.text_input(f"Enter the fixed value for {col}", key=f"same_{col}")
            data_config[col] = ("Same Value", value)

        elif col_type == "Random":
            data_config[col] = ("Random",)

        elif col_type == "Number Range":
            min_val = st.number_input(f"Start value for {col}", value=0, key=f"min_{col}")
            max_val = st.number_input(f"End value for {col}", value=100, key=f"max_{col}")
            data_config[col] = ("Number Range", min_val, max_val)

        elif col_type == "Date":
            start_date = st.date_input(f"Start date for {col}", key=f"start_{col}")
            end_date = st.date_input(f"End date for {col}", key=f"end_{col}")
            data_config[col] = ("Date", start_date, end_date)

        elif col_type == "Text":
            char_length = st.number_input(f"Character length for {col}", value=10, key=f"length_{col}")
            data_config[col] = ("Text", char_length)

    # Select number of rows to generate
    num_rows = st.number_input("Number of rows to generate", min_value=1, value=10)

    if st.button("Generate Data"):
        new_data = []
        for _ in range(num_rows):
            row = {}
            for col, (dtype, *args) in data_config.items():
                if dtype == "Same Value":
                    row[col] = args[0]
                elif dtype == "Random":
                    row[col] = fake.word()
                elif dtype == "Number Range":
                    row[col] = random.randint(args[0], args[1])
                elif dtype == "Date":
                    delta = args[1] - args[0]
                    random_days = random.randint(0, delta.days)
                    row[col] = args[0] + timedelta(days=random_days)
                elif dtype == "Text":
                    row[col] = "".join(random.choices(string.ascii_letters, k=args[0]))
            new_data.append(row)

        new_df = pd.DataFrame(new_data)

        # Convert to CSV
        csv_buffer = io.StringIO()
        new_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue().encode()

        st.write("### Generated Data Preview")
        st.dataframe(new_df)

        # Download Button
        st.download_button("Download CSV", data=csv_bytes, file_name="generated_data.csv", mime="text/csv")
