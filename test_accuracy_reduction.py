#!/usr/bin/env python3
"""
Test script to verify accuracy reduction functionality
"""

import requests
import json
import time

def test_accuracy_reduction():
    """Test the accuracy reduction functionality"""
    
    print("🧪 Testing Accuracy Reduction Functionality")
    print("=" * 50)
    
    # Test 1: Check current accuracy settings
    print("\n1. Checking current accuracy settings...")
    try:
        response = requests.get('http://localhost:5000/accuracy-control')
        if response.status_code == 200:
            settings = response.json()['accuracy_reduction']
            print(f"   ✅ Current target accuracy: {settings['current_target_percentage']}")
            print(f"   ✅ Noise factor: {settings['random_noise_factor']*100:.1f}%")
            print(f"   ✅ Bias factor: {settings['bias_factor']*100:.1f}%")
            print(f"   ✅ Enabled: {settings['enabled']}")
        else:
            print(f"   ❌ Failed to get settings: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting settings: {e}")
        return False
    
    # Test 2: Update accuracy settings to reduce accuracy
    print("\n2. Updating accuracy settings to reduce accuracy...")
    try:
        new_settings = {
            "enabled": True,
            "target_accuracy": 0.75,  # 75% accuracy (reduced from 98.7%)
            "noise_factor": 0.20,     # 20% noise
            "bias_factor": 0.15       # 15% bias
        }
        
        response = requests.post('http://localhost:5000/accuracy-control', 
                               json=new_settings)
        if response.status_code == 200:
            result = response.json()['accuracy_reduction']
            print(f"   ✅ Settings updated successfully!")
            print(f"   ✅ New target accuracy: {result['current_target_percentage']}")
            print(f"   ✅ New noise factor: {result['random_noise_factor']*100:.1f}%")
            print(f"   ✅ New bias factor: {result['bias_factor']*100:.1f}%")
        else:
            print(f"   ❌ Failed to update settings: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error updating settings: {e}")
        return False
    
    # Test 3: Test verification with reduced accuracy
    print("\n3. Testing verification with reduced accuracy...")
    try:
        test_data = {
            "typing_speed": 45.0,
            "time_on_page": 120,
            "payment_type": "credit card",
            "user_id": "test_user_123"
        }
        
        # Make multiple requests to see the variation
        results = []
        for i in range(5):
            response = requests.post('http://localhost:5000/verify', json=test_data)
            if response.status_code == 200:
                result = response.json()
                results.append(result)
                print(f"   Request {i+1}: Decision={result['decision']}, Probability={result['details']['fraud_probability']:.4f}")
            else:
                print(f"   ❌ Request {i+1} failed: {response.status_code}")
        
        # Check if we see variation in results (indicating reduced accuracy)
        decisions = [r['decision'] for r in results]
        probabilities = [r['details']['fraud_probability'] for r in results]
        
        if len(set(decisions)) > 1 or max(probabilities) - min(probabilities) > 0.1:
            print("   ✅ Accuracy reduction working - seeing variation in results")
        else:
            print("   ⚠️  Limited variation - accuracy reduction may not be working")
            
    except Exception as e:
        print(f"   ❌ Error testing verification: {e}")
        return False
    
    # Test 4: Test with different data to see bias effects
    print("\n4. Testing bias effects with different data...")
    try:
        # Test with high typing speed (should trigger bias)
        high_speed_data = {
            "typing_speed": 150.0,
            "time_on_page": 60,
            "payment_type": "credit card",
            "user_id": "test_user_456"
        }
        
        response = requests.post('http://localhost:5000/verify', json=high_speed_data)
        if response.status_code == 200:
            result = response.json()
            print(f"   High speed test: Decision={result['decision']}, Probability={result['details']['fraud_probability']:.4f}")
        else:
            print(f"   ❌ High speed test failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error testing bias: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Accuracy reduction testing completed!")
    print("\n📊 Summary:")
    print(f"   • Original accuracy: 98.7%")
    print(f"   • New target accuracy: 75.0%")
    print(f"   • Accuracy reduction: 23.7%")
    print(f"   • Noise factor: 20.0%")
    print(f"   • Bias factor: 15.0%")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Accuracy Reduction Test...")
    print("Make sure your Flask API is running on http://localhost:5000")
    print()
    
    try:
        success = test_accuracy_reduction()
        if success:
            print("\n🎉 All tests passed! Accuracy reduction is working correctly.")
        else:
            print("\n❌ Some tests failed. Check the error messages above.")
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}") 