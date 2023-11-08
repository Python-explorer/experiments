import streamlit as st
import pandas as pd
import altair as alt

# The URL of the raw CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/ElectiveDataICB.csv'

@st.cache
def load_data(url):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(url)
    # Handle thousands separator if present and convert to numeric
    data['Total number of incomplete pathways'] = pd.to_numeric(
        data['Total number of incomplete pathways'].str.replace(',', ''), errors='coerce')
    data['Total 65 plus weeks'] = pd.to_numeric(
        data['Total 65 plus weeks'].str.replace(',', ''), errors='coerce')
    # Replace 'INTEGRATED CARE BOARD' with 'ICB' in the 'ICB Name' column
    data['ICB Name'] = data['ICB Name'].str.replace('INTEGRATED CARE BOARD', 'ICB')
    return data

# Load the data
df = load_data(csv_url)

# Sidebar title
st.sidebar.header('ICB Electives Dashboard Demo')

# Sidebar dropdown for selecting the value column
selected_value_column = st.sidebar.selectbox(
    'Select the column for bar values',
    options=['Total number of incomplete pathways', 'Total 65 plus weeks']
)

# Sidebar dropdown for selecting the Treatment Function
selected_treatment_function = st.sidebar.selectbox(
    'Select the Treatment Function',
    options=df['Treatment Function'].unique()
)

# Sidebar dropdown for ICB focus
selected_icb_focus = st.sidebar.selectbox(
    'ICB focus',
    options=['None'] + list(df['ICB Name'].unique())
)

# Filter the DataFrame to exclude 'NHS ENGLAND' from 'ICB Name'
df_filtered = df[(df['ICB Name'] != 'NHS ENGLAND') & (df['Treatment Function'] == selected_treatment_function)]

# Group by 'ICB Name' and sum the selected value column
df_grouped = df_filtered.groupby('ICB Name')[selected_value_column].sum().reset_index()

# Sort the grouped data by the selected value column in ascending order for the bar chart
df_sorted = df_grouped.sort_values(by=selected_value_column, ascending=True)

# Prepare the Altair chart
chart = alt.Chart(df_sorted).mark_bar().encode(
    x='ICB Name:N',
    y=f'{selected_value_column}:Q',
    tooltip=['ICB Name:N', f'{selected_value_column}:Q'],
    color=alt.condition(
        alt.datum['ICB Name'] == selected_icb_focus,  # Condition for changing color
        alt.value('paleblue'),  # The color for selected ICB
        alt.value('lightgray')  # The default color
    )
).properties(
    width=700  # Adjust the width as necessary
)

# Display the Altair chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)
