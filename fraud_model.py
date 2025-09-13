import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import mysql.connector

def load_training_data():
    conn = mysql.connector.connect(**db_config)
    query = """ ... """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = pd.read_csv('ai_orders_training.csv')
payment_map = {'cash on delivery': 0, 'credit card': 1, 'paytm': 2, 'paypal': 3}
df['payment_code'] = df['payment_type'].str.lower().map(payment_map)
X = df[['typing_speed', 'time_on_page', 'payment_code']]
y = df['is_fraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)
joblib.dump(model, 'fraud_detection_model.pkl')