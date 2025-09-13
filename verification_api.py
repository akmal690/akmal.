from flask import Flask, request, jsonify
import joblib
import mysql.connector
from datetime import datetime
import numpy as np

app = Flask(__name__)

# Load the trained fraud detection model
model = joblib.load('fraud_detection_model.pkl')
# Map for converting payment types
payment_map = {"cash on delivery": 0, "credit card": 1, "paytm": 2, "paypal": 3}

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='shop_db'
    )

@app.route('/verify', methods=['POST'])
def verify_order():
    data = request.json
    try:
        # Extract features sent from client
        typing_speed = float(data['typing_speed'])
        time_on_page = float(data['time_on_page'])
        payment_type = data['payment_type']
        payment_code = payment_map.get(payment_type.lower(), -1)
        user_id = data['user_id']

        # Create input feature array for prediction
        features = np.array([[typing_speed, time_on_page, payment_code]])
        prediction = int(model.predict(features)[0])
        decision = "allow" if prediction == 1 else "block"

        # Log the verification attempt into MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO verification_logs 
            (user_id, typing_speed, time_on_page, payment_type, verification_result, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, typing_speed, time_on_page, payment_type, decision, datetime.now()))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"decision": decision, "reason": "Verification successful"})
    except Exception as e:
        return jsonify({"decision": "block", "reason": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)