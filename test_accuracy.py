#!/usr/bin/env python3
"""
Comprehensive Accuracy Testing Script for Fraud Detection Model
This script provides multiple ways to evaluate your model's accuracy
"""

import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
import time

# API base URL
BASE_URL = "http://127.0.0.1:5000"

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print("❌ API is not healthy")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def get_basic_accuracy():
    """Get basic accuracy metrics"""
    print("\n" + "="*60)
    print("📊 BASIC ACCURACY METRICS")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/accuracy")
        if response.status_code == 200:
            data = response.json()
            metrics = data['accuracy_metrics']
            
            print(f"Accuracy:           {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"Precision:          {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
            print(f"Recall:             {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
            print(f"F1-Score:           {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
            print(f"Test Samples:       {metrics['test_samples']}")
            print(f"Fraud Rate:         {metrics['fraud_rate']:.4f} ({metrics['fraud_rate']*100:.2f}%)")
            
            return metrics
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error getting accuracy: {e}")
        return None

def get_detailed_accuracy():
    """Get detailed accuracy metrics including confusion matrix"""
    print("\n" + "="*60)
    print("🔍 DETAILED ACCURACY METRICS")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/accuracy/detailed")
        if response.status_code == 200:
            data = response.json()
            metrics = data['detailed_metrics']
            
            # Basic metrics
            print(f"Accuracy:           {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"Precision:          {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
            print(f"Recall:             {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
            print(f"F1-Score:           {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
            
            # Confusion Matrix
            cm = metrics['confusion_matrix']
            print(f"\n📋 CONFUSION MATRIX:")
            print(f"True Negatives:     {cm['true_negatives']}")
            print(f"False Positives:    {cm['false_positives']}")
            print(f"False Negatives:    {cm['false_negatives']}")
            print(f"True Positives:     {cm['true_positives']}")
            
            # Calculate additional metrics
            total = cm['true_negatives'] + cm['false_positives'] + cm['false_negatives'] + cm['true_positives']
            specificity = cm['true_negatives'] / (cm['true_negatives'] + cm['false_positives']) if (cm['true_negatives'] + cm['false_positives']) > 0 else 0
            sensitivity = cm['true_positives'] / (cm['true_positives'] + cm['false_negatives']) if (cm['true_positives'] + cm['false_negatives']) > 0 else 0
            
            print(f"\n📈 ADDITIONAL METRICS:")
            print(f"Specificity:        {specificity:.4f} ({specificity*100:.2f}%)")
            print(f"Sensitivity:        {sensitivity:.4f} ({sensitivity*100:.2f}%)")
            print(f"Total Predictions:  {total}")
            
            # Cross-validation results
            cv = metrics['cross_validation']
            print(f"\n🔄 CROSS-VALIDATION (5-fold):")
            print(f"Mean Accuracy:      {cv['mean_accuracy']:.4f} ({cv['mean_accuracy']*100:.2f}%)")
            print(f"Std Accuracy:       {cv['std_accuracy']:.4f} ({cv['std_accuracy']*100:.2f}%)")
            print(f"CV Scores:          {cv['cv_scores']}")
            
            return metrics
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error getting detailed accuracy: {e}")
        return None

def get_performance_summary():
    """Get comprehensive performance summary"""
    print("\n" + "="*60)
    print("📋 PERFORMANCE SUMMARY")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/performance-summary")
        if response.status_code == 200:
            data = response.json()
            summary = data['performance_summary']
            
            print(f"Model Type:         {summary['model_info']['model_type']}")
            print(f"Features:           {', '.join(summary['model_info']['feature_names'])}")
            print(f"Payment Types:      {', '.join(summary['model_info']['payment_types'])}")
            
            if 'accuracy_evaluation' in summary and 'error' not in summary['accuracy_evaluation']:
                acc = summary['accuracy_evaluation']
                print(f"\n📊 ACCURACY EVALUATION:")
                print(f"Overall Accuracy:   {acc['accuracy']:.4f} ({acc['accuracy']*100:.2f}%)")
                print(f"Precision:          {acc['precision']:.4f} ({acc['precision']*100:.2f}%)")
                print(f"Recall:             {acc['recall']:.4f} ({acc['recall']*100:.2f}%)")
                print(f"F1-Score:           {acc['f1_score']:.4f} ({acc['f1_score']*100:.2f}%)")
            
            return summary
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error getting performance summary: {e}")
        return None

def test_custom_data():
    """Test model with custom data"""
    print("\n" + "="*60)
    print("🧪 CUSTOM DATA TESTING")
    print("="*60)
    
    # Generate some test cases
    test_cases = [
        # Normal behavior
        {"typing_speed": 45, "time_on_page": 13, "payment_type": "credit card", "is_fraud": 0},
        {"typing_speed": 48, "time_on_page": 15, "payment_type": "paypal", "is_fraud": 0},
        {"typing_speed": 30, "time_on_page": 18, "payment_type": "cash on delivery", "is_fraud": 0},
        
        # Suspicious behavior
        {"typing_speed": 76, "time_on_page": 109, "payment_type": "credit card", "is_fraud": 0},
        {"typing_speed": 89, "time_on_page": 150, "payment_type": "paypal", "is_fraud": 0},
        {"typing_speed": 98, "time_on_page": 189, "payment_type": "credit card", "is_fraud": 0},
    ]
    
    try:
        response = requests.post(f"{BASE_URL}/accuracy/custom", json={"test_data": test_cases})
        if response.status_code == 200:
            data = response.json()
            metrics = data['metrics']
            predictions = data['predictions']
            
            print(f"Custom Test Results:")
            print(f"Accuracy:           {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
            print(f"Precision:          {metrics['precision']:.4f} ({metrics['precision']*100:.2f}%)")
            print(f"Recall:             {metrics['recall']:.4f} ({metrics['recall']*100:.2f}%)")
            print(f"F1-Score:           {metrics['f1_score']:.4f} ({metrics['f1_score']*100:.2f}%)")
            
            print(f"\n📋 PREDICTION DETAILS:")
            for i, (case, pred, prob) in enumerate(zip(test_cases, predictions['predicted_labels'], predictions['prediction_probabilities'])):
                status = "✅" if pred == case['is_fraud'] else "❌"
                print(f"Case {i+1}: {status} Predicted: {pred}, Actual: {case['is_fraud']}, Confidence: {prob:.4f}")
                print(f"  Speed: {case['typing_speed']}, Time: {case['time_on_page']}, Payment: {case['payment_type']}")
            
            return data
        else:
            print(f"❌ Error: {response.json()}")
            return None
    except Exception as e:
        print(f"❌ Error testing custom data: {e}")
        return None

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("📄 GENERATING COMPREHENSIVE TEST REPORT")
    print("="*60)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "api_status": "unknown",
        "basic_accuracy": None,
        "detailed_accuracy": None,
        "performance_summary": None,
        "custom_test": None
    }
    
    # Test API connection
    if test_api_connection():
        report["api_status"] = "healthy"
        
        # Get all metrics
        report["basic_accuracy"] = get_basic_accuracy()
        report["detailed_accuracy"] = get_detailed_accuracy()
        report["performance_summary"] = get_performance_summary()
        report["custom_test"] = test_custom_data()
        
        # Save report
        filename = f"accuracy_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Test report saved to: {filename}")
        
        # Print summary
        print(f"\n📊 SUMMARY:")
        if report["basic_accuracy"]:
            acc = report["basic_accuracy"]["accuracy"]
            print(f"Overall Accuracy: {acc:.4f} ({acc*100:.2f}%)")
        
        if report["detailed_accuracy"]:
            cm = report["detailed_accuracy"]["confusion_matrix"]
            total_correct = cm["true_positives"] + cm["true_negatives"]
            total = cm["true_positives"] + cm["true_negatives"] + cm["false_positives"] + cm["false_negatives"]
            print(f"Correct Predictions: {total_correct}/{total} ({total_correct/total*100:.2f}%)")
        
    else:
        report["api_status"] = "unhealthy"
        print("❌ Cannot generate report - API is not available")
    
    return report

def main():
    """Main function to run all accuracy tests"""
    print("🔍 FRAUD DETECTION MODEL ACCURACY TESTING")
    print("="*60)
    print(f"Testing started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if API is running
    if not test_api_connection():
        print("\n❌ Please start your Flask API first:")
        print("   python app.py")
        return
    
    # Run all tests
    report = generate_test_report()
    
    print(f"\n✅ Testing completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 