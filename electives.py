import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# The URL of the raw CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/Python-explorer/experiments/main/ElectiveDataICB.csv'

@st.cache_data
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
df['ICB Name'] = df['ICB Name'].str.replace('INTEGRATED CARE BOARD', 'ICB')


# Streamlit page title
st.title('ICB Electives Dashboard Demo')

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

# Calculate quartiles for the selected value column
q1 = df_sorted[selected_value_column].quantile(0.25)
q3 = df_sorted[selected_value_column].quantile(0.75)

# Assign colors based on quartiles
colors = []
for x in df_sorted[selected_value_column]:
    if x < q1:
        colors.append('green')
    elif x < q3:
        colors.append('orange')
    else:
        colors.append('red')

# Create a vertical bar chart with increased figure size for better readability
fig, ax = plt.subplots(figsize=(18, 15))

# Plot each bar individually to set colors, including the ICB focus
for i, (icb_name, value) in enumerate(zip(df_sorted['ICB Name'], df_sorted[selected_value_column])):
    color = 'blue' if icb_name == selected_icb_focus and selected_icb_focus != 'None' else colors[i]
    ax.bar(icb_name, value, color=color)

ax.set_xlabel('ICB Name')
ax.set_ylabel(selected_value_column)
ax.set_title(f'{selected_value_column} by ICB Name for {selected_treatment_function}')
plt.xticks(rotation=45, ha='right')  # Adjust the rotation and alignment of x-axis labels

# Improve the layout to prevent label overlap
plt.tight_layout()

# Display the chart
st.pyplot(fig)
