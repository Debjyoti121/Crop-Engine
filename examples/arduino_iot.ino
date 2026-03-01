
// Example: Arduino Code for IoT Integration
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Sensor pins
#define DHT_PIN 2
#define MOISTURE_PIN A0
#define PH_PIN A1
#define NPK_PIN A2

DHT dht(DHT_PIN, DHT22);
const char* serverURL = "http://your-server.com:5000/predict";

void setup() {
  Serial.begin(115200);
  dht.begin();
  // WiFi setup code here
}

void loop() {
  // Read sensors
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int moisture = analogRead(MOISTURE_PIN);
  float pH = readPHSensor();
  int npk_n = readNPKSensor('N');
  int npk_p = readNPKSensor('P');
  int npk_k = readNPKSensor('K');
  int rainfall = getRainfall(); // From rain gauge
  
  // Create JSON payload
  DynamicJsonDocument doc(1024);
  doc["N"] = npk_n;
  doc["P"] = npk_p;
  doc["K"] = npk_k;
  doc["pH"] = pH;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["moisture"] = map(moisture, 0, 1023, 0, 100);
  doc["rainfall"] = rainfall;
  
  // Send to API
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  if (httpResponseCode == 200) {
    String response = http.getString();
    Serial.println("Crop recommendation: " + response);
  }
  
  http.end();
  delay(300000); // Wait 5 minutes
}
