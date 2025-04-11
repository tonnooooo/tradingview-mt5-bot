from flask import Flask, request, jsonify
import MetaTrader5 as mt5
import pytz
from datetime import datetime

app = Flask(__name__)

# === Connessione a MetaTrader 5 ===
mt5.initialize()

# === Configura la zona oraria ===
timezone = pytz.timezone("Europe/Rome")

@app.route("/", methods=["POST"])
def tradingview_webhook():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "No data received"}), 400

    signal = data.get("signal")  # Deve essere 'LONG' o 'SHORT'
    symbol = data.get("symbol", "XAUUSD")  # Modifica con il tuo simbolo
    lot = float(data.get("lot", 0.01))  # Modifica con il tuo lotto

    price = mt5.symbol_info_tick(symbol).ask if signal == "LONG" else mt5.symbol_info_tick(symbol).bid
    deviation = 20

    if signal == "LONG":
        request_data = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Long from TradingView",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    elif signal == "SHORT":
        request_data = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Short from TradingView",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    else:
        return jsonify({"error": "Invalid signal"}), 400

    result = mt5.order_send(request_data)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({"error": result.comment}), 500

    return jsonify({"status": "Order sent", "signal": signal})

if __name__ == "__main__":
    app.run(debug=False)
