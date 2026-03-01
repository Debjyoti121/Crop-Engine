import requests
import json

def test_deployed_api():
    # 🔥 REPLACE THIS WITH YOUR ACTUAL RENDER URL
    BASE_URL = "https://crop-recommender-api-XXXX.onrender.com"  # UPDATE THIS!
    
    print("🌐 Testing Deployed Crop Recommender API")
    print("=" * 50)
    print(f"Base URL: {BASE_URL}")
    print()
    
    # Test 1: Health Check
    print("1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print("   ✅ Health check passed!")
            print(f"   Model loaded: {health_data.get('model_loaded')}")
            print(f"   Crops available: {health_data.get('number_of_crops')}")
        else:
            print("   ❌ Health check failed!")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test 2: Crop Prediction
    print("2️⃣ Testing Crop Prediction...")
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
    
    print("   Sending data:", json.dumps(test_data, indent=4))
    print()
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict", 
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print()
            print("   ✅ Prediction successful!")
            print(f"   🌾 Recommended Crop: {result.get('best_crop')}")
            print(f"   📊 Confidence: {result.get('probability', 0)*100:.1f}%")
            print()
            print("   Full Response:")
            print(json.dumps(result, indent=4))
        else:
            print("   ❌ Prediction failed!")
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    print("🔚 Testing completed!")
    print()
    print("📝 Next Steps:")
    print("1. If tests pass, your API is ready!")
    print("2. Copy your Render URL")
    print("3. Use the URL in your mobile app")
    print("4. Replace the BASE_URL in your app code")

if __name__ == "__main__":
    test_deployed_api()