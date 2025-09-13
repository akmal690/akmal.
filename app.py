from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import logging
from datetime import datetime
import os
import mysql.connector
from mysql.connector import Error
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import cross_val_score, train_test_split
import numpy as np
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fraud_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'shop_db',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        return None

def save_fraud_attempt(user_id, typing_speed, time_on_page, payment_type, reason):
    """Save fraud attempt to database"""
    connection = get_db_connection()
    if not connection:
        logger.error("Could not connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO fraud_attempts (user_id, typing_speed, time_on_page, payment_type, reason, attempt_date)
        VALUES (%s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(query, (user_id, typing_speed, time_on_page, payment_type, reason))
        connection.commit()
        cursor.close()
        connection.close()
        logger.info(f"Fraud attempt saved to database for user_id: {user_id}")
        return True
    except Error as e:
        logger.error(f"Error saving fraud attempt: {e}")
        if connection:
            connection.close()
        return False

def evaluate_model_accuracy(test_data_path='ai_orders_training.csv'):
    """Evaluate model accuracy using test data"""
    try:
        # Load test data
        if not os.path.exists(test_data_path):
            return {
                "error": f"Test data file not found: {test_data_path}",
                "suggestion": "Generate test data using generate_fraud_dataset.py"
            }
        
        df = pd.read_csv(test_data_path)
        
        # Prepare features
        df['payment_code'] = df['payment_type'].map(payment_map)
        X = df[['typing_speed', 'time_on_page', 'payment_code']].values
        y = df['is_fraud'].values
        
        # Split data for evaluation
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        # Make predictions
        y_pred = model.predict(X_test)
        # Safe probability extraction for fraud class (1)
        proba_array = model.predict_proba(X_test)
        if hasattr(model, 'classes_') and 1 in list(model.classes_):
            class_index = list(model.classes_).index(1)
            y_pred_proba = proba_array[:, class_index]
        else:
            # Model missing class 1; probabilities default to 0.0
            y_pred_proba = np.zeros(shape=(proba_array.shape[0],), dtype=float)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        # Confusion matrix (ensure 2x2 even if a class is missing)
        cm = confusion_matrix(y_test, y_pred, labels=[0, 1])
        cm_dict = {
            "true_negatives": int(cm[0, 0]),
            "false_positives": int(cm[0, 1]),
            "false_negatives": int(cm[1, 0]),
            "true_positives": int(cm[1, 1])
        }
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        
        return {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "confusion_matrix": cm_dict,
            "cross_validation": {
                "mean_accuracy": round(cv_scores.mean(), 4),
                "std_accuracy": round(cv_scores.std(), 4),
                "cv_scores": [round(score, 4) for score in cv_scores]
            },
            "test_samples": len(y_test),
            "fraud_rate": round(y_test.mean(), 4),
            "classification_report": classification_report(y_test, y_pred, output_dict=True)
        }
        
    except Exception as e:
        logger.error(f"Error evaluating model accuracy: {e}")
        return {"error": str(e)}

def get_model_performance_summary():
    """Get a summary of model performance metrics"""
    if model is None:
        return {"error": "Model not loaded"}
    
    # Basic model info
    model_info = {
        "model_type": type(model).__name__,
        "feature_names": ['typing_speed', 'time_on_page', 'payment_code'],
        "payment_types": list(payment_map.keys())
    }
    
    # Try to evaluate accuracy if test data exists
    accuracy_results = evaluate_model_accuracy()
    
    return {
        "model_info": model_info,
        "accuracy_evaluation": accuracy_results
    }

# Load the trained model
try:
    model = joblib.load('fraud_detection_model.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# Payment type mapping
payment_map = {'cash on delivery': 0, 'credit card': 1, 'paytm': 2, 'paypal': 3}

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    db_status = "connected" if get_db_connection() else "disconnected"
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "database": db_status,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/verify', methods=['POST'])
def verify_order():
    """Verify order for potential fraud"""
    if model is None:
        return jsonify({
            "decision": "block",
            "reason": "Model not loaded",
            "details": {}
        }), 500

    data = request.json
    
    if not data:
        return jsonify({
            "decision": "block",
            "reason": "No data provided",
            "details": {}
        }), 400

    try:
        # Input validation
        required_fields = ['typing_speed', 'time_on_page', 'payment_type']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                "decision": "block",
                "reason": f"Missing required fields: {', '.join(missing_fields)}",
                "details": {}
            }), 400

        # Validate and convert input values
        try:
            typing_speed = float(data['typing_speed'])
            time_on_page = float(data['time_on_page'])
        except (ValueError, TypeError):
            return jsonify({
                "decision": "block",
                "reason": "Invalid numeric values for typing_speed or time_on_page",
                "details": {}
            }), 400

        # Validate ranges
        if typing_speed < 0 or typing_speed > 200:
            return jsonify({
                "decision": "block",
                "reason": "Typing speed out of valid range (0-200)",
                "details": {}
            }), 400

        if time_on_page < 0 or time_on_page > 3600:
            return jsonify({
                "decision": "block",
                "reason": "Time on page out of valid range (0-3600 seconds)",
                "details": {}
            }), 400

        payment_type = data['payment_type']
        payment_code = payment_map.get(payment_type.lower())

        if payment_code is None:
            return jsonify({
                "decision": "block",
                "reason": f"Unknown payment type: {payment_type}. Supported types: {list(payment_map.keys())}",
                "details": {}
            }), 400

        # Get user_id from request (optional)
        user_id = data.get('user_id', None)

        # Prepare features for prediction
        features = pd.DataFrame([{
            'typing_speed': typing_speed,
            'time_on_page': time_on_page,
            'payment_code': payment_code
        }])

        # Make prediction
        prediction = int(model.predict(features)[0])
        # Safe probability extraction for fraud class (1)
        proba_array = model.predict_proba(features)
        if hasattr(model, 'classes_') and 1 in list(model.classes_):
            class_index = list(model.classes_).index(1)
            proba = float(proba_array[0][class_index])
        else:
            # Model does not include class 1; treat fraud probability as 0.0
            proba = 0.0

        decision = "block" if prediction == 1 else "allow"
        reason = "Fraud detected" if prediction == 1 else "Verification successful"

        # Only save if blocked (optional)
        if decision == "block":
            logger.info(f"Saving fraud attempt: user_id={user_id}, typing_speed={typing_speed}, time_on_page={time_on_page}, payment_type={payment_type}, reason={reason}")
            save_fraud_attempt(user_id, typing_speed, time_on_page, payment_type, reason)

        # Log the verification request
        logger.info(f"Verification request: {data}")
        logger.info(f"Prediction: {prediction}, Probability: {proba:.4f}, Decision: {decision}")

        return jsonify({
            "decision": decision,
            "reason": reason,
            "saved": decision == "block", # Indicate if it was saved
            "details": {
                "fraud_probability": round(proba, 4),
                "typing_speed": typing_speed,
                "time_on_page": time_on_page,
                "payment_type": payment_type,
                "user_id": user_id
            }
        })

    except Exception as e:
        logger.error(f"Error processing verification request: {e}")
        return jsonify({
            "decision": "block",
            "reason": f"Internal server error: {str(e)}",
            "details": {}
        }), 500

@app.route('/fraud-attempts', methods=['GET'])
def get_fraud_attempts():
    """Get all fraud attempts from database"""
    connection = get_db_connection()
    if not connection:
        return jsonify({
            "error": "Database connection failed",
            "attempts": []
        }), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT fa.*, u.name as user_name, u.email as user_email
        FROM fraud_attempts fa
        LEFT JOIN users u ON fa.user_id = u.id
        ORDER BY fa.attempt_date DESC
        """
        cursor.execute(query)
        attempts = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify({
            "status": "success",
            "count": len(attempts),
            "attempts": attempts
        })
    except Error as e:
        logger.error(f"Error fetching fraud attempts: {e}")
        if connection:
            connection.close()
        return jsonify({
            "error": f"Database error: {str(e)}",
            "attempts": []
        }), 500

@app.route('/model-info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    if model is None:
        return jsonify({
            "status": "error",
            "message": "Model not loaded"
        }), 500

    return jsonify({
        "status": "loaded",
        "model_type": type(model).__name__,
        "feature_names": ['typing_speed', 'time_on_page', 'payment_code'],
        "payment_types": list(payment_map.keys()),
        "supported_payment_codes": payment_map
    })

@app.route('/accuracy', methods=['GET'])
def get_accuracy():
    """Get model accuracy metrics"""
    if model is None:
        return jsonify({
            "error": "Model not loaded"
        }), 500
    
    results = evaluate_model_accuracy()
    
    if "error" in results:
        return jsonify(results), 400
    
    return jsonify({
        "status": "success",
        "accuracy_metrics": results
    })

@app.route('/accuracy/detailed', methods=['GET'])
def get_detailed_accuracy():
    """Get detailed accuracy metrics including confusion matrix"""
    if model is None:
        return jsonify({
            "error": "Model not loaded"
        }), 500
    
    results = evaluate_model_accuracy()
    
    if "error" in results:
        return jsonify(results), 400
    
    return jsonify({
        "status": "success",
        "detailed_metrics": results
    })

@app.route('/accuracy/custom', methods=['POST'])
def evaluate_custom_data():
    """Evaluate model accuracy on custom test data"""
    if model is None:
        return jsonify({
            "error": "Model not loaded"
        }), 500
    
    data = request.json
    if not data or 'test_data' not in data:
        return jsonify({
            "error": "Please provide test_data in the request body"
        }), 400
    
    try:
        # Convert test data to DataFrame
        test_df = pd.DataFrame(data['test_data'])
        
        # Validate required columns
        required_cols = ['typing_speed', 'time_on_page', 'payment_type', 'is_fraud']
        missing_cols = [col for col in required_cols if col not in test_df.columns]
        
        if missing_cols:
            return jsonify({
                "error": f"Missing required columns: {missing_cols}"
            }), 400
        
        # Prepare features
        test_df['payment_code'] = test_df['payment_type'].str.lower().map(payment_map)
        if test_df['payment_code'].isnull().any():
            unknowns = sorted(test_df.loc[test_df['payment_code'].isnull(), 'payment_type'].unique().tolist())
            return jsonify({
                "error": f"Unknown payment_type values in test_data: {unknowns}. Supported: {list(payment_map.keys())}"
            }), 400
        X = test_df[['typing_speed', 'time_on_page', 'payment_code']].values
        y = test_df['is_fraud'].values
        
        # Make predictions
        y_pred = model.predict(X)
        # Safe probability extraction for class 1 for batch
        proba_array = model.predict_proba(X)
        if hasattr(model, 'classes_') and 1 in list(model.classes_):
            class_index = list(model.classes_).index(1)
            y_pred_proba = proba_array[:, class_index]
        else:
            y_pred_proba = np.zeros(shape=(proba_array.shape[0],), dtype=float)
        
        # Calculate metrics
        accuracy = accuracy_score(y, y_pred)
        precision = precision_score(y, y_pred, zero_division=0)
        recall = recall_score(y, y_pred, zero_division=0)
        f1 = f1_score(y, y_pred, zero_division=0)
        
        # Confusion matrix (force 2x2 shape)
        cm = confusion_matrix(y, y_pred, labels=[0, 1])
        
        return jsonify({
            "status": "success",
            "metrics": {
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1, 4),
                "confusion_matrix": {
                    "true_negatives": int(cm[0, 0]),
                    "false_positives": int(cm[0, 1]),
                    "false_negatives": int(cm[1, 0]),
                    "true_positives": int(cm[1, 1])
                },
                "total_samples": len(y),
                "fraud_rate": round(y.mean(), 4)
            },
            "predictions": {
                "predicted_labels": y_pred.tolist(),
                "prediction_probabilities": [round(prob, 4) for prob in y_pred_proba]
            }
        })
        
    except Exception as e:
        logger.error(f"Error evaluating custom data: {e}")
        return jsonify({
            "error": f"Error processing test data: {str(e)}"
        }), 500

@app.route('/performance-summary', methods=['GET'])
def performance_summary():
    """Get comprehensive model performance summary"""
    if model is None:
        return jsonify({
            "error": "Model not loaded"
        }), 500
    
    summary = get_model_performance_summary()
    
    if "error" in summary:
        return jsonify(summary), 400
    
    return jsonify({
        "status": "success",
        "performance_summary": summary
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/verify", 
            "/health", 
            "/model-info", 
            "/fraud-attempts",
            "/accuracy",
            "/accuracy/detailed", 
            "/accuracy/custom",
            "/performance-summary"
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    if model is None:
        logger.error("Cannot start server: Model not loaded")
        exit(1)
    
    logger.info("Starting fraud detection server...")
    app.run(host='0.0.0.0', port=5000, debug=False)