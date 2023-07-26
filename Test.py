import pandas as pd
import joblib
from FlightData import FlightData
from catboost import CatBoost

# Load the model from the joblib file
model = joblib.load('Modell/catboost_model.joblib')

# Now you can use the 'model' object to make predictions, etc.
flight_data = FlightData(21, 1, 'DL', 'THL', 'ATL', '1500-1559', 223.0)
new_data = pd.DataFrame(flight_data.get_data())