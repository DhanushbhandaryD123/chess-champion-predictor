import React, { useState, useEffect, useCallback, useRef } from "react";

function PredictLiveMatchForm() {
  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [accuracy, setAccuracy] = useState(null);
  const [loading, setLoading] = useState(false);

  const player1Ref = useRef(null);

  // ✅ Auto-focus on Player 1 input
  useEffect(() => {
    player1Ref.current?.focus();
  }, []);

  // ✅ Load model accuracy once
  useEffect(() => {
    fetch("http://localhost:5000/accuracy")
      .then((res) => res.text())
      .then((data) => setAccuracy(data))
      .catch(() => setAccuracy(null));
  }, []);

  // ✅ Fetch prediction
  const fetchPrediction = useCallback(async () => {
    const p1 = player1.trim().toLowerCase();
    const p2 = player2.trim().toLowerCase();
    if (!p1 || !p2) return;

    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ player1: p1, player2: p2 }),
      });

      const data = await res.json();
      if (res.ok) {
        setResult(data);
        setError("");
      } else {
        setError(data.error || "Something went wrong");
        setResult(null);
      }
    } catch (err) {
      setError("Server error. Please try again.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }, [player1, player2]);

  // ✅ Auto-refresh every 15 seconds
  useEffect(() => {
    if (!player1 || !player2) return;
    const interval = setInterval(() => {
      fetchPrediction();
    }, 15000);
    return () => clearInterval(interval);
  }, [fetchPrediction, player1, player2]);

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchPrediction();
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: "500px", margin: "auto" }}>
      <h2 className="text-center mb-4">🔍 Predict Chess Champion</h2>

      <input
        ref={player1Ref}
        type="text"
        className="form-control mb-3"
        placeholder="Enter Player 1 Username"
        value={player1}
        onChange={(e) => setPlayer1(e.target.value)}
        required
      />

      <input
        type="text"
        className="form-control mb-3"
        placeholder="Enter Player 2 Username"
        value={player2}
        onChange={(e) => setPlayer2(e.target.value)}
        required
      />

      <button type="submit" className="btn btn-warning w-100" disabled={loading}>
        {loading ? (
          <>
            <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Predicting...
          </>
        ) : (
          "Predict"
        )}
      </button>

      {error && <p className="text-danger mt-3 text-center">{error}</p>}

      {result && (
        <div className="mt-4 p-3 bg-light rounded shadow-sm">
          <h4>🏆 Prediction Result</h4>
          <p><strong>{result.player1.username}:</strong> {result.player1.prob}% chance</p>
          <p><strong>{result.player2.username}:</strong> {result.player2.prob}% chance</p>
          <p><strong>Predicted Winner:</strong> {result.winner}</p>
          {accuracy && <p className="text-muted">🔢 Model Accuracy: {accuracy}%</p>}
        </div>
      )}
    </form>
  );
}

export default PredictLiveMatchForm;
