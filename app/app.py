import requests
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

API_KEY = '95225285c336cae7d2d73db3'  # Your API key from Exchangerate-API
BASE_URL = 'https://v6.exchangerate-api.com/v6/'

def get_supported_currencies():
    url = f"{BASE_URL}{API_KEY}/codes"
    response = requests.get(url)
    data = response.json()
    
    if data['result'] == 'success':
        return [currency[0] for currency in data['supported_codes']]
    else:
        raise Exception("Error retrieving supported currencies")

def get_exchange_rate(base_currency, target_currency, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['result'] == 'success':
                exchange_rate = data['conversion_rates'][target_currency]
                return exchange_rate
            else:
                raise Exception("Error retrieving exchange rate")
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            retries += 1
            time.sleep(2)  # Wait for 2 seconds before retrying
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(2)  # Wait for 2 seconds before retrying

    print(f"Failed to fetch exchange rate after {max_retries} retries.")
    return None

@app.route('/')
def index():
    try:
        currencies = get_supported_currencies()
        return render_template('index.html', currencies=currencies)
    except Exception as e:
        return str(e)

@app.route('/convert', methods=['POST'])
def convert_currency():
    amount = float(request.form['amount'])
    base_currency = request.form['base_currency'].upper()
    target_currency = request.form['target_currency'].upper()
    
    try:
        exchange_rate = get_exchange_rate(base_currency, target_currency)
        if exchange_rate is not None:
            converted_amount = round(amount * exchange_rate, 2)
            return jsonify({
                'converted_amount': f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}"
            })
        else:
            return jsonify({'error': "Currency conversion failed. Please try again."})
    except Exception as e:
        return jsonify({'error': f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
