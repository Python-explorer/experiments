import streamlit as st
import pandas as pd
import altair as alt

# The URL of the raw CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/ElectiveDataICB.csv'

@st.cache
def load_data(url):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(url)
    return data

# Load the data
df = load_data(csv_url)

# Streamlit dropdown menu for 'Treatment Function'
selected_treatment = st.selectbox(
    'Select a Treatment Function:',
    options=df['Treatment Function'].unique()
)

# Filter the DataFrame based on the selected treatment function
filtered_df = df[df['Treatment Function'] == selected_treatment]

# Create a vertical bar chart using Altair
chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('ICB Name:N', sort='-y'),  # Sort bars by the 'Total number of incomplete pathways' in descending order
    y=alt.Y('Total number of incomplete pathways:Q'),
    tooltip=['ICB Name', 'Total number of incomplete pathways']
).properties(
    width=600,
    height=300
)

# Display the chart
st.altair_chart(chart, use_container_width=True)
