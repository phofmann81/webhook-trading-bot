from chalice import Chalice
from chalicelib.alpaca_secrets import get_alpaca_credentials
import requests
import json

app = Chalice(app_name="tradingview-webhook-alerts")
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = "{}/v2/orders".format(BASE_URL)
HEADERS = get_alpaca_credentials()


@app.route("/alpaca_order", methods=["POST"], api_key_required=True)
def alpaca_order():
    request = app.current_request

    webhook_message = request.json_body

    data = {
        "symbol": webhook_message["ticker"],
        "qty": 1,
        "side": "buy",
        "type": "limit",
        "limit_price": webhook_message["close"],
        "time_in_force": "gtc",
        "order_class": "bracket",
        "take_profit": {"limit_price": webhook_message["close"] * 1.05},
        "stop_loss": {
            "stop_price": webhook_message["close"] * 0.98,
        },
    }

    r = requests.post(ORDERS_URL, json=data, headers=HEADERS)

    response = json.loads(r.content)

    return {
        "webhook_message": webhook_message,
        "response": response,
    }
