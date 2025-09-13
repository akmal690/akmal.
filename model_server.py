# model_server.py (Flask API)
from flask import Flask, request, jsonify
import joblib
import mysql.connector
from azure_fraud import AzureFraudService
import pandas as pd
import json

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "shop_db"
}

app = Flask(__name__)
model = joblib.load('fraud_model.pkl')
azure = AzureFraudService()

@app.route('/verify', methods=['POST'])
def verify_order():
    data = request.json
    user_data = get_user_data(data['user_id'])
    
    features = {
        'typing_speed': data['typing_speed'],
        'time_on_page': data['time_on_page'],
        'payment_type': data['payment_type'],
        'order_count': user_data['order_count'],
        'avg_typing_speed': user_data['avg_typing_speed'],
        'user_age': user_data['user_age']
    }
    
    local_pred = model.predict(pd.DataFrame([features]))[0]
    azure_features = [data['typing_speed'], data['time_on_page'], user_data['order_count']]
    azure_result = azure.analyze_behavior(azure_features)
    
    if local_pred or any(azure_result):
        log_fraud_attempt(data['user_id'], features)
        return jsonify({
            'decision': 'block',
            'reason': 'suspicious_activity',
            'details': {
                'local_score': model.predict_proba(pd.DataFrame([features]))[0][1],
                'azure_anomalies': azure_result
            }
        })
    
    return jsonify({'decision': 'allow'})

def get_user_data(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT order_count, avg_typing_speed, 
               TIMESTAMPDIFF(DAY, created_at, NOW()) AS user_age 
        FROM users WHERE id = %s
    """, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def log_fraud_attempt(user_id, features):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO fraud_attempts 
        (user_id, features, detected_at)
        VALUES (%s, %s, NOW())
    """, (user_id, json.dumps(features)))
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# azure_fraud.py
class AzureFraudService:
    def __init__(self):
        pass

    def analyze_behavior(self, features):
        # Dummy implementation
        return [False]

