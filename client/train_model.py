# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

print("✅ Training started...")

# ✅ Load data from CSV
csv_path = os.path.join("dataset", "sample_chess_players.csv")
try:
    data = pd.read_csv(csv_path)
    print(f"📊 Loaded {len(data)} rows from {csv_path}")
except Exception as e:
    print("❌ Failed to load CSV:", e)
    exit()

# ✅ Ensure required columns exist
required_cols = ["rating", "wins", "losses", "draws", "win_rate", "champion"]
if not all(col in data.columns for col in required_cols):
    print(f"❌ CSV missing required columns: {required_cols}")
    exit()

# ✅ Split into features and labels
X = data.drop("champion", axis=1)
y = data["champion"]

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# ✅ Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

# ✅ Save model and accuracy
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("accuracy.txt", "w") as f:
    f.write(f"{accuracy * 100:.2f}")

print("✅ model.pkl and accuracy.txt saved successfully")
