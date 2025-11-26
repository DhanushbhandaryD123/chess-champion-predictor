from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from chess_api import (
    get_chesscom_live_stats,
    are_players_in_live_game,
    get_live_game_stats,
    predict_match,
    log_prediction_to_csv,
    get_tournament_group_matches
)

app = Flask(__name__)
CORS(app)

# ✅ Load trained model
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("✅ model.pkl loaded")
except Exception as e:
    model = None
    print("❌ Failed to load model.pkl:", e)

# ✅ Load model accuracy
try:
    with open("accuracy.txt", "r") as f:
        model_accuracy = float(f.read())
    print("✅ accuracy.txt loaded")
except Exception:
    model_accuracy = None
    print("⚠️ accuracy.txt not found or unreadable")

@app.route("/")
def home():
    return "✅ Flask server is running! Use POST /predict or /predict-tournament-round"

@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    player1 = data.get("player1")
    player2 = data.get("player2")

    if not player1 or not player2:
        return jsonify({"error": "Both player1 and player2 usernames are required"}), 400

    # 🔍 Check live game
    live_game = are_players_in_live_game(player1, player2)
    if live_game:
        print("♟️ Players found in a live game")
        stats_dict = get_live_game_stats(live_game)
        stats1 = stats_dict.get(player1.lower())
        stats2 = stats_dict.get(player2.lower())
    else:
        print("🧠 Falling back to historical stats")
        stats1 = get_chesscom_live_stats(player1)
        stats2 = get_chesscom_live_stats(player2)

    print(f"📥 {player1} stats: {stats1}")
    print(f"📥 {player2} stats: {stats2}")

    if not stats1 or not stats2:
        return jsonify({"error": "One or both players not found or inactive"}), 404

    try:
        features1 = np.array([[stats1["rating"], stats1["wins"], stats1["losses"], stats1["draws"], stats1["win_rate"]]])
        features2 = np.array([[stats2["rating"], stats2["wins"], stats2["losses"], stats2["draws"], stats2["win_rate"]]])

        prob1 = model.predict_proba(features1)[0][1]
        prob2 = model.predict_proba(features2)[0][1]
        winner = player1 if prob1 > prob2 else player2

        result = {
            "timestamp": "manual_test",
            "player1": player1,
            "player2": player2,
            "player1_prob": round(prob1 * 100, 2),
            "player2_prob": round(prob2 * 100, 2),
            "winner": winner,
            "source": "manual"
        }

        log_prediction_to_csv(result)

        return jsonify({
            "player1": {"username": player1, "prob": result["player1_prob"]},
            "player2": {"username": player2, "prob": result["player2_prob"]},
            "winner": result["winner"],
            "model_accuracy": model_accuracy if model_accuracy is not None else "Unknown"
        })

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

@app.route("/predict-tournament-round", methods=["POST"])
def predict_tournament_round():
    if not model:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    tournament_id = data.get("tournament_id")
    round_num = data.get("round")
    group_num = data.get("group")

    if not tournament_id or not round_num or not group_num:
        return jsonify({"error": "tournament_id, round, and group are required"}), 400

    try:
        matches = get_tournament_group_matches(tournament_id, round_num, group_num)
        results = []

        for match in matches:
            p1 = match["white"]
            p2 = match["black"]
            result = predict_match(model, p1, p2, source="tournament")
            if result:
                results.append(result)
                log_prediction_to_csv(result)

        return jsonify({
            "tournament": tournament_id,
            "round": round_num,
            "group": group_num,
            "total_matches": len(results),
            "predictions": results
        })

    except Exception as e:
        return jsonify({"error": f"Tournament prediction failed: {str(e)}"}), 500

@app.route("/accuracy", methods=["GET"])
def get_accuracy():
    return str(model_accuracy) if model_accuracy is not None else "Unknown"

# ✅ Optional Console Runner
def run_manual_test():
    print("\n🔧 Manual Prediction Test")
    p1 = input("Enter Player 1 Username: ").strip().lower()
    p2 = input("Enter Player 2 Username: ").strip().lower()

    result = predict_match(model, p1, p2)
    if result:
        print(f"\n🏁 Prediction between {p1} vs {p2}")
        print(f"{p1}: {result['player1_prob']}%")
        print(f"{p2}: {result['player2_prob']}%")
        print(f"Predicted Winner: {result['winner']}")
        log_prediction_to_csv(result)
    else:
        print("❌ Failed to fetch stats or predict")

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        run_manual_test()
    else:
        app.run(port=5000)
