import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# The URL of the raw CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/ElectiveDataICB.csv'

@st.cache
def load_data(url):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(url)
    # Handle thousands separator if present
    data['Total number of incomplete pathways'] = pd.to_numeric(
        data['Total number of incomplete pathways'].str.replace(',', ''), errors='coerce')
    return data

# Load the data
df = load_data(csv_url)

# Filter the DataFrame for the given 'ICB NAME' and exclude rows where 'Treatment Function' is 'Total'
icb_name_filter = 'NHS SUSSEX INTEGRATED CARE BOARD'
df_filtered = df[(df['ICB Name'] == icb_name_filter) & (df['Treatment Function'] != 'Total')]

# Group by 'Treatment Function' and sum 'Total number of incomplete pathways'
df_grouped = df_filtered.groupby('Treatment Function')['Total number of incomplete pathways'].sum().reset_index()

# Sort the grouped data by 'Total number of incomplete pathways' in ascending order for the bar chart
df_sorted = df_grouped.sort_values(by='Total number of incomplete pathways', ascending=True)

# Create a vertical bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(df_sorted['Treatment Function'], df_sorted['Total number of incomplete pathways'])
ax.set_xlabel('Treatment Function')
ax.set_ylabel('Total number of incomplete pathways')
ax.set_title('Total Incomplete Pathways by Treatment Function for NHS SUSSEX INTEGRATED CARE BOARD')
plt.xticks(rotation=90)  # Rotate the x-axis labels to show them more clearly

# Display the chart
st.pyplot(fig)
