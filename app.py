from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data is None:
        return jsonify({'error': 'No data'}), 400

    action = data.get("action")
    if action == "buy":
        requests.get("http://localhost:3000/open_order?action=buy")
    elif action == "sell":
        requests.get("http://localhost:3000/open_order?action=sell")
    return jsonify({'status': 'ok'})
