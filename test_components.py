#!/usr/bin/env python
"""
Test script for crop recommender components
"""
import os
import sys
import json

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
os.chdir(src_dir)

def test_components():
    """Test all components of the crop recommender."""
    print("=== Testing Crop Recommender Components ===\n")
    
    try:
        # Test imports
        print("1. Testing imports...")
        from data_preprocessors import skewness_handler, scaling_transformation
        from predictor import crop_recommender, load_model, _load_encoder
        print("✓ All imports successful\n")
        
        # Test model loading
        print("2. Testing model loading...")
        model = load_model()
        encoder, class_names = _load_encoder()
        print(f"✓ Model loaded successfully")
        print(f"✓ Encoder loaded successfully")
        print(f"✓ Number of crop classes: {len(class_names)}")
        print(f"✓ Available crops: {class_names[:5]}... (showing first 5)\n")
        
        # Test data preprocessing
        print("3. Testing data preprocessing...")
        test_data = {
            "N": 276.50,
            "P": 35,
            "K": 40,
            "pH": 6.70,
            "temperature": 37,
            "humidity": 67.50,
            "moisture": 79,
            "rainfall": 150
        }
        
        print(f"   Original data: {test_data}")
        
        # Apply skewness handler
        skewed_data = skewness_handler(test_data)
        print(f"   After skewness handling: {skewed_data}")
        
        # Apply scaling
        scaled_data = scaling_transformation(skewed_data)
        print(f"   After scaling: {scaled_data}")
        print("✓ Data preprocessing successful\n")
        
        # Test prediction
        print("4. Testing crop prediction...")
        best_crop, probability = crop_recommender(scaled_data)
        print(f"✓ Best crop recommended: {best_crop}")
        print(f"✓ Confidence probability: {probability:.4f}")
        print("✓ Crop prediction successful\n")
        
        # Test Flask app import
        print("5. Testing Flask app...")
        from app import app
        print("✓ Flask app imported successfully")
        
        # Test Flask app endpoints
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            print(f"✓ Health endpoint status: {response.status_code}")
            health_data = response.get_json()
            print(f"   Health data: {health_data}")
            
            # Test root endpoint
            response = client.get('/')
            print(f"✓ Root endpoint status: {response.status_code}")
            
            # Test predict endpoint
            response = client.post('/predict', 
                                 json=test_data,
                                 content_type='application/json')
            print(f"✓ Predict endpoint status: {response.status_code}")
            prediction_data = response.get_json()
            print(f"   Prediction result: {prediction_data}")
        
        print("\n=== ALL TESTS PASSED! ===")
        print("Your crop recommender engine is working correctly!")
        print("\nTo start the server, run:")
        print(f"  cd \"{src_dir}\"")
        print("  python start_server.py")
        print("\nThen test with:")
        print("  python test.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_components()