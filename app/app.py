#!/usr/bin/env python3
"""Initialize and configure flask instance of the app"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from exchange_rate import get_exchange_rate as fetch_exchange_rate

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=['GET'], strict_slashes=False)
def home_page():
    return render_template("index.html")

@app.route("/", methods=['POST'], strict_slashes=False)
def get_rate():
    data = request.get_json()
    amount = float(data['amount'])
    source_currency = data['source_currency']
    target_currency = data['target_currency']
    print(amount, source_currency, target_currency)

    exchange_rate = fetch_exchange_rate(source_currency, target_currency)
    if exchange_rate is not None:
        converted_amount = round(amount * exchange_rate, 2)
        return jsonify({'converted_amount': converted_amount})
    else:
        return jsonify({'error': 'Failed to fetch exchange rate'}), 500

if __name__ == "__main__":
    app.run()
