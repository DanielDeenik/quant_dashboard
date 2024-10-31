from flask import Flask, render_template
import pandas as pd
import tensorflow as tf
from dash import dcc, html, Input, Output
from dash import Dash
import numpy as np
import dash_bootstrap_components as dbc

import plotly.graph_objs as go

# Initialize Flask and Dash
server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/dashboard/')

# Load pre-trained model
model = tf.keras.models.load_model("model/trade_model.h5")

# Example of generating predictions using the model
def predict(input_data):
    prediction = model.predict(input_data)
    return prediction

# Sample data
def generate_data():
    dates = pd.date_range(start="2024-01-01", periods=100)
    values = np.random.randn(100).cumsum()
    return pd.DataFrame({"Date": dates, "Value": values})

# Dashboard Layout
app.layout = html.Div([
    html.H1("Quant Trading Dashboard"),
    dcc.Graph(id='price-chart'),
    dcc.Interval(id="interval-component", interval=1*1000, n_intervals=0)
])

# Update chart with new data and predictions
@app.callback(Output('price-chart', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_chart(n):
    data = generate_data()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Value'], mode='lines', name='Price'))
    predictions = predict(data[['Value']].values.reshape(-1, 1))
    fig.add_trace(go.Scatter(x=data['Date'], y=predictions.flatten(), mode='lines', name='Predictions'))
    return fig

@server.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run_server(debug=True)