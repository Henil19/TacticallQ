import React, { useState } from 'react';
import { Globe, Search, Bot, Gamepad2, Sparkles, CheckCircle2 } from 'lucide-react';
import { apiClient } from '../api/client';

// Helper component to format raw markdown into clean point-wise glassmorphic cards
function PointWiseCardList({ text, accentColor = '#38BDF8' }) {
  if (!text) return null;

  const lines = text.split('\n');
  const sections = [];
  let currentSection = { title: '', points: [] };

  lines.forEach((rawLine) => {
    const line = rawLine.trim();
    if (!line) return;

    // Check for Section Headers (###, ####, 1., 2., etc.)
    if (line.startsWith('#') || line.match(/^[0-9]+\.\s+[A-Z]/i)) {
      if (currentSection.title || currentSection.points.length > 0) {
        sections.push({ ...currentSection });
      }
      const cleanedTitle = line
        .replace(/^[#\s0-9.\-*]+/, '')
        .replace(/\*\*/g, '')
        .replace(/^[📋🛡️⚡🎯🚀🔥💡]\s*/, '')
        .trim();
      currentSection = { title: cleanedTitle, points: [] };
    } else if (line.startsWith('-') || line.startsWith('•') || line.startsWith('*')) {
      const cleanPoint = line.replace(/^[-•*]\s*/, '').trim();
      if (cleanPoint) {
        currentSection.points.push(cleanPoint);
      }
    } else if (line.includes(':') && !line.startsWith('Based on')) {
      currentSection.points.push(line);
    } else {
      if (line.length > 5 && !line.startsWith('Analyst Query Response')) {
        currentSection.points.push(line);
      }
    }
  });

  if (currentSection.title || currentSection.points.length > 0) {
    sections.push({ ...currentSection });
  }

  const renderPointText = (point) => {
    const parts = point.split('**');
    if (parts.length >= 3) {
      return (
        <span>
          <strong style={{ color: accentColor, fontWeight: 700 }}>{parts[1]}</strong>
          {parts.slice(2).join('')}
        </span>
      );
    }
    return point.replace(/\*\*/g, '');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '12px' }}>
      {sections.map((sec, secIdx) => (
        <div
          key={secIdx}
          style={{
            background: 'rgba(11, 15, 25, 0.85)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderLeft: `4px solid ${accentColor}`,
            borderRadius: '10px',
            padding: '16px 20px',
            boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)'
          }}
        >
          {sec.title && (
            <div
              style={{
                fontWeight: 800,
                fontSize: '0.95rem',
                color: '#F8FAFC',
                marginBottom: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <span
                style={{
                  background: `${accentColor}22`,
                  color: accentColor,
                  padding: '3px 9px',
                  borderRadius: '6px',
                  fontSize: '0.72rem',
                  fontWeight: 800,
                  letterSpacing: '0.5px'
                }}
              >
                POINT {secIdx + 1}
              </span>
              {sec.title}
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {sec.points.map((pt, ptIdx) => (
              <div
                key={ptIdx}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  fontSize: '0.88rem',
                  lineHeight: 1.5,
                  color: '#CBD5E1'
                }}
              >
                <CheckCircle2 size={15} color={accentColor} style={{ marginTop: '3px', flexShrink: 0 }} />
                <div>{renderPointText(pt)}</div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default function AIScout({ matchInfo, apiKey }) {
  const homeTeam = matchInfo?.home_team || 'Spain';
  const awayTeam = matchInfo?.away_team || 'England';

  // State for Q&A
  const [query, setQuery] = useState(`How did ${homeTeam} control possession against ${awayTeam}?`);
  const [scoutAnswer, setScoutAnswer] = useState(null);
  const [loadingScout, setLoadingScout] = useState(false);

  // State for Counter Strategy Simulator
  const [oppTeam, setOppTeam] = useState(awayTeam);
  const [oppFormation, setOppFormation] = useState('4-3-3');
  const [oppPlaystyle, setOppPlaystyle] = useState('High Pressing & Vertical Transition');
  const [oppStar, setOppStar] = useState('Jude Bellingham');
  const [blueprint, setBlueprint] = useState('');
  const [loadingSim, setLoadingSim] = useState(false);

  const handleSearchAndAnalyze = async () => {
    if (!query) return;
    setLoadingScout(true);
    try {
      const res = await apiClient.runAIScoutQuery(matchInfo.match_id || 3930159, query, apiKey);
      setScoutAnswer(res.answer);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingScout(false);
    }
  };

  const handleRunSimulation = async () => {
    setLoadingSim(true);
    try {
      const res = await apiClient.simulateCounterStrategy(oppTeam, oppFormation, oppPlaystyle, oppStar, apiKey);
      setBlueprint(res.blueprint);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingSim(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Scout Q&A Card */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Globe color="#38BDF8" size={20} /> AI Scout Assistant
        </h3>
        <p className="subtitle" style={{ marginBottom: '16px' }}>
          Query StatsBomb match telemetry to analyze team tactics, player roles, and execution patterns.
        </p>

        <div style={{ display: 'flex', gap: '10px', marginBottom: '16px' }}>
          <input
            type="text"
            className="input-field"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter Tactical Scouting Question..."
          />
          <button onClick={handleSearchAndAnalyze} className="btn-primary" disabled={loadingScout}>
            <Search size={15} /> {loadingScout ? 'Analyzing...' : 'Search & Analyze'}
          </button>
        </div>

        {scoutAnswer && (
          <div style={{ marginTop: '16px' }}>
            <h4
              style={{
                color: '#38BDF8',
                fontSize: '0.95rem',
                marginBottom: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: 700
              }}
            >
              <Bot color="#38BDF8" size={18} /> AI Scout Tactical Analysis Points
            </h4>
            <PointWiseCardList text={scoutAnswer} accentColor="#38BDF8" />
          </div>
        )}
      </div>

      {/* Interactive AI Tactical Counter-Strategy Simulator Card */}
      <div className="glass-card card-indigo">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Gamepad2 color="#818CF8" size={20} /> Interactive AI Tactical Counter-Strategy Simulator
        </h3>
        <p className="subtitle" style={{ marginBottom: '16px' }}>
          Input custom opponent tactical setups to generate an instant point-wise counter-strategy blueprint and pressing plan.
        </p>

        <div className="grid-2" style={{ marginBottom: '16px' }}>
          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Opponent Team Name:</label>
            <input type="text" className="input-field" value={oppTeam} onChange={(e) => setOppTeam(e.target.value)} />
          </div>

          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Opponent Formation:</label>
            <select className="select-field" value={oppFormation} onChange={(e) => setOppFormation(e.target.value)}>
              <option value="4-3-3">4-3-3 Attacking</option>
              <option value="4-2-3-1">4-2-3-1 Double Pivot</option>
              <option value="5-3-2 / 3-5-2">5-3-2 / 3-5-2 Wingbacks</option>
              <option value="4-4-2 Mid-Block">4-4-2 Mid-Block</option>
              <option value="3-4-2-1 High Press">3-4-2-1 High Press</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Opponent Playstyle:</label>
            <select className="select-field" value={oppPlaystyle} onChange={(e) => setOppPlaystyle(e.target.value)}>
              <option value="High Pressing & Vertical Transition">High Pressing & Vertical Transition</option>
              <option value="Low Block Counter-Attack">Low Block Counter-Attack</option>
              <option value="Possession Heavy & Overlapping Wings">Possession Heavy & Overlapping Wings</option>
              <option value="Direct Long-Ball Target Man">Direct Long-Ball Target Man</option>
            </select>
          </div>

          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>
              Key Opponent Player to Neutralize:
            </label>
            <input type="text" className="input-field" value={oppStar} onChange={(e) => setOppStar(e.target.value)} />
          </div>
        </div>

        <button
          onClick={handleRunSimulation}
          className="btn-primary"
          style={{ width: '100%', marginBottom: '16px' }}
          disabled={loadingSim}
        >
          <Sparkles size={16} />{' '}
          {loadingSim ? 'Simulating Counter Blueprint...' : 'Run AI Tactical Counter-Strategy Simulation'}
        </button>

        {blueprint && (
          <div style={{ marginTop: '16px' }}>
            <h4
              style={{
                color: '#818CF8',
                fontSize: '0.95rem',
                marginBottom: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: 700
              }}
            >
              <Sparkles color="#818CF8" size={18} /> Tactical Counter-Strategy Blueprint Points
            </h4>
            <PointWiseCardList text={blueprint} accentColor="#818CF8" />
          </div>
        )}
      </div>
    </div>
  );
}
