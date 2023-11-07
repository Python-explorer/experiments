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
        # Send a GET request to the URL
        response = requests.get(url)
        # Ensure the request is successful
        response.raise_for_status()
        
        # Check the content type of the response to guess the file type
        content_type = response.headers.get('Content-Type')
        if 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
            engine = 'openpyxl'  # For .xlsx files
        elif 'application/vnd.ms-excel' in content_type:
            engine = 'xlrd'  # For .xls files
        else:
            raise ValueError(f"Unknown Content-Type for Excel file: {content_type}")
        
        # Read the content of the response with the appropriate engine
        return pd.read_excel(BytesIO(response.content), engine=engine)
    except requests.exceptions.HTTPError as e:
        raise st_exception(f"HTTPError: {e.response.status_code} {e.response.reason} for URL: {url}")
    except ValueError as e:
        raise st_exception(f"ValueError: {e}")
    except Exception as e:
        raise st_exception(f"An error occurred: {e}")

# Make sure to provide the correct URL to your Excel file
data_url = 'https://path_to_your_excel_file.xlsx'
df = load_data(data_url)

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
