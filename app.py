import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend

import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import os
from predictions import daily_predictions, yearly_predictions  # Import your prediction data

app = Flask(__name__)

# Ensure the 'static' folder exists to store images
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    graph_url = None

    if request.method == 'POST':
        # Get user input: daily or yearly prediction
        prediction_type = request.form.get('prediction_type')

        # Get the corresponding predictions
        if prediction_type == 'daily':
            prediction = daily_predictions
        elif prediction_type == 'yearly':
            prediction = yearly_predictions

        # Plot the graph based on the predictions
        filename = f'static/eth_prediction.png'
        plot_graph(prediction, prediction_type, filename)

        # Pass the graph URL to the template
        graph_url = filename

    return render_template('index.html', prediction=prediction, graph_url=graph_url)

def plot_graph(data, prediction_type, filename):
    """Plot the graph and save it to the static folder"""
    plt.figure(figsize=(10, 5))
    plt.plot(data, marker='o')
    plt.title(f'Ethereum Price Prediction ({prediction_type.capitalize()})')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)

    # Save the graph as a PNG file
    plt.savefig(filename)
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)