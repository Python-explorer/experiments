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

# Calculate quartiles for the selected value column
q1 = df_grouped[selected_value_column].quantile(0.25)
q3 = df_grouped[selected_value_column].quantile(0.75)

# Define colors based on quartiles
def get_color(value, name):
    if name == selected_icb_focus and selected_icb_focus != 'None':
        return 'blue'
    elif value < q1:
        return 'green'
    elif value < q3:
        return 'orange'
    else:
        return 'red'

# Apply colors to each row based on its quartile
df_grouped['color'] = df_grouped.apply(lambda row: get_color(row[selected_value_column], row['ICB Name']), axis=1)

# Sort the grouped data by the selected value column in ascending order for the bar chart
df_grouped = df_grouped.sort_values(by=selected_value_column)

# Prepare the Altair chart
chart = alt.Chart(df_grouped).mark_bar().encode(
    x=alt.X('ICB Name:N', sort=alt.EncodingSortField(field=selected_value_column, order='ascending')),
    y=alt.Y(f'{selected_value_column}:Q'),
    color=alt.Color('color:N', scale=None),  # Use the 'color' field in the data for bar color
    tooltip=['ICB Name:N', f'{selected_value_column}:Q']
).properties(
    width=700  # Adjust the width as necessary
)

# Display the Altair chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)
