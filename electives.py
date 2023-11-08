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
    data['Total 65 plus weeks'] = pd.to_numeric(
        data['Total 65 plus weeks'].str.replace(',', ''), errors='coerce')
    return data

# Load the data
df = load_data(csv_url)


# Streamlit page title
st.title('ICB Electives Dashboard Demo')

# Dropdown to select the column for bar values
selected_value_column = st.sidebar.selectbox(
    'Select the column for bar values',
    options=['Total number of incomplete pathways', 'Total 65 plus weeks']
)

# Dropdown to select the criteria for rows
selected_treatment_function = st.sidebar.selectbox(
    'Select the Treatment Function',
    options=df['Treatment Function'].unique()
)

# Filter the DataFrame to exclude 'NHS ENGLAND' from 'ICB Name' and for the selected 'Treatment Function'
df_filtered = df[(df['ICB Name'] != 'NHS ENGLAND') & (df['Treatment Function'] == selected_treatment_function)]

# Group by 'ICB Name' and sum the selected value column
df_grouped = df_filtered.groupby('ICB Name')[selected_value_column].sum().reset_index()

# Sort the grouped data by the selected value column in ascending order for the bar chart
df_sorted = df_grouped.sort_values(by=selected_value_column, ascending=True)

# Create a vertical bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(df_sorted['ICB Name'], df_sorted[selected_value_column])
ax.set_xlabel('ICB Name')
ax.set_ylabel(selected_value_column)
ax.set_title(f'{selected_value_column} by ICB Name for {selected_treatment_function}')
plt.xticks(rotation=90)  # Rotate the x-axis labels to show them more clearly

# Display the chart
st.pyplot(fig)
