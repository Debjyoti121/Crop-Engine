
// Example: React Native / Flutter Integration
const cropRecommendationAPI = {
  baseURL: 'http://your-server.com:5000',
  
  // Method 1: Complete manual input
  async getRecommendationManual(soilData) {
    const response = await fetch(`${this.baseURL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        N: soilData.nitrogen,
        P: soilData.phosphorus,
        K: soilData.potassium,
        pH: soilData.pH,
        temperature: soilData.temperature,
        humidity: soilData.humidity,
        moisture: soilData.moisture,
        rainfall: soilData.rainfall
      })
    });
    return await response.json();
  },
  
  // Method 2: Partial input with defaults
  async getRecommendationPartial(availableData) {
    const response = await fetch(`${this.baseURL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(availableData) // Only provide what you have
    });
    return await response.json();
  },
  
  // Method 3: With GPS location for weather
  async getRecommendationWithWeather(soilData, location, apiKey) {
    const response = await fetch(`${this.baseURL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...soilData,
        lat: location.latitude,
        lon: location.longitude,
        weather_api_key: apiKey
      })
    });
    return await response.json();
  }
};
