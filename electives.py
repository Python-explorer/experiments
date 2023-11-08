import streamlit as st
import pandas as pd

# Function to load CSV data from a URL
@st.experimental_memo
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# URL to the CSV file
data_url = 'https://raw.githubusercontent.com/yourusername/yourrepo/main/yourdata.csv'

# Load the data
data = load_data(data_url)

# Main app
def main():
    if not data.empty:
        st.write("Unique values in 'Treatment Function' column:")
        # Display the unique values in the column
        unique_values = data['Treatment Function'].unique()
        st.write(unique_values)
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
