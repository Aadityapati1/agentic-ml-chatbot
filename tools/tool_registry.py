from tools.calculator import calculate
from models.house_price_model import predict_house_price


TOOLS = {
    "calculator": {
        "description": "Use this tool for mathematical calculations.",
        "function": calculate
    },

    "house_price_predictor": {
        "description": """
Use this tool to predict a house price.

It requires exactly 8 numerical features in this order:

1. MedInc - median income
2. HouseAge - median house age
3. AveRooms - average rooms per household
4. AveBedrms - average bedrooms per household
5. Population - block population
6. AveOccup - average household occupancy
7. Latitude - geographic latitude
8. Longitude - geographic longitude
""",
        "function": predict_house_price
    }
}