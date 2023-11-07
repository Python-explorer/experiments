import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from streamlit import exception as st_exception

# Function to load data
@st.cache
def load_data(url):
    try:
        # Use pandas to read the excel file from the given url
        return pd.read_excel(url)
    except Exception as e:
        # If there's an error, show it in the Streamlit app
        st.error(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame as a fallback

# Specify the URL of your Excel file
data_url = 'https://docs.google.com/spreadsheets/d/1zCrX-_4zPRxXuqHrKwnJ_uLwaU-iH_zVMy65Q7IsO1M/edit?usp=sharing'

# Make sure to call load_data with the data_url
data = load_data(data_url)

# Check if data is loaded and not empty before proceeding
if not data.empty:
    # Get the unique values from the 'Treatment Function' column as options for the selectbox
    unique_functions = data['Treatment Function'].unique().tolist()
    selected_function = st.sidebar.selectbox('Select a Treatment Function:', unique_functions)
else:
    # If data is empty, display a message in the sidebar
    st.sidebar.write("No data available.")

# Function to plot the bar chart
def plot_bar_chart(data, selected_function):
    # Filter data for the selected treatment function
    filtered_data = data[data['Treatment Function'] == selected_function]

    # Sort the data by 'Total number of incomplete pathways' in ascending order
    filtered_data_sorted = filtered_data.sort_values(by='Total number of incomplete pathways', ascending=True)
    
    # Determine the quartiles
    quartiles = filtered_data_sorted['Total number of incomplete pathways'].quantile([0.25, 0.5, 0.75]).values

    # Color the bars based on the quartile
    colors = ['green' if x < quartiles[0]
              else 'orange' if quartiles[0] <= x < quartiles[2]
              else 'red' for x in filtered_data_sorted['Total number of incomplete pathways']]

    # Find the position of 'NHS SUSSEX INTEGRATED CARE BOARD' after sorting
    sussex_position = filtered_data_sorted.reset_index().index[filtered_data_sorted['ICB Name'] == 'NHS SUSSEX INTEGRATED CARE BOARD'].tolist()
    if sussex_position:
        # Apply the light blue color to the 'NHS SUSSEX INTEGRATED CARE BOARD' bar
        colors[sussex_position[0]] = 'lightblue'

    # Create the bar chart
    plt.figure(figsize=(20, 20))
    plt.bar(filtered_data_sorted['ICB Name'], filtered_data_sorted['Total number of incomplete pathways'], color=colors)
    plt.xlabel('ICB Name', fontsize=24)
    plt.ylabel('Total number of incomplete pathways')
    plt.title(f'Total Number of Incomplete Pathways - {selected_function}')
    plt.xticks(rotation=90)
    plt.tight_layout()  # Adjust layout to fit the x-axis labels
    return plt

# Load the dataset
data = load_data()

# Streamlit sidebar - Treatment Function selection
selected_function = st.sidebar.selectbox('Select a Treatment Function:', data['Treatment Function'].unique())

# Plot the chart in the main page
st.write(f"## Total Number of Incomplete Pathways - {selected_function}")
fig = plot_bar_chart(data, selected_function)
st.pyplot(fig)
