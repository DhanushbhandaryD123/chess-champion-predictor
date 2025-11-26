# evaluate_model_accuracy.py
import requests
import time
import pickle
import numpy as np
from chess_api import get_chesscom_live_stats as get_chesscom_stats

print("✅ Script is running!")

# Load model
try:
    model = pickle.load(open("model.pkl", "rb"))
    print("✅ model.pkl loaded")
except Exception as e:
    print("❌ Failed to load model:", e)
    exit()

# Get archived months for a player
def get_archives(username):
    url = f"https://api.chess.com/pub/player/{username}/games/archives"
    res = requests.get(url)
    if res.status_code != 200:
        print(f"❌ Failed to fetch archives for {username} — status code {res.status_code}")
        return []
    return res.json().get("archives", [])

# Fetch games from a monthly archive
def fetch_games_from_archive(url):
    time.sleep(1)
    res = requests.get(url)
    if res.status_code != 200:
        return []
    return res.json().get("games", [])

# Main function to evaluate accuracy
def evaluate_accuracy(username):
    archives = get_archives(username)
    correct, total = 0, 0

    for archive_url in archives[-3:]:  # Only last 3 months
        games = fetch_games_from_archive(archive_url)

        for game in games:
            try:
                white = game.get("white", "").split("/")[-1]
                black = game.get("black", "").split("/")[-1]

                if white != username and black != username:
                    continue  # Skip if user was not in this game

                result_data = game.get("white_result" if white == username else "black_result")
                result = game.get("results", {}).get("white" if white == username else "black", "")

                if result not in ["win", "loss"]:
                    continue  # Skip draws

                stats1 = get_chesscom_stats(white)
                stats2 = get_chesscom_stats(black)
                if not stats1 or not stats2:
                    continue

                x1 = np.array([[stats1["rating"], stats1["wins"], stats1["losses"], stats1["draws"], stats1["win_rate"]]])
                x2 = np.array([[stats2["rating"], stats2["wins"], stats2["losses"], stats2["draws"], stats2["win_rate"]]])

                prob1 = model.predict_proba(x1)[0][1]
                prob2 = model.predict_proba(x2)[0][1]

                predicted = white if prob1 > prob2 else black
                actual = white if result == "win" else black

                if predicted == actual:
                    correct += 1
                total += 1

                time.sleep(0.5)  # prevent throttling

            except Exception:
                continue

    if total == 0:
        print("⚠️ No valid matches found.")
    else:
        accuracy = (correct / total) * 100
        print(f"\n🎯 Evaluated on {total} games for '{username}'")
        print(f"✅ Prediction Accuracy: {accuracy:.2f}%")

        with open("accuracy.txt", "w") as f:
            f.write(f"{accuracy:.2f}")

# Run test on your username
evaluate_accuracy("dhanushbhnadary")
