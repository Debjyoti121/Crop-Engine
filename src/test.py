import json
import requests
import numpy as np
import warnings
warnings.filterwarnings('ignore')

data_to_send = {
    "N" : 276.50,
    "P" : 35,
    "K" : 40,
    "pH" : 6.70,
    "temperature" : 37,
    "humidity" : 67.50,
    "moisture" : 79,
    "rainfall" : 150
}

url = "http://localhost:5000/predict"

print(f"Sending data to {url}...")
print("Data:", json.dumps(data_to_send, indent=2))

try:
    # 'json=data_to_send' automatically sets the Content-Type header to application/json
    response = requests.post(url, json=data_to_send)
    
    # --- 3. Print the Response ---
    
    print("\n--- Server Response ---")
    print(f"Status Code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Prediction (JSON):")
        # .json() parses the JSON response into a Python dictionary
        print(json.dumps(response.json(), indent=2))
    else:
        # Print the error from the server (if any)
        print("Error:")
        print(response.text)

except requests.ConnectionError:
    print("\n--- ERROR ---")
    print("Connection failed. Is the Flask server (app.py) running?")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")
