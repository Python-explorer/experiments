import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data
@st.cache_data
def load_data(url):
    return pd.read_excel(url)

data_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/electives.xlsx'
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
