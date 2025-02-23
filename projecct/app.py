from flask import Flask, render_template
import requests
from decimal import Decimal
from forms import CurrencyForm
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_exchange_rate(from_currency, to_currency):
    """Fetch exchange rates from API with error handling."""
    url = Config.API_URL.format(Config.API_KEY, from_currency)
    print(f"[DEBUG] Requesting URL: {url}")

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        print("[ERROR] Connection Error:", e)
        return None

    print(f"[DEBUG] Response Status Code: {response.status_code}")
    print(f"[DEBUG] Response Text: {response.text}")

    # Check HTTP status
    if response.status_code != 200:
        print("[ERROR] Non-200 response")
        return None

    # Attempt to parse JSON
    try:
        data = response.json()
    except ValueError as e:
        print("[ERROR] JSON Decode Error:", e)
        return None

    # Check if the API returned a success result
    if data.get("result") == "success":
        rates = data.get("conversion_rates", {})
        print(f"[DEBUG] Conversion Rates Available: {list(rates.keys())}")
        return rates.get(to_currency)
    else:
        print("[ERROR] API returned an error:", data)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    form = CurrencyForm()
    conversion_result = None

    if form.validate_on_submit():
        from_currency = form.from_currency.data.upper()
        to_currency = form.to_currency.data.upper()
        amount = form.amount.data

        print(f"[DEBUG] From Currency: {from_currency}")
        print(f"[DEBUG] To Currency: {to_currency}")
        print(f"[DEBUG] Amount: {amount}")

        exchange_rate = get_exchange_rate(from_currency, to_currency)
        if exchange_rate:
            print(f"[DEBUG] Received Exchange Rate: {exchange_rate}")
            # Multiply the amount by the exchange rate.
            conversion_result = round(amount * Decimal(str(exchange_rate)), 2)
            print(f"[DEBUG] Conversion Result: {conversion_result}")
        else:
            conversion_result = "Invalid currency code or API error."
            print("[ERROR] No valid exchange rate found.")

    return render_template("index.html", form=form, result=conversion_result)

if __name__ == "__main__":
    app.run(debug=True)