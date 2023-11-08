import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# The URL of the raw CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/ElectiveDataICB.csv'

@st.cache
def load_data(url):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(url)
    # Ensure 'Total number of incomplete pathways' is numeric for sorting
    data['Total number of incomplete pathways'] = pd.to_numeric(data['Total number of incomplete pathways'], errors='coerce')
    return data

# Load the data
df = load_data(csv_url)

# Verify that we have numeric data and there's variation in the 'Total number of incomplete pathways' column
if not pd.api.types.is_numeric_dtype(df['Total number of incomplete pathways']):
    st.error('The "Total number of incomplete pathways" column does not contain numeric data.')
else:
    # Streamlit dropdown menu for 'Treatment Function'
    selected_treatment = st.selectbox(
        'Select a Treatment Function:',
        options=df['Treatment Function'].unique()
    )

    # Filter the DataFrame based on the selected treatment function
    filtered_df = df[df['Treatment Function'] == selected_treatment]

    # Sort the filtered DataFrame based on 'Total number of incomplete pathways' in descending order
    sorted_df = filtered_df.sort_values(by='Total number of incomplete pathways', ascending=False)

    # Create a vertical bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sorted_df['ICB Name'], sorted_df['Total number of incomplete pathways'])
    ax.set_xlabel('ICB Name')
    ax.set_ylabel('Total number of incomplete pathways')
    ax.set_title('Total Incomplete Pathways by ICB Name')
    plt.xticks(rotation=90)  # Rotate the x-axis labels to show them more clearly

    # Display the chart
    st.pyplot(fig)
