import React from 'react';
import { Search, Filter, Trophy, Sparkles } from 'lucide-react';

export default function Sidebar({
  matches,
  stages,
  selectedMatchId,
  setSelectedMatchId,
  searchQuery,
  setSearchQuery,
  selectedStage,
  setSelectedStage
}) {
  return (
    <aside style={{
      width: '300px',
      background: 'linear-gradient(180deg, rgba(15, 23, 42, 0.96) 0%, rgba(8, 12, 20, 0.98) 100%)',
      backdropFilter: 'blur(24px)',
      borderRight: '1px solid rgba(255, 255, 255, 0.08)',
      padding: '24px 18px',
      display: 'flex',
      flexDirection: 'column',
      gap: '20px',
      flexShrink: 0
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <Trophy color="#38BDF8" size={24} />
        <h2 style={{ margin: 0, color: '#F8FAFC', fontSize: '1.3rem', fontWeight: 800 }}>
          Euro 2024
        </h2>
      </div>

      <div>
        <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Search size={14} /> Search Team / Stage
        </label>
        <input
          type="text"
          placeholder="e.g. Spain, Germany, Final..."
          className="input-field"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      <div>
        <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Filter size={14} /> Filter Stage
        </label>
        <select
          className="select-field"
          value={selectedStage}
          onChange={(e) => setSelectedStage(e.target.value)}
        >
          {stages.map((stg) => (
            <option key={stg} value={stg}>{stg}</option>
          ))}
        </select>
      </div>

      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '8px' }}>
          Select Fixture ({matches.length})
        </label>
        <div style={{
          overflowY: 'auto',
          maxHeight: '400px',
          display: 'flex',
          flexDirection: 'column',
          gap: '6px',
          paddingRight: '4px'
        }}>
          {matches.map((m) => {
            const isSelected = m.match_id === selectedMatchId;
            return (
              <button
                key={m.match_id}
                onClick={() => setSelectedMatchId(m.match_id)}
                style={{
                  textAlign: 'left',
                  padding: '10px 12px',
                  borderRadius: '10px',
                  border: isSelected ? '1px solid #38BDF8' : '1px solid rgba(255,255,255,0.06)',
                  background: isSelected ? 'rgba(56, 189, 248, 0.15)' : 'rgba(30, 41, 59, 0.4)',
                  color: isSelected ? '#FFFFFF' : '#CBD5E1',
                  cursor: 'pointer',
                  fontSize: '0.83rem',
                  fontWeight: isSelected ? 700 : 500,
                  transition: 'all 0.2s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '3px' }}>
                  <span style={{ fontSize: '0.72rem', color: isSelected ? '#38BDF8' : '#94A3B8' }}>{m.stage}</span>
                  <span style={{ fontSize: '0.72rem', color: '#64748B' }}>{m.match_date}</span>
                </div>
                <div style={{ fontSize: '0.88rem', fontWeight: 700 }}>
                  {m.home_team} {m.home_score} - {m.away_score} {m.away_team}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div style={{
        padding: '14px',
        background: 'rgba(30, 41, 59, 0.5)',
        borderRadius: '12px',
        border: '1px solid rgba(255, 255, 255, 0.06)',
        fontSize: '0.78rem',
        color: '#94A3B8',
        display: 'flex',
        gap: '8px'
      }}>
        <Sparkles color="#38BDF8" size={20} style={{ flexShrink: 0 }} />
        <div>
          <strong style={{ color: '#38BDF8' }}>TacticalIQ Scout Tip:</strong> Select fixtures to switch telemetry datasets instantly. Gemini AI automatically synthesizes match dossiers.
        </div>
      </div>
    </aside>
  );
}
