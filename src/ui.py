import streamlit as st
from src.file_handler import process_uploaded_file
from src.data_generator import generate_data


def render_ui():
    """Renders the Streamlit UI"""
    st.title("📄 CSV Data Generator")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        df = process_uploaded_file(uploaded_file)
        st.write("### Step 1: Select Data Types for Each Column")

        # Define data type options
        data_type_options = [
            "Same Value",
            "Random",
            "Number Range",
            "Date",
            "Text",
            "Sequential Number",
            "Concatenate with Padding",
        ]
        column_types = {}
        data_config = {}

        # User selects data type for each column
        for col in df.columns:
            col_type = st.selectbox(
                f"Select type for **{col}**", data_type_options, key=f"type_{col}"
            )
            column_types[col] = col_type

            # Configure settings based on selection
            if col_type == "Same Value":
                value = st.text_input(
                    f"Enter the fixed value for {col}", key=f"same_{col}"
                )
                data_config[col] = ("Same Value", value)

            elif col_type == "Random":
                data_config[col] = ("Random",)

            elif col_type == "Number Range":
                min_val = st.number_input(
                    f"Start value for {col}", value=0, key=f"min_{col}"
                )
                max_val = st.number_input(
                    f"End value for {col}", value=100, key=f"max_{col}"
                )
                data_config[col] = ("Number Range", min_val, max_val)

            elif col_type == "Date":
                start_date = st.date_input(f"Start date for {col}", key=f"start_{col}")
                end_date = st.date_input(f"End date for {col}", key=f"end_{col}")
                data_config[col] = ("Date", start_date, end_date)

            elif col_type == "Text":
                char_length = st.number_input(
                    f"Character length for {col}", value=10, key=f"length_{col}"
                )
                data_config[col] = ("Text", char_length)

            elif col_type == "Sequential Number":
                start_value = st.number_input(
                    f"Start value for {col}", value=0, key=f"seq_start_{col}"
                )
                data_config[col] = ("Sequential Number", start_value)

            elif col_type == "Concatenate with Padding":
                base_value = st.text_input(f"Base value for {col}", key=f"base_{col}")
                padding_length = st.number_input(
                    f"Padding length for {col}", value=3, key=f"padding_{col}"
                )
                data_config[col] = (
                    "Concatenate with Padding",
                    base_value,
                    padding_length,
                )

        num_rows = st.number_input("Number of rows to generate", min_value=1, value=5)

        if st.button("Generate Data"):
            new_df = generate_data(num_rows, data_config)
            st.write("### Generated Data Preview")
            st.dataframe(new_df)

            csv_data = new_df.to_csv(index=False).encode()
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="generated_data.csv",
                mime="text/csv",
            )
