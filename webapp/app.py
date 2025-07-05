import os
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'nifty50_sample.csv')
API_KEY = os.environ.get('INDIAN_STOCK_API_KEY', 'demo')


def load_data():
    return pd.read_csv(DATA_FILE)


@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', tables=[data.to_html(classes='data')], api_key=API_KEY)


if __name__ == '__main__':
    app.run(debug=True)
