from sklearn.datasets import fetch_california_housing

data = fetch_california_housing()

print("Feature names:")
print(data.feature_names)

print("\nDataset shape:")
print(data.data.shape)

print("\nTarget shape:")
print(data.target.shape)

print("\nFirst 5 rows:")
print(data.data[:5])

print("\nFirst 5 target values:")
print(data.target[:5])