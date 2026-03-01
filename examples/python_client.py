
# Example: Python script for automated data collection
import requests
import time
import json
from datetime import datetime

class CropRecommenderClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def get_recommendation(self, data):
        """Get crop recommendation from API"""
        try:
            response = requests.post(f"{self.base_url}/predict", json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def collect_and_recommend(self):
        """Collect data and get recommendation"""
        # Example: Read from sensors, files, or user input
        data = {
            "N": self.read_nitrogen_sensor(),
            "P": self.read_phosphorus_sensor(),
            "K": self.read_potassium_sensor(),
            "pH": self.read_ph_sensor(),
            "temperature": self.read_temperature(),
            "humidity": self.read_humidity(),
            "moisture": self.read_soil_moisture(),
            "rainfall": self.read_rainfall()
        }
        
        result = self.get_recommendation(data)
        
        # Log result
        timestamp = datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "input_data": data,
            "recommendation": result
        }
        
        with open("crop_recommendations.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        return result
    
    def read_nitrogen_sensor(self):
        # Replace with actual sensor reading
        return 275.0
    
    # ... other sensor reading methods

# Usage
client = CropRecommenderClient()
recommendation = client.collect_and_recommend()
print(f"Recommended crop: {recommendation.get('best_crop', 'Unknown')}")
