import React from "react";
import { Link } from "react-router-dom";
import PredictLiveMatchForm from "../components/PredictLiveMatchForm";
import chessBg from "../assets/chess-bg.jpg";
import "./Home.css";

function Home() {
  const scrollToPredict = () => {
    const predictSection = document.getElementById("predict");
    if (predictSection) {
      predictSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="home-container">
      {/* Navbar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow">
        <div className="container-fluid">
          <Link className="navbar-brand fw-bold" to="/">
            ♟️ Chess Predictor
          </Link>
          <button className="btn btn-warning" onClick={scrollToPredict}>
            Predict Now
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        className="hero-section position-relative text-center text-white"
        style={{
          paddingTop: "90px", // avoid overlap
          height: "100vh",
          overflow: "hidden",
        }}
      >
        <img
          src={chessBg}
          alt="Chess"
          className="w-100 h-100 object-fit-cover"
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            zIndex: 1,
            filter: "brightness(0.4)",
          }}
        />
        <div
          className="position-relative d-flex flex-column justify-content-center align-items-center h-100"
          style={{ zIndex: 2 }}
        >
          <h1 className="display-3 fw-bold text-uppercase mb-3 text-shadow">
            Predict Chess Champions Live
          </h1>
          <p className="lead fs-4 text-shadow-light">
            Real-time AI predictions based on player stats and gameplay history.
          </p>
          <button
            className="btn btn-warning mt-4 fw-semibold px-4 py-2"
            onClick={scrollToPredict}
          >
            🔮 Start Predicting
          </button>
        </div>
      </section>

      {/* Featured 15s Video Section */}
      <section className="container text-center py-5">
        <h3 className="fw-bold mb-4">👑 Witness Lightning-Fast Chess Brilliance!</h3>
        <div className="ratio ratio-16x9 shadow rounded" style={{ maxWidth: "700px", margin: "0 auto" }}>
          <iframe
            src="https://www.youtube.com/embed/Ua6kfbiNQCo?autoplay=1&mute=1&rel=0&controls=1&modestbranding=1"
            title="15s Chess Clip"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          ></iframe>
        </div>
      </section>

      {/* Highlights Section */}
      <section className="container py-5">
        <div className="text-center mb-4">
          <h2 className="fw-bold display-6 text-gradient">♟️ Epic Chess Moments</h2>
          <p className="lead text-muted">
            Relive thrilling moves and legendary checkmates
          </p>
        </div>

        <div className="row g-4">
          {[
            {
              title: "Chess Highlight 1",
              src: "https://www.youtube.com/embed/FcLYgXCkucc?rel=0&modestbranding=1&mute=1",
            },
            {
              title: "Chess Highlight 2",
              src: "https://www.youtube.com/embed/O8cb34ADUCE?rel=0&modestbranding=1&mute=1",
            },
            {
              title: "Chess Highlight 3",
              src: "https://www.youtube.com/embed/RbCKgjYh8So?rel=0&modestbranding=1&mute=1",
            },
          ].map((video, index) => (
            <div className="col-md-4" key={index}>
              <div className="ratio ratio-16x9 shadow rounded">
                <iframe
                  src={video.src}
                  title={video.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                  allowFullScreen
                ></iframe>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Prediction Form */}
      <section id="predict" className="bg-secondary text-white py-5">
        <div className="container">
          <h3 className="text-center fw-bold mb-4">🔮 Start Predicting</h3>
          <PredictLiveMatchForm />
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark text-white text-center py-3 mt-4">
        © 2025 Chess Predictor · Made with ❤️
      </footer>
    </div>
  );
}

export default Home;
