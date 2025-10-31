import requests
import pandas as pd
import joblib
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000')

def fetch_latest_data() -> Dict:
    """Fetch the latest egg production data from the API."""
    response = requests.get(f"{API_URL}/egg-production/")
    if response.status_code == 200:
        productions = response.json()
        if productions:
            # Get the latest entry
            latest = sorted(productions, key=lambda x: x['id'], reverse=True)[0]
            return latest
    raise Exception("Failed to fetch latest data")

def prepare_data_for_prediction(data: Dict) -> pd.DataFrame:
    """Prepare the data for prediction."""
    # Create a DataFrame with the required features
    features = pd.DataFrame([{
        'laying_hens': data['laying_hens'],
        'eggs_consumed': data['eggs_consumed'],
        'eggs_sold': data['eggs_sold'],
        'egg_unit_price': data['egg_unit_price'],
        'hatched_eggs': data['hatched_eggs'],
        'eggs_for_other_usages': data['eggs_for_other_usages']
    }])
    return features

def load_model(model_path: str = 'models/egg_yield_model.joblib'):
    """Load the trained model."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return joblib.load(model_path)

def make_prediction():
    """Fetch latest data and make a prediction."""
    try:
        # Fetch the latest data
        latest_data = fetch_latest_data()
        print("Latest data fetched successfully")
        
        # Prepare the data
        features = prepare_data_for_prediction(latest_data)
        print("Data prepared for prediction")
        
        # Load the model
        model = load_model()
        print("Model loaded successfully")
        
        # Make prediction
        prediction = model.predict(features)
        print(f"Prediction: {prediction[0]}")
        
        return {
            "household_id": latest_data["household_id"],
            "prediction": bool(prediction[0]),
            "features_used": features.to_dict(orient='records')[0]
        }
        
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
        return None

if __name__ == "__main__":
    result = make_prediction()
    if result:
        print("\nPrediction Results:")
        print(f"Household ID: {result['household_id']}")
        print(f"Predicted Yield: {'Yes' if result['prediction'] else 'No'}")
        print("\nFeatures used:")
        for feature, value in result['features_used'].items():
            print(f"{feature}: {value}")