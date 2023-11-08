# app.py
import streamlit as st

# Define the navigation structure
PAGES = {
    "Descriptive Statistics": "electives",
    "Long waits analysis tool": "longwaits"
    # You can add more pages here
}

# Sidebar for navigation
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

module = PAGES[selection]
if module == "electives":
    electives = importlib.import_module(module)
    importlib.reload(electives)  # This reloads the module
    electives.app()
elif module == "longwaits":
    electives = importlib.import_module(module)
    importlib.reload(longwaits)  # This reloads the module
    longwaits.app()
# Add elif blocks for additional pages as needed
