import requests
import pandas as pd
import pickle
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv('API_URL', 'http://localhost:8000')

def fetch_latest_data() -> Dict:
    """Fetch the latest egg production data from the API."""
    response = requests.get(f"{API_URL}/egg-production/?skip=0&limit=5")
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
        "province": data['province']['province_name'],
        'district': data['district']['district_name'],
        's11q2_2': data['month'], 
        's11q2_3': data['laying_hens'], 
        's11q2_6': data['eggs_sold'], 
        's11q2_7': data['egg_unit_price'], 
        's11q2_8': data['hatched_eggs'], 
        's11q2_9': data['eggs_for_other_usages'],
    }])
    return features

def load_model(model_path: str = '../model/egg_yield_model_gbr.pkl'):
    """Load the trained model."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    return pickle.load(open(model_path, 'rb'))

def make_prediction():
    """Fetch latest data and make a prediction."""
    try:
        # Fetch the latest data
        latest_data = fetch_latest_data()
        print("Latest data fetched successfully")
        
        # Prepare the data
        features = prepare_data_for_prediction(latest_data)
        print("Data prepared for prediction")
        
        # # Load the model
        model = load_model()
        print("Model loaded successfully")
        
        # # Make prediction
        prediction = model.predict(features)
        print(f"Prediction: {prediction[0]}")
        
        return {
            "latest_data": latest_data,
            "prediction": prediction[0],
            "features_used": features.to_dict(orient='records')[0]
        }
        
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
        return None

if __name__ == "__main__":
    result = make_prediction()
    if result:
        print("\nPrediction Results:")
        print(f"Predicted Yield Rate:", result['prediction'])
        print("\nFeatures used:")
        print(pd.DataFrame([result['features_used']]).rename(columns={
            's11q2_2': 'month', 
            's11q2_3': 'laying_hens', 
            's11q2_6': 'eggs_sold', 
            's11q2_7': 'egg_unit_price', 
            's11q2_8': 'hatched_eggs', 
            's11q2_9': 'eggs_for_other_usages',
        }).to_dict(orient='records'))
        print("\nLatest data used:")
        print(pd.DataFrame([result['latest_data']]).to_dict(orient='records'))