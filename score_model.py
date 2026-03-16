import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

df = pd.read_csv("mobile_prices_transformed.csv")

# Generate score from specs (0-100).
df['score'] = (
    (df['ram']          / df['ram'].max()          * 30) +
    (df['back_camera']  / df['back_camera'].max()  * 25) +
    (df['battery']      / df['battery'].max()      * 20) +
    (df['display']      / df['display'].max()      * 10) +
    (df['tier_encoded'] / df['tier_encoded'].max() * 15)
).round(2)

print("Score preview: 🎖️")
print(df[['ram', 'back_camera', 'battery', 'display', 'tier_encoded', 'score']].head(10))

# Features and target.
X = df[['back_camera', 'battery', 'display', 'ram', 'brand_encoded', 'tier_encoded']]
y = df['score']

# Train.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save.
with open("score_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Results.
y_pred = model.predict(X_test)
print(f"\n Score model trained and saved as score_model.pkl 🎯")
print(f"R2 Score 🏆:  {r2_score(y_test, y_pred):.2f}  (1.0 = perfect)")
print(f"Avg Error 🛤️: {mean_absolute_error(y_test, y_pred):.2f} points out of 100")