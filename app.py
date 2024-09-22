from flask import Flask, render_template, request, jsonify, session
import requests

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"
app = Flask(__name__)
app.secret_key = 'my_secret_key'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json['message']
    print("user message: ", user_message)


    rasa_reponse = requests.post(RASA_API_URL, json={'message': user_message})

    messages = rasa_reponse.json()


    combined_messages = ""
    for message in messages:
        combined_messages += message.get('text', '') + "\n"
    return jsonify({'response': combined_messages.strip()})


if __name__ == '__main__':
    app.run(debug=True)