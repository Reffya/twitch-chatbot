from flask import Flask, jsonify, request
import time

app = Flask(__name__)

last_alert = {"value" : "", "timestamp" : time.time()}

@app.route('/put-alert', methods=['POST'])
def put_alert():
    data = request.json
    last_alert.update({"value" : data["alert"], "timestamp" : time.time()*1000})
    return jsonify(success=True)

@app.route('/get-alert', methods=['GET'])
def get_alert():
    return jsonify(last_alert)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
