import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


df = pd.read_csv("cleaned_vehicles.csv")# read csv

taxi_management_data = {
            "Cab Management Group, Inc.": 139,
            "Chicago Taxicab Management Inc.": 89,
            "Medallion Leasing and Management, Inc.": 340,
            "Medallion Management Corp.": 2,
            "Owner Manager": 3416,
            "Owner-Operator": 1937,
            "Star North Management LLC": 180,
            "Sun Financial Services, Inc.": 129,
            "Taxi Experts, Inc.": 2,
            "Top Cab Corp.": 122,
            "none": 5693
}


illinois_df = df[df['State'] == 'IL']
city_model_counts = illinois_df.groupby('City').size().reset_index(name='Vehicle Count')


latitudes = df.set_index('City')['Latitude'].to_dict()  
longitudes = df.set_index('City')['Longitude'].to_dict()  


app = Dash(__name__) # run app


app.layout = html.Div([
    html.Div([
        html.H1("Vehicles Distribution Dashboard for State of IL (illinois)", style={'textAlign': 'center','fontSize': '28px', 'fontFamily': 'Ariel, sans-serif'}),

        # city filter
        html.Div([
            html.Label("Select a City:"),
            dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': city, 'value': city} for city in df['City'].unique()],
                value=None,  
                placeholder="Filter by city",
                clearable=True
            ),
        ], style={'width': '200px', 'display': 'inline-block', 'padding': '20px', 'align-self': 'center', 'float': 'right','marginRight': '20px'})
    ], style={'width': '100%', 'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginLeft': '20px'}), 
    
    html.Div(id='key-metrics', style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px'}),

    #most popular make 
    html.Div(id='popular-make-model', style={
        'marginTop': '20px',
        'width': '95%', 'display': 'inline-block', 'padding': '20px', 'verticalAlign': 'top',
        'border': '1px solid #ddd', 'borderRadius': '10px', 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)',
        'textAlign': 'center', 'marginLeft': '20px'
    }),

    # pie Charts div
html.Div([
    # fuel sourc pie chart
    html.Div([
        
        dcc.Graph(id='fuel-source-pie')
    ], style={
        'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'margin': '16px', 'flex': '1',
        'textAlign': 'center'
    }),

    
    html.Div([
        dcc.Graph(id='wheelchair-access-pie')# Wheelchair accessibility Ppirchat
    ], style={
        'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'margin': '16px', 'flex': '1',
        'textAlign': 'center'
    }),
], style={
    'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px','marginRight': '15px','marginLeft': '5px'
}),

   # div for bar charts
html.Div([
    
    html.Div([
        dcc.Graph(id='status-bar')# Status Bar Chart
    ], style={
        'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'margin': '16px', 'flex': '1',
        'textAlign': 'center'
    }),

    # Vehicle type barchart
    html.Div([
        dcc.Graph(id='vehicle-type-bar')
    ], style={
        'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
        'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'margin': '16px', 'flex': '1',
        'textAlign': 'center'
    }),
], style={
    'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px','marginRight': '15px','marginLeft': '5px'
}),


# Map Visualization vehicle numbers
html.Div([
    dcc.Graph(id='city-vehicle-model-map')
], style={
    'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'margin': '16px', 'width': '90%', 'marginLeft': 'auto', 'marginRight': 'auto'
})
]),





