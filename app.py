import streamlit as st
from src.ui import render_ui

# App Title
st.set_page_config(page_title="CSV Data Generator", layout="wide")

# Render UI
render_ui()
