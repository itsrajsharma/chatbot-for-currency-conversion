from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "fca_live_C1MVGIrEYpuhHNSeTXJFtfZ1p65OOG7BZjK5EYuA"
BASE_URL = "https://api.freecurrencyapi.com/v1/latest"

def fetch_conversion_factor(source, target):
    try:
        url = f"{BASE_URL}?apikey={API_KEY}&base_currency={source}&currencies={target}"
        response = requests.get(url)
        data = response.json()

        if "data" in data and target in data["data"]:
            return data["data"][target]
        else:
            return None
    except Exception as e:
        print("API Error:", str(e))
        return None

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    
    try:
        source_currency = data['queryResult']['parameters']['unit-currency']['currency']
        amount = data['queryResult']['parameters']['unit-currency']['amount']
        target_currency = data['queryResult']['parameters']['currency-name']

        cf = fetch_conversion_factor(source_currency, target_currency)

        if cf is None:
            return jsonify({
                "fulfillmentText": "Error! Unable to fetch conversion rate. Try again later."
            })

        final_amount = round(amount * cf, 2)

        return jsonify({
            "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
        })

    except Exception as e:
        print("Error in webhook:", str(e))
        return jsonify({
            "fulfillmentText": "Error! Servers might be down. Please visit https://www.xe.com/currencyconverter/"
        })

if __name__ == "__main__":
    app.run(debug=True)
