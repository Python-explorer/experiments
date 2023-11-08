# app.py
import streamlit as st

# Define the navigation structure
PAGES = {
    "Descriptive Statistics": "electives",
    # You can add more pages here
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

if selection == "Descriptive Statistics":
    import electives
    electives.app()
# Add elif blocks for additional pages as needed
