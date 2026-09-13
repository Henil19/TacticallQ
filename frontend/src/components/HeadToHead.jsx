import React, { useState, useEffect } from 'react';
import { Swords, Shield, Target, ArrowRight } from 'lucide-react';
import { apiClient } from '../api/client';

export default function HeadToHead({ matches }) {
  const [matchAId, setMatchAId] = useState(matches[0]?.match_id || '');
  const [matchBId, setMatchBId] = useState(matches[Math.min(1, matches.length - 1)]?.match_id || '');
  const [h2hData, setH2hData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (matches.length > 0) {
      if (!matchAId) setMatchAId(matches[0].match_id);
      if (!matchBId) setMatchBId(matches[Math.min(1, matches.length - 1)].match_id);
    }
  }, [matches]);

  useEffect(() => {
    if (matchAId && matchBId) {
      fetchH2H();
    }
  }, [matchAId, matchBId]);

  const fetchH2H = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getHeadToHead(matchAId, matchBId);
      setH2hData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Swords color="#38BDF8" size={20} /> ⚔️ Head-to-Head & Cross-Fixture Telemetry Analytics
        </h3>
        <p className="subtitle" style={{ marginBottom: '16px' }}>
          Compare key performance metrics, xG conversion efficiency, and defensive block heights side-by-side across Euro 2024 fixtures.
        </p>

        <div className="grid-2">
          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Select Primary Fixture (Match A):</label>
            <select className="select-field" value={matchAId} onChange={e => setMatchAId(Number(e.target.value))}>
              {matches.map(m => (
                <option key={m.match_id} value={m.match_id}>{m.display_label}</option>
              ))}
            </select>
          </div>

          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Select Benchmark Fixture (Match B):</label>
            <select className="select-field" value={matchBId} onChange={e => setMatchBId(Number(e.target.value))}>
              {matches.map(m => (
                <option key={m.match_id} value={m.match_id}>{m.display_label}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px', color: '#38BDF8' }}>Loading comparison telemetry...</div>
      ) : h2hData ? (
        <div className="grid-2">
          {/* Match A Card */}
          <div className="glass-card">
            <h3 style={{ fontSize: '1.1rem', color: '#38BDF8', marginBottom: '12px' }}>
              🏟️ Match A: {h2hData.match_a.info.home_team} {h2hData.match_a.info.home_score} - {h2hData.match_a.info.away_score} {h2hData.match_a.info.away_team}
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {Object.keys(h2hData.match_a.xg_summary).map(team => {
                const xgInfo = h2hData.match_a.xg_summary[team];
                const defInfo = h2hData.match_a.defensive_line[team] || {};
                const dirInfo = h2hData.match_a.pass_directness[team] || {};

                return (
                  <div key={team} style={{ background: 'rgba(8, 12, 20, 0.6)', padding: '14px', borderRadius: '10px' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase' }}>{team} Telemetry</div>
                    <div style={{ fontSize: '1.05rem', color: '#FFF', fontWeight: 800, marginTop: '4px' }}>
                      xG: {xgInfo.total_xg} | Shots: {xgInfo.total_shots} | Goals: {xgInfo.goals}
                    </div>
                    <div style={{ color: '#38BDF8', fontSize: '0.83rem', marginTop: '4px' }}>
                      Defensive Line: {defInfo.avg_line_height_yards || 'N/A'} yds ({defInfo.block_type || 'N/A'})
                    </div>
                    <div style={{ color: '#94A3B8', fontSize: '0.83rem' }}>
                      Pass Directness: {dirInfo.directness_pct || 'N/A'}% forward | Avg Length: {dirInfo.avg_pass_length_yards || 'N/A'} yds
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Match B Card */}
          <div className="glass-card card-indigo">
            <h3 style={{ fontSize: '1.1rem', color: '#818CF8', marginBottom: '12px' }}>
              🏟️ Match B: {h2hData.match_b.info.home_team} {h2hData.match_b.info.home_score} - {h2hData.match_b.info.away_score} {h2hData.match_b.info.away_team}
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {Object.keys(h2hData.match_b.xg_summary).map(team => {
                const xgInfo = h2hData.match_b.xg_summary[team];
                const defInfo = h2hData.match_b.defensive_line[team] || {};
                const dirInfo = h2hData.match_b.pass_directness[team] || {};

                return (
                  <div key={team} style={{ background: 'rgba(8, 12, 20, 0.6)', padding: '14px', borderRadius: '10px' }}>
                    <div style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700, textTransform: 'uppercase' }}>{team} Telemetry</div>
                    <div style={{ fontSize: '1.05rem', color: '#FFF', fontWeight: 800, marginTop: '4px' }}>
                      xG: {xgInfo.total_xg} | Shots: {xgInfo.total_shots} | Goals: {xgInfo.goals}
                    </div>
                    <div style={{ color: '#818CF8', fontSize: '0.83rem', marginTop: '4px' }}>
                      Defensive Line: {defInfo.avg_line_height_yards || 'N/A'} yds ({defInfo.block_type || 'N/A'})
                    </div>
                    <div style={{ color: '#94A3B8', fontSize: '0.83rem' }}>
                      Pass Directness: {dirInfo.directness_pct || 'N/A'}% forward | Avg Length: {dirInfo.avg_pass_length_yards || 'N/A'} yds
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
