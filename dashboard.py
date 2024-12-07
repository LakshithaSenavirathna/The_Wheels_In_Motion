import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Read the dataset
df = pd.read_csv('cleaned_vehicles.csv')  # Update the file path if needed

df['Status'] = df['Status'].astype('category')
df['Vehicle Type'] = df['Vehicle Type'].astype('category')
df['City'] = df['City'].astype('category')
df['Wheelchair Accessible'] = df['Wheelchair Accessible'].astype('category')

# Vehicle Count by Status
status_counts = df['Status'].value_counts().reset_index()
status_counts.columns = ['Status', 'count']  # Renaming for clarity
status_fig = px.bar(status_counts, x='Status', y='count', labels={'Status': 'Vehicle Status', 'count': 'Vehicle Count'}, title="Vehicle Count by Status")

# Vehicle Type Distribution
vehicle_type_counts = df['Vehicle Type'].value_counts().reset_index()
vehicle_type_counts.columns = ['Vehicle Type', 'count']  # Renaming for clarity
vehicle_type_fig = px.pie(vehicle_type_counts, names='Vehicle Type', values='count', title="Vehicle Type Distribution")

# Wheelchair Accessible Distribution (Pie chart)
wheelchair_counts = df['Wheelchair Accessible'].value_counts().reset_index()
wheelchair_counts.columns = ['Wheelchair Accessible', 'count']  # Renaming for clarity
wheelchair_fig = px.pie(wheelchair_counts, names='Wheelchair Accessible', values='count', title="Wheelchair Accessible Vehicle Distribution")

# Map of Illinois with city counts and color shading
# For this example, we'll assume that the 'City' column has city names.
# You will need a GeoJSON of Illinois' city boundaries to correctly visualize this data.
# Here, we use a placeholder for city count visualization with color shading.
illinois_geojson = '/path/to/illinois_cities.geojson'  # Replace with actual GeoJSON file path

# Create a city count per city (this could be vehicle count or another metric)
city_counts = df['City'].value_counts().reset_index()
city_counts.columns = ['City', 'count']

# Merge the city counts with the GeoJSON data to display on the map
# For the purpose of this example, let's assume the GeoJSON file has 'city' as a key for cities
# Merge with GeoJSON data and display map based on the counts

map_fig = px.choropleth(city_counts, 
                        geojson=illinois_geojson, 
                        locations='City', 
                        color='count',
                        hover_name='City',
                        color_continuous_scale="Viridis",
                        title="City Counts in Illinois")

# Layout of the dashboard with City filter
app.layout = html.Div([
    html.H1("Vehicle Dashboard"),
    
    # Dropdown to filter by city
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['City'].unique()],
        value=df['City'].unique()[0],  # Default value (first city)
        multi=False
    ),
    
    # Bar chart for Vehicle Count by Status
    dcc.Graph(id='status-graph', figure=status_fig),
    
    # Pie chart for Vehicle Type Distribution
    dcc.Graph(id='vehicle-type-graph', figure=vehicle_type_fig),
    
    # Pie chart for Wheelchair Accessible Distribution
    dcc.Graph(id='wheelchair-graph', figure=wheelchair_fig),
    
    # Map of Illinois with city counts and color shading
    dcc.Graph(id='illinois-map', figure=map_fig),
])

# Callback to update graphs based on selected city
@app.callback(
    [dash.dependencies.Output('status-graph', 'figure'),
     dash.dependencies.Output('vehicle-type-graph', 'figure'),
     dash.dependencies.Output('wheelchair-graph', 'figure')],
    [dash.dependencies.Input('city-dropdown', 'value')]
)
def update_graphs(selected_city):
    # Filter the dataframe based on the selected city
    filtered_df = df[df['City'] == selected_city]

    # Vehicle Count by Status
    status_counts = filtered_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'count']
    status_fig = px.bar(status_counts, x='Status', y='count', labels={'Status': 'Vehicle Status', 'count': 'Vehicle Count'}, title=f"Vehicle Count by Status ({selected_city})")

    # Vehicle Type Distribution
    vehicle_type_counts = filtered_df['Vehicle Type'].value_counts().reset_index()
    vehicle_type_counts.columns = ['Vehicle Type', 'count']
    vehicle_type_fig = px.pie(vehicle_type_counts, names='Vehicle Type', values='count', title=f"Vehicle Type Distribution ({selected_city})")

    # Wheelchair Accessible Distribution
    wheelchair_counts = filtered_df['Wheelchair Accessible'].value_counts().reset_index()
    wheelchair_counts.columns = ['Wheelchair Accessible', 'count']
    wheelchair_fig = px.pie(wheelchair_counts, names='Wheelchair Accessible', values='count', title=f"Wheelchair Accessible Vehicle Distribution ({selected_city})")

    return status_fig, vehicle_type_fig, wheelchair_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)