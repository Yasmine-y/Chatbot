from flask import Flask, jsonify

app = Flask(__name__)

user_accounts = {
    "Yasmine Charradi": ["Account 1", "Account 2","Account 3","Account 4","Account 5","Account 6","Account 7","Account 8","Account 9"],
    "John Doe": ["Account 1", "Account 2"]
}

user_balance = {
    "Yasmine Charradi": {
    "Account 1": "balance 1",
    "Account 2": "balance 2",
    "Account 3": "balance 3",
    "Account 4": "balance 4",
    "Account 5": "balance 5",
    "Account 6": "balance 6",
    "Account 7": "balance 7",
    "Account 8": "balance 8",
    "Account 9": "balance 9",
    },
    "John Doe": {
    "Account 1": "balance 1",
    "Account 2": "balance 2",
    }
}

@app.route('/accounts/<username>', methods=['GET'])
def get_user_accounts(username):
    accounts = user_accounts.get(username)
    if accounts:
        return jsonify({"accounts": accounts})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/accounts/<username>/<number>', methods=['GET'])
def get_user_balance(username, number):
   balance = user_balance.get(username).get(number)
   if balance:
       return jsonify({"balance": balance})
   else:
       return jsonify({"error": "User not found"}), 404



if __name__ == '__main__':
    app.run(debug=True,port=8080)
