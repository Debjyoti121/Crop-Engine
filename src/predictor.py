import joblib
import pickle
import os

# Global variables to cache loaded models
_loaded_model = None
_loaded_encoder = None
_class_names = None

def _get_script_dir():
    """Get the directory where this script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def _load_encoder():
    """Load the label encoder once and cache it."""
    global _loaded_encoder, _class_names
    if _loaded_encoder is None:
        try:
            script_dir = _get_script_dir()
            filename = os.path.join(script_dir, "crop_label_encoder.pkl")
            with open(filename, 'rb') as file:
                _loaded_encoder = pickle.load(file)
            _class_names = list(_loaded_encoder.inverse_transform(list(range(22))))
            print("Label encoder loaded successfully.")
        except FileNotFoundError:
            raise FileNotFoundError("crop_label_encoder.pkl not found")
        except Exception as e:
            raise Exception(f"Error loading label encoder: {e}")
    return _loaded_encoder, _class_names

def load_model():
    """Load the ML model once and cache it."""
    global _loaded_model
    if _loaded_model is None:
        try:
            script_dir = _get_script_dir()
            model_filename = os.path.join(script_dir, "lgbm_best_model_22class.joblib")
            print(f"Loading model from {model_filename}...")
            _loaded_model = joblib.load(model_filename)
            print("Model loaded successfully.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Model file 'lgbm_best_model_22class.joblib' not found")
        except Exception as e:
            raise Exception(f"Error loading model: {e}")
    return _loaded_model

def crop_recommender(data_point):
    """Get crop recommendation from the input data point."""
    try:
        # Load encoder and get class names
        _, class_names = _load_encoder()
        
        # Define the expected property order for the model
        prop_order = ["N", "temperature", "humidity", "moisture", "P", "K", "rainfall", "pH"]
        
        # Validate that all required properties are present
        missing_props = [prop for prop in prop_order if prop not in data_point]
        if missing_props:
            raise ValueError(f"Missing required properties: {missing_props}")
        
        # Prepare input array in the correct order
        X = [data_point[prop] for prop in prop_order]
        
        # Load model and make prediction
        model = load_model()
        probabilities = model.predict_proba([X])[0]
        
        # Create probability dictionary and find best crop
        prob_dict = dict(zip(class_names, probabilities))
        sorted_probs = sorted(prob_dict.items(), key=lambda item: item[1], reverse=True)
        best_crop, probability = sorted_probs[0]
        
        return best_crop, probability
        
    except Exception as e:
        raise Exception(f"Error in crop recommendation: {e}")