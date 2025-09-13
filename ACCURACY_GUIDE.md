# Fraud Detection Model Accuracy Guide

This guide explains how to check your fraud detection model's accuracy using the new evaluation features.

## 🚀 Quick Start

### 1. Start Your Flask API
```bash
python app.py
```

### 2. Generate Test Data (if needed)
```bash
python generate_fraud_dataset.py
```

### 3. Run Comprehensive Accuracy Test
```bash
python test_accuracy.py
```

## 📊 Available Accuracy Checking Methods

### Method 1: Basic Accuracy Metrics
**Endpoint:** `GET /accuracy`

Returns basic accuracy metrics:
- Accuracy
- Precision
- Recall
- F1-Score
- Test samples count
- Fraud rate

**Example:**
```bash
curl http://127.0.0.1:5000/accuracy
```

### Method 2: Detailed Accuracy Metrics
**Endpoint:** `GET /accuracy/detailed`

Returns comprehensive metrics including:
- All basic metrics
- Confusion matrix (True/False Positives/Negatives)
- Cross-validation scores (5-fold)
- Specificity and Sensitivity
- Classification report

**Example:**
```bash
curl http://127.0.0.1:5000/accuracy/detailed
```

### Method 3: Custom Data Testing
**Endpoint:** `POST /accuracy/custom`

Test your model with custom data:

**Example:**
```bash
curl -X POST http://127.0.0.1:5000/accuracy/custom \
  -H "Content-Type: application/json" \
  -d '{
    "test_data": [
      {"typing_speed": 45.0, "time_on_page": 120, "payment_type": "credit card", "is_fraud": 0},
      {"typing_speed": 150.0, "time_on_page": 15, "payment_type": "credit card", "is_fraud": 1}
    ]
  }'
```

### Method 4: Performance Summary
**Endpoint:** `GET /performance-summary`

Returns comprehensive model information and performance metrics.

**Example:**
```bash
curl http://127.0.0.1:5000/performance-summary
```

## 🧪 Testing Scripts

### 1. Comprehensive Accuracy Test (`test_accuracy.py`)
This script provides a complete accuracy evaluation:

```bash
python test_accuracy.py
```

**What it does:**
- Tests API connectivity
- Gets basic accuracy metrics
- Gets detailed accuracy metrics with confusion matrix
- Performs cross-validation analysis
- Tests with custom data
- Generates a comprehensive report
- Saves results to a JSON file

### 2. API Testing (`test_api.py`)
Tests all API endpoints including accuracy endpoints:

```bash
python test_api.py
```

## 📈 Understanding Accuracy Metrics

### Basic Metrics
- **Accuracy**: Overall correct predictions / Total predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall

### Confusion Matrix
```
                Predicted
Actual    0 (Normal)  1 (Fraud)
0 (Normal)    TN         FP
1 (Fraud)     FN         TP
```

- **True Negatives (TN)**: Correctly identified normal transactions
- **False Positives (FP)**: Normal transactions flagged as fraud
- **False Negatives (FN)**: Fraud transactions missed
- **True Positives (TP)**: Correctly identified fraud transactions

### Additional Metrics
- **Specificity**: TN / (TN + FP) - Ability to identify normal transactions
- **Sensitivity**: TP / (TP + FN) - Ability to identify fraud transactions

## 🔍 Cross-Validation

The system performs 5-fold cross-validation to provide more robust accuracy estimates:
- Mean accuracy across all folds
- Standard deviation of accuracy
- Individual fold scores

## 📄 Generated Reports

The `test_accuracy.py` script generates detailed reports saved as:
```
accuracy_report_YYYYMMDD_HHMMSS.json
```

These reports contain:
- Timestamp of testing
- API status
- All accuracy metrics
- Confusion matrix
- Cross-validation results
- Custom test results

## 🛠️ Troubleshooting

### Common Issues

1. **"Test data file not found"**
   - Run `python generate_fraud_dataset.py` to create test data

2. **"Model not loaded"**
   - Ensure your model file `fraud_detection_model.pkl` exists
   - Check the model loading section in `app.py`

3. **API connection errors**
   - Make sure Flask API is running: `python app.py`
   - Check if port 5000 is available

4. **Missing dependencies**
   - Install required packages: `pip install scikit-learn pandas numpy`

### Required Dependencies
```bash
pip install flask flask-cors joblib pandas scikit-learn mysql-connector-python requests
```

## 📊 Interpreting Results

### Good Accuracy Indicators
- **Accuracy > 0.85** (85%)
- **Precision > 0.80** (80%)
- **Recall > 0.75** (75%)
- **F1-Score > 0.80** (80%)
- **Low false positive rate** (high specificity)
- **Consistent cross-validation scores** (low standard deviation)

### Areas for Improvement
- **Low recall**: Model misses too many fraud cases
- **Low precision**: Model flags too many normal transactions as fraud
- **High false positive rate**: Too many legitimate customers blocked
- **Inconsistent CV scores**: Model may be overfitting

## 🔄 Continuous Monitoring

For production use, consider:
1. **Regular accuracy checks** (weekly/monthly)
2. **Real-time performance monitoring**
3. **A/B testing** with different model versions
4. **Feedback loop** from actual fraud detection results

## 📞 Support

If you encounter issues:
1. Check the logs in `fraud_detection.log`
2. Verify all dependencies are installed
3. Ensure test data exists and is properly formatted
4. Check database connectivity if using fraud attempts storage 