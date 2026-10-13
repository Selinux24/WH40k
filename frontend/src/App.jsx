// src/App.jsx
import React, { useState } from 'react';
import './App.css';

function App() {
  const [armyList1, setArmyList1] = useState('');
  const [armyList2, setArmyList2] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!armyList1 || !armyList2) {
      setError("Please provide both army lists.");
      return;
    }

    setLoading(true);
    setError(null);
    setReport(null);

    try {
      const response = await fetch('http://localhost:5000/api/calculate-combat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ army1: armyList1, army2: armyList2 }),
      });

      const data = await response.json();
      if (response.ok && data.status === "success") {
        setReport(data.report);
      } else {
        setError(data.error || "Failed to generate report.");
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError("Could not connect to the backend API. Ensure Flask is running on port 5000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1 style={{textAlign: 'center'}}>⚔️ Combat Damage Calculator</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'flex', gap: '20px' }}>
          <div style={{ flex: 1 }}>
            <h2>Army List A</h2>
            <textarea
              rows="15"
              placeholder="Paste or upload the first army list here (e.g., UnitName - PowerLevel)"
              value={armyList1}
              onChange={(e) => setArmyList1(e.target.value)}
              required
              style={{ width: '100%', fontFamily: 'monospace' }}
            />
          </div>
          <div style={{ flex: 1 }}>
            <h2>Army List B</h2>
            <textarea
              rows="15"
              placeholder="Paste or upload the second army list here (e.g., UnitName - PowerLevel)"
              value={armyList2}
              onChange={(e) => setArmyList2(e.target.value)}
              required
              style={{ width: '100%', fontFamily: 'monospace' }}
            />
          </div>
        </div>
        <button 
          onClick={handleSubmit} 
          disabled={loading}
          style={{ padding: '10px 20px', marginTop: '20px', cursor: loading ? 'not-allowed' : 'pointer', display: 'block', width: 'fit-content', margin: '20px auto' }}
        >
          {loading ? 'Calculating...' : 'Calculate Combat Report'}
        </button>
      </form>

      {error && <div style={{ color: 'red', margin: '20px', border: '1px solid red', padding: '10px' }}>Error: {error}</div>}

      {report && (
        <div className="report-container" style={{ marginTop: '40px', borderTop: '2px dashed #ccc', paddingTop: '20px' }}>
          <h2 style={{textAlign: 'center'}}>🛡️ Combat Report</h2>
          
          <section>
            <h3 style={{marginTop: '20px'}}>Summary</h3>
            <p><strong style={{display: 'block'}}>Overall Assessment:</strong > {report.combat_summary}</p>
            <div style={{ display: 'flex', gap: '30px' }}>
              <div style={{ padding: '15px', border: '2px solid green', flex: 1, borderRadius: '8px', boxShadow: '0 0 10px rgba(76, 175, 80, 0.2)'}}>
                <h4 style={{color: '#388e3c'}}>Win Chance A: {report.probability_breakdown.win_chance_army1}</h4>
                <p>Damage Estimate: {report.damage_estimates.army1_total_damage}</p>
              </div>
               <div style={{ padding: '15px', border: '2px solid orange', flex: 1, borderRadius: '8px', boxShadow: '0 0 10px rgba(255, 165, 0, 0.2)'}}>
                <h4 style={{color: '#ff9800'}}>Win Chance B: {report.probability_breakdown.win_chance_army2}</h4>
                <p>Damage Estimate: {report.damage_estimates.army2_total_damage}</p>
              </div>
            </div>
          </section>

          <section style={{ marginTop: '30px' }}>
            <h3 style={{marginTop: '20px'}}>Detailed Analysis</h3>
            {/* Simplified rendering of the complex report object */}
            <pre style={{ backgroundColor: '#f4f4f9', padding: '15px', borderRadius: '5px', overflowX: 'auto' }}>{JSON.stringify(report, null, 2)}</pre>
          </section>
        </div>
      )}
    </div>
  );
}

export default App;