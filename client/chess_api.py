import requests
import csv
from datetime import datetime
import numpy as np

def get_chesscom_live_stats(username):
    profile_res = requests.get(f"https://api.chess.com/pub/player/{username}")
    if profile_res.status_code != 200:
        return None

    stats_res = requests.get(f"https://api.chess.com/pub/player/{username}/stats")
    if stats_res.status_code != 200:
        return None

    stats_data = stats_res.json()

    for mode in ['chess_bullet', 'chess_blitz', 'chess_rapid']:
        if mode in stats_data and 'last' in stats_data[mode]:
            mode_data = stats_data[mode]
            rating = mode_data['last']['rating']
            record = mode_data.get('record', {})
            wins = record.get('win', 0)
            losses = record.get('loss', 0)
            draws = record.get('draw', 0)
            total = wins + losses + draws
            win_rate = round((wins / total) * 100, 2) if total > 0 else 0.0

            return {
                "rating": rating,
                "wins": wins,
                "losses": losses,
                "draws": draws,
                "win_rate": win_rate
            }

    return {
        "rating": 1200,
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "win_rate": 0.0
    }

def are_players_in_live_game(player1, player2):
    url1 = f"https://api.chess.com/pub/player/{player1}/games"
    url2 = f"https://api.chess.com/pub/player/{player2}/games"

    try:
        games1 = requests.get(url1).json().get("games", [])
        games2 = requests.get(url2).json().get("games", [])
    except:
        return None

    live_games = {game['url']: game for game in games1 if game.get('url') in [g.get('url') for g in games2]}
    return list(live_games.values())[0] if live_games else None

def get_live_game_stats(game):
    white = game["white"].split("/")[-1].lower()
    black = game["black"].split("/")[-1].lower()

    stats = {}
    for username in [white, black]:
        user_stats = get_chesscom_live_stats(username)
        if user_stats:
            stats[username] = user_stats

    return stats

# 🔁 Tournament support functions

def get_tournament_players(tournament_id):
    url = f"https://api.chess.com/pub/tournament/{tournament_id}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    return [p["username"] for p in data.get("players", [])]

def get_tournament_round_games(tournament_id, round_number):
    url = f"https://api.chess.com/pub/tournament/{tournament_id}/{round_number}"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    round_data = res.json()
    all_games = []
    for group_url in round_data.get("groups", []):
        g = requests.get(group_url)
        if g.status_code == 200:
            all_games.extend(g.json().get("games", []))
    return all_games

def predict_match(model, player1, player2):
    stats1 = get_chesscom_live_stats(player1)
    stats2 = get_chesscom_live_stats(player2)

    if not stats1 or not stats2:
        return None

    features1 = np.array([[stats1["rating"], stats1["wins"], stats1["losses"], stats1["draws"], stats1["win_rate"]]])
    features2 = np.array([[stats2["rating"], stats2["wins"], stats2["losses"], stats2["draws"], stats2["win_rate"]]])

    prob1 = model.predict_proba(features1)[0][1]
    prob2 = model.predict_proba(features2)[0][1]

    winner = player1 if prob1 > prob2 else player2

    return {
        "timestamp": datetime.now().isoformat(),
        "player1": player1,
        "player2": player2,
        "player1_prob": round(prob1 * 100, 2),
        "player2_prob": round(prob2 * 100, 2),
        "winner": winner,
        "source": "tournament"
    }

def log_prediction_to_csv(result, filename="predictions_log.csv"):
    fieldnames = ["timestamp", "player1", "player2", "player1_prob", "player2_prob", "winner", "source"]
    try:
        with open(filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            f.seek(0, 2)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(result)
    except Exception as e:
        print(f"❌ Failed to write log: {e}")

# ✅ New: get_tournament_group_matches
def get_tournament_group_matches(tournament_id, round_number, group_number):
    url = f"https://api.chess.com/pub/tournament/{tournament_id}/{round_number}/{group_number}"
    res = requests.get(url)
    if res.status_code != 200:
        raise Exception(f"Failed to fetch tournament group: {res.status_code}")
    
    data = res.json()
    matches = []

    for game in data.get("games", []):
        white = game.get("white", "").split("/")[-1]
        black = game.get("black", "").split("/")[-1]

        if white and black:
            matches.append({
                "white": white,
                "black": black
            })

    return matches
