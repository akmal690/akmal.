# AI Verification Accuracy Reduction Guide

This guide explains how to reduce the accuracy of the AI fraud detection system from 98.7% to a configurable lower level.

## 🎯 Overview

The original fraud detection model had an accuracy of **98.7%**. With the new accuracy reduction system, you can:

- **Reduce accuracy** to any target between 70% and 95%
- **Add random noise** to predictions (0-30%)
- **Introduce bias** towards false positives/negatives (0-20%)
- **Control all settings** through a web interface or API

## 🚀 Quick Start

### 1. Start the Flask API
```bash
python app.py
```

### 2. Open the Checkout Page
Navigate to `checkout.php` in your browser. You'll see a new "AI Verification Accuracy Control" section.

### 3. Adjust Accuracy Settings
- **Target Accuracy**: Set your desired accuracy (default: 85%)
- **Noise Factor**: Add randomness to predictions (default: 15%)
- **Bias Factor**: Introduce systematic errors (default: 10%)
- **Enable/Disable**: Toggle accuracy reduction on/off

### 4. Click "Update Accuracy Settings"
This will apply your changes to the Flask API.

## 📊 Accuracy Reduction Methods

### Method 1: Random Noise
- Adds random variation to prediction probabilities
- Makes the model less consistent
- Range: 0-30%

### Method 2: Feature-Based Bias
- **High typing speed** (>100 WPM): Bias towards false positives
- **Low time on page** (<30 seconds): Bias towards false negatives  
- **Credit card payments**: Bias towards false positives
- Range: 0-20%

### Method 3: Random Prediction Flipping
- Randomly flips some predictions from correct to incorrect
- Automatically calculated based on target accuracy
- Example: To reach 85% accuracy, ~15% of predictions are flipped

## 🔧 API Endpoints

### Get Current Settings
```bash
GET http://localhost:5000/accuracy-control
```

### Update Settings
```bash
POST http://localhost:5000/accuracy-control
Content-Type: application/json

{
    "enabled": true,
    "target_accuracy": 0.75,
    "noise_factor": 0.20,
    "bias_factor": 0.15
}
```

### Test Verification
```bash
POST http://localhost:5000/verify
Content-Type: application/json

{
    "typing_speed": 45.0,
    "time_on_page": 120,
    "payment_type": "credit card",
    "user_id": "user123"
}
```

## 🧪 Testing

### Run the Test Script
```bash
python test_accuracy_reduction.py
```

This will:
1. Check current settings
2. Update to 75% accuracy
3. Test verification with reduced accuracy
4. Verify bias effects

### Manual Testing
1. Set target accuracy to 80%
2. Make multiple verification requests with the same data
3. Observe variation in results (indicating reduced accuracy)

## 📈 Example Scenarios

### Scenario 1: Moderate Accuracy Reduction
- **Target**: 90% accuracy
- **Noise**: 10%
- **Bias**: 5%
- **Result**: ~10% accuracy reduction with moderate randomness

### Scenario 2: Aggressive Accuracy Reduction
- **Target**: 75% accuracy  
- **Noise**: 25%
- **Bias**: 20%
- **Result**: ~24% accuracy reduction with high randomness

### Scenario 3: Disable Accuracy Reduction
- **Target**: 98.7% (original)
- **Noise**: 0%
- **Bias**: 0%
- **Result**: Original model performance

## 🎛️ Configuration Variables

In `app.py`, you can modify these global variables:

```python
ACCURACY_REDUCTION_ENABLED = True      # Master switch
ACCURACY_TARGET = 0.85                # Target accuracy (0.70-0.95)
RANDOM_NOISE_FACTOR = 0.15            # Random noise (0.0-0.30)
BIAS_FACTOR = 0.10                    # Systematic bias (0.0-0.20)
```

## 🔍 Monitoring

### Logs
The system logs all accuracy reduction activities:
```
INFO: Accuracy reduction applied: Original pred=0, proba=0.1234 -> New pred=1, proba=0.8765
```

### Metrics
Check the `/accuracy` endpoint to see how the reduced accuracy affects model performance.

## ⚠️ Important Notes

1. **Production Use**: Accuracy reduction is intended for testing and development
2. **Security**: Lower accuracy may increase fraud risk
3. **Performance**: Random operations add minimal overhead
4. **Persistence**: Settings are stored in memory and reset on API restart

## 🛠️ Troubleshooting

### API Not Responding
- Ensure Flask API is running on port 5000
- Check firewall settings
- Verify CORS is enabled

### No Accuracy Reduction
- Check if `ACCURACY_REDUCTION_ENABLED = True`
- Verify target accuracy is below 98.7%
- Check browser console for JavaScript errors

### Inconsistent Results
- This is expected behavior with reduced accuracy
- Higher noise/bias factors increase inconsistency
- Use the test script to verify functionality

## 📚 Files Modified

- `app.py` - Added accuracy reduction logic and API endpoint
- `checkout.php` - Added web interface for controlling accuracy
- `test_accuracy_reduction.py` - Test script for verification
- `ACCURACY_REDUCTION_README.md` - This documentation

## 🎉 Success!

You've successfully reduced the AI verification accuracy from 98.7% to a configurable lower level. The system now provides:

- **Flexible accuracy control** (70%-95%)
- **Multiple reduction methods** (noise, bias, flipping)
- **Real-time configuration** through web interface
- **Comprehensive testing** and monitoring tools

Use this system responsibly and remember that lower accuracy may impact fraud detection effectiveness. 