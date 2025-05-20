import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load Data
orders = pd.read_csv('olist_orders.csv', parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])
products = pd.read_csv('product_df_cleaned.csv')

# Preprocess
orders['order_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_purchase_timestamp']).dt.days

# Prepare bar chart data for order status
order_status_df = orders['order_status'].value_counts().reset_index()
order_status_df.columns = ['order_status', 'count']

# Prepare bar chart data for customer states
customer_state_df = orders['customer_state'].value_counts().reset_index()
customer_state_df.columns = ['state', 'count']

# Validate product category column
if 'product_category_name_english' not in products.columns:
    products.columns = [col.lower().strip() for col in products.columns]

# App Init
app = Dash(__name__)
server = app.server  

# Layout
app.layout = html.Div([
    html.H1("Olist E-commerce Dashboard", style={'textAlign': 'center', 'marginBottom': '40px'}),

    html.Div([
        html.Div([
            html.Div("Total Orders", style={'fontSize': '20px'}),
            html.Div(f"{orders.shape[0]:,}", style={'fontSize': '30px'})
        ], style={'backgroundColor': '#007bff', 'color': 'white', 'padding': '20px', 'borderRadius': '10px', 'textAlign': 'center'})
    ], style={'display': 'flex', 'justifyContent': 'center'}),

    html.Div([
        html.Label("Select Month:"),
        dcc.Dropdown(
            options=[{"label": month, "value": month} for month in sorted(orders['order_month'].unique())],
            value=sorted(orders['order_month'].unique())[0],
            id='month-filter'
        ),

        html.Label("Select State:"),
        dcc.Dropdown(
            options=[{"label": state, "value": state} for state in sorted(orders['customer_state'].dropna().unique())],
            value=None,
            id='state-filter',
            placeholder="Select a state (optional)",
            multi=False
        )
    ], style={'width': '60%', 'margin': '20px auto'}),

    html.Div([
        html.Div([
            dcc.Graph(id='status-bar-chart')
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                figure=px.bar(
                    products.groupby(products.columns[0]).size().nlargest(10).reset_index(name='count'),
                    x=products.columns[0], y='count',
                    labels={products.columns[0]: 'Product Category'},
                    title="Top Product Categories"
                )
            )
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),

    html.Div([
        html.Div([
            dcc.Graph(
                figure=px.histogram(
                    orders.dropna(subset=['delivery_time']),
                    x='delivery_time', nbins=40,
                    title="Delivery Time Distribution (Days)"
                )
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                figure=px.box(
                    orders.dropna(subset=['delivery_time']),
                    y='delivery_time',
                    title="Delivery Time Spread"
                )
            )
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ]),

    html.Div([
        dcc.Graph(
            figure=px.bar(
                customer_state_df,
                x='state', y='count',
                labels={'state': 'State', 'count': 'Customer Count'},
                title="Customer Distribution by State"
            )
        )
    ]),

    html.Div([
        dcc.Graph(
            figure=px.line(
                orders.groupby('order_month').size().reset_index(name='count'),
                x='order_month', y='count',
                labels={'order_month': 'Month', 'count': 'Order Volume'},
                title="Orders Over Time"
            )
        )
    ])
])

# Callbacks
@app.callback(
    Output('status-bar-chart', 'figure'),
    [Input('month-filter', 'value'),
     Input('state-filter', 'value')]
)
def update_status_chart(selected_month, selected_state):
    filtered = orders[orders['order_month'] == selected_month]
    if selected_state:
        filtered = filtered[filtered['customer_state'] == selected_state]
    data = filtered['order_status'].value_counts().reset_index()
    data.columns = ['order_status', 'count']
    fig = px.bar(data, x='order_status', y='count', title=f"Order Status for {selected_month} {f'in {selected_state}' if selected_state else ''}",
                 labels={'order_status': 'Order Status', 'count': 'Count'})
    return fig

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
