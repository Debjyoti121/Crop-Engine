from flask import Flask, request, jsonify
import numpy as np
from data_preprocessors import skewness_handler, scaling_transformation
from predictor import crop_recommender, load_model, _load_encoder
import warnings
import traceback
warnings.filterwarnings('ignore')

app = Flask(__name__)

# Required input fields and their types
REQUIRED_FIELDS = {
    "N": (int, float),
    "P": (int, float), 
    "K": (int, float),
    "pH": (int, float),
    "temperature": (int, float),
    "humidity": (int, float),
    "moisture": (int, float),
    "rainfall": (int, float)
}

def validate_input_data(data):
    """Validate the input data format and values."""
    if not isinstance(data, dict):
        return False, "Input data must be a JSON object"
    
    # Check for missing fields
    missing_fields = [field for field in REQUIRED_FIELDS if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {missing_fields}"
    
    # Check for extra fields
    extra_fields = [field for field in data if field not in REQUIRED_FIELDS]
    if extra_fields:
        return False, f"Unknown fields found: {extra_fields}"
    
    # Validate field types and values
    for field, value in data.items():
        expected_types = REQUIRED_FIELDS[field]
        if not isinstance(value, expected_types):
            return False, f"Field '{field}' must be a number, got {type(value).__name__}"
        
        # Basic range validation
        if field == "pH" and not (0 <= value <= 14):
            return False, f"pH must be between 0 and 14, got {value}"
        elif field in ["humidity", "moisture"] and not (0 <= value <= 100):
            return False, f"{field} must be between 0 and 100, got {value}"
        elif value < 0:
            return False, f"Field '{field}' cannot be negative, got {value}"
    
    return True, None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify service status."""
    try:
        # Try to load the model and encoder to ensure they're accessible
        model = load_model()
        encoder, class_names = _load_encoder()
        
        return jsonify({
            "status": "healthy",
            "message": "Crop Recommender API is running",
            "model_loaded": model is not None,
            "encoder_loaded": encoder is not None,
            "number_of_crops": len(class_names) if class_names else 0
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "message": "Service is not ready",
            "error": str(e)
        }), 503

@app.route('/predict', methods=['POST'])
def predict_crop():
    """
    Receives a data point as JSON, processes it,
    and returns the best crop and its probability.
    
    Expected input format:
    {
        "N": 276.50,        // Nitrogen content
        "P": 35,            // Phosphorus content
        "K": 40,            // Potassium content
        "pH": 6.70,         // Soil pH (0-14)
        "temperature": 37,   // Temperature in °C
        "humidity": 67.50,   // Humidity percentage (0-100)
        "moisture": 79,      // Soil moisture (0-100)
        "rainfall": 150      // Rainfall in mm
    }
    """
    try:
        # Get JSON data from the request
        input_data = request.get_json()

        # Validate that we got data
        if not input_data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate input format and values
        is_valid, error_message = validate_input_data(input_data)
        if not is_valid:
            return jsonify({"error": error_message}), 400
        
        # 1. Apply skewness handler
        data_point_skewed = skewness_handler(input_data)
        
        # 2. Apply scaling transformation
        data_point_scaled = scaling_transformation(data_point_skewed)
        
        # 3. Get recommendation
        best_crop, probability = crop_recommender(data_point_scaled)
        
        # 4. Round the probability
        probability = np.round(probability, 4)
        
        # --- Return the result ---
        result = {
            "best_crop": best_crop,
            "probability": float(probability),
            "input_received": input_data
        }
        
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except FileNotFoundError as e:
        return jsonify({"error": f"Model files not found: {str(e)}"}), 503
    except Exception as e:
        # Log the full traceback for debugging
        print(f"Unexpected error: {traceback.format_exc()}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information."""
    return jsonify({
        "service": "Crop Recommender API",
        "version": "1.0",
        "endpoints": {
            "/health": "GET - Check service health",
            "/predict": "POST - Get crop recommendation",
            "/": "GET - This information"
        },
        "example_request": {
            "method": "POST",
            "url": "/predict",
            "body": {
                "N": 276.50,
                "P": 35,
                "K": 40,
                "pH": 6.70,
                "temperature": 37,
                "humidity": 67.50,
                "moisture": 79,
                "rainfall": 150
            }
        }
    }), 200

if __name__ == '__main__':
    # 'debug=True' reloads the server on code changes.
    # 'host=0.0.0.0' makes it accessible on your network.
    app.run(host='0.0.0.0', port=5000, debug=True)
