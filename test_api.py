import requests
import json

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/health')
        print("Health Check:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Health check failed: {e}")

def test_model_info():
    """Test the model info endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/model-info')
        print("Model Info:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Model info failed: {e}")

def test_verify():
    """Test the verify endpoint"""
    try:
        data = {
            "user_id": 1,
            "typing_speed": 45.5,
            "time_on_page": 120,
            "payment_type": "credit card"
        }
        response = requests.post('http://127.0.0.1:5000/verify', json=data)
        print("Verify Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Verify test failed: {e}")

def test_fraud_attempts():
    """Test the fraud attempts endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/fraud-attempts')
        print("Fraud Attempts:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Fraud attempts test failed: {e}")

def test_accuracy():
    """Test the accuracy endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/accuracy')
        print("Accuracy Metrics:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            metrics = data['accuracy_metrics']
            print(f"Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"Precision: {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
            print(f"Recall: {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
            print(f"F1-Score: {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
        else:
            print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Accuracy test failed: {e}")

def test_detailed_accuracy():
    """Test the detailed accuracy endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/accuracy/detailed')
        print("Detailed Accuracy Metrics:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            metrics = data['detailed_metrics']
            print(f"Accuracy: {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"Confusion Matrix: {metrics['confusion_matrix']}")
            print(f"Cross-validation Mean: {metrics['cross_validation']['mean_accuracy']:.4f}")
        else:
            print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Detailed accuracy test failed: {e}")

def test_performance_summary():
    """Test the performance summary endpoint"""
    try:
        response = requests.get('http://127.0.0.1:5000/performance-summary')
        print("Performance Summary:")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            summary = data['performance_summary']
            print(f"Model Type: {summary['model_info']['model_type']}")
            print(f"Features: {summary['model_info']['feature_names']}")
        else:
            print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Performance summary test failed: {e}")

if __name__ == "__main__":
    print("Testing API Endpoints...")
    print("=" * 50)
    
    test_health()
    test_model_info()
    test_verify()
    test_fraud_attempts()
    test_accuracy()
    test_detailed_accuracy()
    test_performance_summary()
    
    print("Testing completed!") 