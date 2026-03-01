import numpy as np
import pickle
import os
from sklearn.preprocessing import StandardScaler

def skewness_handler(data_point):
    """Apply skewness transformations to the input data."""
    data_point_copy = data_point.copy()  # Don't modify original data
    data_point_copy["P"] = np.log1p(data_point_copy["P"])
    data_point_copy["K"] = np.log1p(data_point_copy["K"])
    data_point_copy["rainfall"] = np.log1p(data_point_copy["rainfall"])
    data_point_copy["pH"] = (data_point_copy["pH"]**5.87-1)/5.87
    return data_point_copy


def scaling_transformation(data_point):
    """Apply scaling transformations to the input data."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(script_dir, "column_scalers.pkl")
        
        with open(filename, 'rb') as file:
            col_scalers = pickle.load(file)
        
        data_point_copy = data_point.copy()  # Don't modify original data
        for property in data_point_copy:
            if property in col_scalers:
                scaler = col_scalers[property]
                data_point_copy[property] = scaler.transform([[data_point_copy[property]]])[0][0]
            else:
                raise ValueError(f"No scaler found for property: {property}")
        return data_point_copy
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not find column_scalers.pkl file: {e}")
    except Exception as e:
        raise Exception(f"Error in scaling transformation: {e}")
    
    
