import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
data = pd.read_excel('Price Tracker Dataset.xlsx', sheet_name='Sheet1')

# Ensure that months are ordered correctly
data['Month'] = pd.Categorical(
    data['Month'], 
    categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], 
    ordered=True
)

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Monthly Sale Price Tracker"),

    # Dropdown for selecting multiple platforms
    html.Label("Select Platform(s):"),
    dcc.Dropdown(
        id='platform-dropdown',
        options=[
            {'label': platform, 'value': platform}
            for platform in data['Platform'].unique()
        ],
        multi=True,
        value=[data['Platform'].iloc[0]]  # Default to the first platform
    ),

    # Dropdown for selecting multiple products
    html.Label("Select Product(s):"),
    dcc.Dropdown(
        id='product-dropdown',
        options=[
            {'label': product, 'value': product}
            for product in data['Product Name'].unique()
        ],
        multi=True,
        value=[data['Product Name'].iloc[0]]  # Default to the first product
    ),

    # Graph for visualizing the sale price trend
    dcc.Graph(id='price-trend-graph')
])

# Callback for updating the graph
@app.callback(
    Output('price-trend-graph', 'figure'),
    Input('platform-dropdown', 'value'),
    Input('product-dropdown', 'value')
)
def update_graph(selected_platforms, selected_products):
    # Ensure selected_platforms and selected_products are lists
    if not isinstance(selected_platforms, list):
        selected_platforms = [selected_platforms]
    if not isinstance(selected_products, list):
        selected_products = [selected_products]

    # Filter data for the selected platforms and products
    filtered_data = data[(data['Platform'].isin(selected_platforms)) & 
                         (data['Product Name'].isin(selected_products))]
    
    # Sort data by year and month for proper plotting
    filtered_data = filtered_data.sort_values(['Year', 'Month'])

    # Create line plot
    fig = px.line(
        filtered_data, 
        x='Month', 
        y='Sale Price', 
        color='Platform',  # Differentiate by platform
        line_dash='Product Name',  # Differentiate products within platforms
        markers=True,
        title=f"Monthly Sale Price Trend for Selected Products on Selected Platforms",
        labels={
            'Month': 'Month',
            'Sale Price': 'Sale Price (in currency)',
            'Product Name': 'Product Name'
        }
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
