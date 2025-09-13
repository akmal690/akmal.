# fraud_detection.py (Scikit-Learn Model Training)
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import mysql.connector
from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import TimeSeriesPoint, UnivariateDetectionOptions
from azure.core.credentials import AzureKeyCredential

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "shop_db"
}
# Azure Configuration
AZURE_ENDPOINT = "https://your-fraud-detection.cognitiveservices.azure.com/"
AZURE_KEY = "your-azure-key"

def load_training_data():
    """Load training data from MySQL with advanced features"""
    conn = mysql.connector.connect(**db_config)
    query = """
    SELECT 
        o.typing_speed, 
        o.time_on_page, 
        o.payment_type,
        u.order_count,
        u.avg_typing_speed,
        TIMESTAMPDIFF(SECOND, u.created_at, o.created_at) AS user_age,
        o.is_fraud
    FROM orders o
    JOIN users u ON o.user_id = u.id
    """
    return pd.read_sql(query, conn)

def train_fraud_model():
    """Train and save advanced fraud detection model"""
    data = load_training_data()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('payment', OneHotEncoder(), ['payment_type']),
            ('scaler', StandardScaler(), ['typing_speed', 'time_on_page', 'order_count', 'avg_typing_speed', 'user_age'])
 ])
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=200, class_weight='balanced'))
    ])
    
    X = data.drop('is_fraud', axis=1)
    y = data['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
    model.fit(X_train, y_train)
    
    joblib.dump(model, 'fraud_model.pkl')
    print("Model trained with accuracy:", model.score(X_test, y_test))

class AzureFraudService:
    """Azure Anomaly Detection Integration"""
    def __init__(self):
        self.client = AnomalyDetectorClient(
            AZURE_ENDPOINT,
            AzureKeyCredential(AZURE_KEY)
        )
    
    def analyze_behavior(self, features):
        """Analyze behavior patterns using Azure AI"""
        # Create time series points
        series = [TimeSeriesPoint(timestamp=str(pd.Timestamp.now()), value=float(x)) for x in features]
        options = UnivariateDetectionOptions(
            series=series,
            granularity="minutely"
        )
        response = self.client.detect_entire_series(options)
        return response.is_anomaly

if __name__ == "__main__":
    train_fraud_model()

