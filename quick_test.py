import requests
import json

def test_api():
    data = {
        'N': 276.50,
        'P': 35,
        'K': 40,
        'pH': 6.70,
        'temperature': 37,
        'humidity': 67.50,
        'moisture': 79,
        'rainfall': 150
    }

    print('🌱 Testing Crop Prediction API')
    print('=' * 40)
    print('📤 POST http://127.0.0.1:5000/predict')
    print('📋 Input Data:')
    print(json.dumps(data, indent=2))
    print()

    try:
        response = requests.post('http://127.0.0.1:5000/predict', json=data, timeout=10)
        print(f'📊 Status Code: {response.status_code}')
        
        if response.status_code == 200:
            result = response.json()
            print()
            print('✅ SUCCESS! Crop Recommendation Result:')
            print(f'🌾 Recommended Crop: {result.get("best_crop")}')
            print(f'📈 Confidence Level: {result.get("probability", 0)*100:.1f}%')
            print()
            print('📝 Complete Response:')
            print(json.dumps(result, indent=2))
        else:
            print('❌ Error Response:')
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print('❌ ERROR: Cannot connect to server on port 5000')
        print('   Make sure Flask server is running!')
    except Exception as e:
        print(f'❌ Unexpected Error: {e}')

    print()
    print('🔚 Test completed!')

if __name__ == "__main__":
    test_api()