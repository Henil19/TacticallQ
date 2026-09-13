import React, { useState } from 'react';
import { Activity, Key, Shield, Zap, Cpu } from 'lucide-react';

export default function Header({ matchInfo, eventCount, apiKey, setApiKey }) {
  const [showKeyInput, setShowKeyInput] = useState(false);
  const homeTeam = matchInfo?.home_team || 'Home';
  const awayTeam = matchInfo?.away_team || 'Away';
  const homeScore = matchInfo?.home_score ?? 0;
  const awayScore = matchInfo?.away_score ?? 0;

  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      border: '1px solid rgba(255, 255, 255, 0.1)',
      borderTop: '3px solid #38BDF8',
      borderRadius: '18px',
      padding: '20px 26px',
      boxShadow: '0 12px 30px -6px rgba(0, 0, 0, 0.5)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '2.2rem' }}>⚽</span>
            <h1 style={{ margin: 0, color: '#F8FAFC', fontSize: '1.9rem', fontWeight: 800 }}>
              Tactical<span style={{ color: '#38BDF8' }}>IQ</span>
            </h1>
            <span style={{
              background: 'linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%)',
              color: 'white',
              padding: '3px 12px',
              borderRadius: '20px',
              fontSize: '0.75rem',
              fontWeight: 800,
              letterSpacing: '0.05em'
            }}>
              PRO REACT UI v2.5
            </span>
          </div>
          <p style={{ margin: '4px 0 0 0', color: '#94A3B8', fontSize: '0.9rem' }}>
            UEFA Euro 2024 AI Match Intelligence & Spatial Pitch Analytics Platform
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
          <div style={{
            background: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            padding: '6px 14px',
            borderRadius: '30px',
            fontSize: '0.8rem',
            fontWeight: 600,
            color: '#34D399',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <span className="live-dot"></span> FASTAPI ONLINE
          </div>

          <div style={{
            background: 'rgba(56, 189, 248, 0.12)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            padding: '6px 14px',
            borderRadius: '30px',
            fontSize: '0.8rem',
            fontWeight: 600,
            color: '#38BDF8',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <Activity size={14} /> StatsBomb Standard
          </div>

          <button
            onClick={() => setShowKeyInput(!showKeyInput)}
            className="btn-secondary"
            style={{ padding: '6px 14px', fontSize: '0.8rem' }}
          >
            <Key size={14} color="#A5B4FC" /> {apiKey ? 'Gemini Key Configured' : 'Set Gemini Key'}
          </button>
        </div>
      </div>

      {showKeyInput && (
        <div style={{ marginTop: '14px', paddingTop: '12px', borderTop: '1px solid rgba(255, 255, 255, 0.08)', display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input
            type="password"
            placeholder="Enter Google Gemini API Key..."
            className="input-field"
            value={apiKey || ''}
            onChange={(e) => setApiKey(e.target.value)}
            style={{ maxWidth: '400px' }}
          />
          <span style={{ fontSize: '0.78rem', color: '#94A3B8' }}>
            Optional: If omitted, built-in domain heuristic synthesis is used.
          </span>
        </div>
      )}

      <div style={{
        marginTop: '16px',
        paddingTop: '14px',
        borderTop: '1px solid rgba(255, 255, 255, 0.08)',
        display: 'flex',
        justifyConstraint: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '12px',
        fontSize: '0.88rem'
      }}>
        <div style={{ color: '#CBD5E1' }}>
          <span style={{ color: '#94A3B8' }}>Active Fixture Telemetry:</span>{' '}
          <strong style={{ color: '#F8FAFC', fontSize: '1.05rem', marginLeft: '6px' }}>
            {homeTeam} {homeScore} - {awayScore} {awayTeam}
          </strong>{' '}
          <span style={{ color: '#64748B', margin: '0 8px' }}>|</span>
          <span style={{ color: '#38BDF8', fontWeight: 600 }}>{matchInfo?.stage || 'Euro 2024'}</span>{' '}
          <span style={{ color: '#64748B', margin: '0 8px' }}>|</span>
          <span style={{ color: '#94A3B8' }}>{matchInfo?.match_date || '2024'}</span>
        </div>
        <div style={{ color: '#94A3B8', fontSize: '0.82rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Zap size={14} color="#38BDF8" /> <strong style={{ color: '#38BDF8' }}>{eventCount}</strong> Event Telemetry Tokens
        </div>
      </div>
    </div>
  );
}
