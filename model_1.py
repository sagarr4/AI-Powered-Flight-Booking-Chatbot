import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load your dataset
data = pd.read_csv("flight_results.csv")  # Replace with the path to your dataset

# Assuming your dataset has columns: 'departure_city', 'destination_city', 'flight_type', 'departure_date', 'return_date', 'price'
# Preprocess the data
data['Departure Time'] = pd.to_datetime(data['Departure Time']).astype(int) / 10**9
data['Arrival Time'] = pd.to_datetime(data['Arrival Time']).astype(int) / 10**9

# Encoding categorical features
label_encoder = LabelEncoder()
data['departureCity'] = label_encoder.fit_transform(data['departureCity'])
data['destinationCity'] = label_encoder.fit_transform(data['destinationCity'])
data['flightType'] = label_encoder.fit_transform(data['flightType'])

# Split the data
X = data[['departureCity', 'destinationCity', 'flightType', 'Departure Time', 'Arrival Time']]
y = data['Price (USD)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the model and label encoder
joblib.dump(model, "flight_price_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("Model and label encoder saved!")
