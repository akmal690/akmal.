import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset
df = pd.read_csv('ai_orders_training.csv')

# Encode payment_type to match your app.py mapping
payment_map = {'cash on delivery': 0, 'credit card': 1, 'paytm': 2, 'paypal': 3}
df['payment_code'] = df['payment_type'].str.lower().map(payment_map)

# Prepare features and target
X = df[['typing_speed', 'time_on_page', 'payment_code']]
y = df['is_fraud']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'fraud_detection_model.pkl')

# Optional: print accuracy
print("Test accuracy:", model.score(X_test, y_test))