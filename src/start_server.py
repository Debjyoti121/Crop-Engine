#!/usr/bin/env python
import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Change to the directory containing this script
os.chdir(current_dir)

try:
    from flask import Flask, request, jsonify
    import numpy as np
    from data_preprocessors import skewness_handler, scaling_transformation
    from predictor import crop_recommender, load_model, _load_encoder
    import warnings
    import traceback
    warnings.filterwarnings('ignore')

    print("All imports successful!")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in directory: {os.listdir('.')}")
    
    # Test if we can load the model files
    try:
        model = load_model()
        encoder, class_names = _load_encoder()
        print(f"Model and encoder loaded successfully! Number of crops: {len(class_names)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        
    # Import and run the app
    from app import app
    print("Starting Flask application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()