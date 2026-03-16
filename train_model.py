import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

df = pd.read_csv("mobile_prices_transformed.csv")

# Create label
median_price = df['price'].median()
df['label'] = (df['price'] > median_price).astype(int)

# Features and target
X = df[['back_camera', 'battery', 'display', 'ram', 'brand_encoded', 'tier_encoded']]
y = df['label']

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

# Results
y_pred = model.predict(X_test)
print("✅ Model trained and saved as model.pkl")
print(classification_report(y_test, y_pred, target_names=["decrease", "increase"]))