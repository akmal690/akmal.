import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Generate synthetic training data (replace with your labeled data)
np.random.seed(42)
n_samples = 1000
data = pd.DataFrame({
    'typing_speed': np.random.normal(50, 20, n_samples),  # average typing speed (keys per minute)
    'time_on_page': np.random.normal(180, 60, n_samples),   # seconds spent on page
    'payment_type': np.random.choice(['cash on delivery', 'credit card', 'paytm', 'paypal'], n_samples)
})

# Mark orders as fraudulent if they are too fast or too slow (for simulation)
data['is_fraudulent'] = (
    (data['typing_speed'] < 10) |      # very slow typing
    (data['typing_speed'] > 100) |     # unusually fast typing
    (data['time_on_page'] < 30) |      # very short time
    (data['time_on_page'] > 600)        # too long on page
).astype(int)

# Convert to allow/block (1 = allow, 0 = block/fraud)
data['label'] = 1 - data['is_fraudulent']

# Encode payment type to numeric codes for training
payment_map = {'cash on delivery': 0, 'credit card': 1, 'paytm': 2, 'paypal': 3}
data['payment_code'] = data['payment_type'].map(payment_map)

# Prepare features and label
X = data[['typing_speed', 'time_on_page', 'payment_code']]
y = data['label']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create and train RandomForest model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model
print("Model Performance:")
print(classification_report(y_test, clf.predict(X_test)))

# Save the model for later use by the Flask API
joblib.dump(clf, 'fraud_detection_model.pkl')
print("Model saved as fraud_detection_model.pkl")