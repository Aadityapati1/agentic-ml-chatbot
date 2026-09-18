import joblib


# Load the trained model
model = joblib.load("models/house_price_model.pkl")

FEATURE_NAMES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
]

def predict_house_price(features):
    if not isinstance(features, list):
        raise ValueError("Features must be provided as a list.")

    if len(features) != 8:
        raise ValueError("House price prediction requires exactly 8 features.")

    if not all(isinstance(value, (int, float)) for value in features):
        raise ValueError("All features must be numbers.")

    prediction = model.predict([features])

    return prediction[0]