import requests
import time

API_KEY = '95225285c336cae7d2d73db3'  # Your API key from Exchangerate-API
BASE_URL = 'https://v6.exchangerate-api.com/v6/'

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

def convert_currency():
    print("Welcome to the Currency Converter App")
    
    # Get source and target currencies
    base_currency = input("Enter the base currency (e.g., USD): ").upper()
    target_currency = input("Enter the target currency (e.g., EUR): ").upper()

    # Get amount to convert
    while True:
        try:
            amount = float(input("Enter the amount to convert: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    # Fetch exchange rate
    exchange_rate = get_exchange_rate(base_currency, target_currency)

    if exchange_rate is not None:
        # Convert currency
        converted_amount = round(amount * exchange_rate, 2)
        print(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
    else:
        print("Currency conversion failed. Please try again.")

# Main function
def main():
    while True:
        convert_currency()
        choice = input("Do you want to convert another currency? (yes/no): ").lower()
        if choice != 'yes':
            print("Thank you for using the Currency Converter App!")
            break

if __name__ == "__main__":
    main()
