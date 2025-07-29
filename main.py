from flask import Flask, request, jsonify
from binance.client import Client
from binance.enums import *
import os

app = Flask(__name__)

API_KEY = os.environ['BINANCE_API_KEY']
API_SECRET = os.environ['BINANCE_API_SECRET_KEY']
client = Client(API_KEY, API_SECRET)

USDT_AMOUNT = 100
SYMBOL = "SOLUSDT"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    if not data or 'action' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    action = data['action']

    try:
        if action == 'buy':
            order = client.order_market_buy(
                symbol=SYMBOL,
                quoteOrderQty=USDT_AMOUNT
            )
            print("🟢 Orden de COMPRA ejecutada:", order)

        elif action == 'sell':
            balance = client.get_asset_balance(asset='SOL')
            qty = float(balance['free'])
            if qty > 0:
                order = client.order_market_sell(
                    symbol=SYMBOL,
                    quantity=round(qty, 3)
                )
                print("🔴 Orden de VENTA ejecutada:", order)
            else:
                print("⚠️ No tienes SOL disponible para vender.")
        else:
            return jsonify({'error': 'Acción no válida'}), 400

        return jsonify({'status': 'orden ejecutada', 'action': action})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
