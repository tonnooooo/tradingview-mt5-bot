from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Webhook attivo!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Ricevuto:", data)

    # INDIRIZZO DEL TUO PC (se sei in locale, usa IP locale)
    try:
        res = requests.post("http://192.168.1.41:8000/order", json=data)
        return jsonify({"status": "inviato", "response": res.text})
    except Exception as e:
        return jsonify({"errore": str(e)})

if __name__ == '__main__':
    app.run()
