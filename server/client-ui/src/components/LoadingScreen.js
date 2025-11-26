import React, { useEffect } from "react";
import kingIcon from "../assets/king.png"; // Ensure this image exists in /assets
import "./LoadingScreen.css"; // Contains spinning/animation styles

function LoadingScreen({ onLoaded }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      if (onLoaded) onLoaded(); // Safety check
    }, 3000);
    return () => clearTimeout(timer);
  }, [onLoaded]);

  return (
    <div className="loading-screen d-flex flex-column justify-content-center align-items-center bg-dark vh-100">
      <img
        src={kingIcon}
        alt="Chess King Icon Loading"
        className="rotate-king mb-3"
        width={100}
        height={100}
      />
      <h2 className="text-light">Loading Chess Predictor...</h2>
    </div>
  );
}

export default LoadingScreen;