@app.callback(
    [
        Output('key-metrics', 'children'),
        Output('fuel-source-pie', 'figure'),
        Output('wheelchair-access-pie', 'figure'),
        Output('status-bar', 'figure'),
        Output('vehicle-type-bar', 'figure'),
        Output('city-vehicle-model-map', 'figure'),
        Output('popular-make-model', 'children'),
      
       
    ],
    [Input('city-dropdown', 'value')]
)
def update_dashboard(selected_city):
    # city dropdown filtr
    filtered_df = df if selected_city is None else df[df['City'] == selected_city]

    
    total_vehicles = len(filtered_df)
    total_unique_makes = filtered_df['Vehicle Make'].nunique()
    wheelchair_accessible_pct = (
        filtered_df['Wheelchair Accessible'].value_counts(normalize=True).get('Y', 0) * 100
    )
    average_model_year = filtered_df['Vehicle Model Year'].median()

    key_metrics = [
        html.Div([
            html.H4("Total Vehicles",style={'fontSize': '18px', 'fontFamily': 'Arial, sans-serif'}),
            html.H2(f"{total_vehicles}", style={'color': '#007bbf', 'fontSize': '32px', 'fontFamily': 'Verdana, sans-serif'}),
        ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
                  'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'textAlign': 'center', 'width': '20%'}),
        html.Div([
            html.H4("Unique Vehicle Makes", style={'fontSize': '18px', 'fontFamily': 'Arial, sans-serif'}),
            html.H2(f"{total_unique_makes}", style={'color': '#007bff', 'fontSize': '32px', 'fontFamily': 'Verdana, sans-serif'}),
        ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
                  'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'textAlign': 'center', 'width': '20%'}),
        html.Div([
            html.H4("Wheelchair Accessible",style={'fontSize': '18px', 'fontFamily': 'Arial, sans-serif'}),
            html.H2(f"{wheelchair_accessible_pct:.2f}%", style={'color': '#17a2b8', 'fontSize': '32px', 'fontFamily': 'Verdana, sans-serif'}),
        ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
                  'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'textAlign': 'center', 'width': '20%'}),
        html.Div([
            html.H4("Average Model Year",style={'fontSize': '18px', 'fontFamily': 'Arial, sans-serif'}),
            html.H2(f"{average_model_year:.0f}", style={'color': '#6c757d','fontSize': '32px', 'fontFamily': 'Verdana, sans-serif'}),
        ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px',
                  'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)', 'textAlign': 'center', 'width': '20%'}),
    ]

    # Piecharts
    fuel_pie = px.pie(
        filtered_df, names='Vehicle Fuel Source', title='Vehicle Fuel Source Distribution',
        color_discrete_sequence=px.colors.qualitative.Pastel,hole=0.7
    )
    
    filtered_df['Wheelchair Accessible Label'] = filtered_df['Wheelchair Accessible'].map({'Y': 'Yes', 'N': 'No'})


    wheelchair_pie = px.pie(
        filtered_df, 
        names='Wheelchair Accessible Label', 
        title='Wheelchair Accessibility',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # BarCharts
    status_counts = filtered_df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    status_bar = px.bar(
        status_counts, x='Status', y='Count',
        labels={'Status': 'Status', 'Count': 'Count'},
        title='Count of Vehicles by Status',
        color_discrete_sequence=['#636EFA']
    )

    vehicle_type_counts = filtered_df['Vehicle Type'].value_counts().reset_index()
    vehicle_type_counts.columns = ['Vehicle Type', 'Count']
    vehicle_type_bar = px.bar(
        vehicle_type_counts, x='Count', y='Vehicle Type',
        labels={'Vehicle Type': 'Vehicle Type', 'Count': 'Count'},
        title='Count of Vehicles by Type',
        color_discrete_sequence=['#EF553B']
    )

    # map of state
    city_model_map = px.scatter_mapbox(
        city_model_counts,
        lat=[latitudes.get(city, None) for city in city_model_counts['City']],
        lon=[longitudes.get(city, None) for city in city_model_counts['City']],
        size=city_model_counts['Vehicle Count'],
        color=city_model_counts['Vehicle Count'],
        title='Vehicle Model Counts by City in Illinois',
        color_continuous_scale="Viridis",
        size_max=15,
        zoom=5,
        mapbox_style="open-street-map"
    )
    
    # popular model 
    if selected_city is None:
        most_popular_make = df['Vehicle Make'].value_counts().idxmax()
        most_popular_model = df['Vehicle Model'].value_counts().idxmax()
        most_popular_year = df['Vehicle Model Year'].value_counts().idxmax()
        most_popular_color = df['Vehicle Color'].value_counts().idxmax()
        popular_make_model = html.Div([
            html.H4("Most Popular Make - Model - Year - Color (State-wide)",style={'fontSize': '18px', 'fontFamily': 'Helvetica, sans-serif'}),
            html.H2(f"{most_popular_make} - {most_popular_model} - {most_popular_year} - {most_popular_color}", style={'color': '#ff5733','fontSize': '25px', 'fontFamily': 'Verdana, sans-serif'}),
        ])
    else:
        most_popular_make = filtered_df['Vehicle Make'].value_counts().idxmax()
        most_popular_model = filtered_df['Vehicle Model'].value_counts().idxmax()
        most_popular_year = filtered_df['Vehicle Model Year'].value_counts().idxmax()
        most_popular_color = filtered_df['Vehicle Color'].value_counts().idxmax()
        popular_make_model = html.Div([
            html.H4("Most Popular Make - Model - Year - Color",style={'fontSize': '18px', 'fontFamily': 'Helvetica, sans-serif'}),
            html.H2(f"{most_popular_make} - {most_popular_model} - {most_popular_year} - {most_popular_color}", style={'color': '#ff5733','fontSize': '25px', 'fontFamily': 'Verdana, sans-serif'}),
        ])

   
    
    return key_metrics, fuel_pie, wheelchair_pie, status_bar, vehicle_type_bar, city_model_map, popular_make_model


if __name__ == "__main__":
    app.run_server(debug=True)
