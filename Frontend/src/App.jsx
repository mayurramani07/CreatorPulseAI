import "./App.css";

function App() {
  return (
    <div className="app">
      <main className="hero">
        <div className="badge">
          AI-Powered Audience Intelligence
        </div>

        <h1>
          CreatorPulse
          <span>AI</span>
        </h1>

        <p className="hero-description">
          Turn YouTube comments into actionable
          content opportunities.
        </p>

        <div className="analyzer-card">
          <input
            type="text"
            placeholder="Paste your YouTube video URL..."
          />

          <button>
            Analyze Audience
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;