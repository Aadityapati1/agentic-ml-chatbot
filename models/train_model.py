from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib


# 1. Load dataset
data = fetch_california_housing()

X = data.data
y = data.target


# 2. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 3. Train Linear Regression
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

linear_mae = mean_absolute_error(y_test, linear_predictions)
linear_rmse = np.sqrt(mean_squared_error(y_test, linear_predictions))
linear_r2 = r2_score(y_test, linear_predictions)


# 4. Train Random Forest
random_forest_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

random_forest_model.fit(X_train, y_train)

random_forest_predictions = random_forest_model.predict(X_test)

random_forest_mae = mean_absolute_error(
    y_test,
    random_forest_predictions
)

random_forest_rmse = np.sqrt(
    mean_squared_error(y_test, random_forest_predictions)
)

random_forest_r2 = r2_score(
    y_test,
    random_forest_predictions
)


# 5. Print results
print("MODEL COMPARISON")
print("================")

print("\nLinear Regression:")
print("MAE:", linear_mae)
print("RMSE:", linear_rmse)
print("R2 Score:", linear_r2)

print("\nRandom Forest:")
print("MAE:", random_forest_mae)
print("RMSE:", random_forest_rmse)
print("R2 Score:", random_forest_r2)


# 6. Save Random Forest model
joblib.dump(
    random_forest_model,
    "models/house_price_model.pkl"
)

print("\nRandom Forest model saved successfully!")