from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Bot attivo!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Ricevuto:", data)
    # Puoi aggiungere elaborazione, validazioni, invio a MT5, ecc.
    return "OK", 200
