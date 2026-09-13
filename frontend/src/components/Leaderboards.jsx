import React, { useState, useEffect } from 'react';
import { Trophy, Target, Share2, Shield } from 'lucide-react';
import { apiClient } from '../api/client';

export default function Leaderboards() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient.getLeaderboards()
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ textAlign: 'center', padding: '40px', color: '#38BDF8' }}>Loading tournament leaderboards...</div>;
  if (!data) return null;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Trophy color="#38BDF8" size={20} /> 🏆 UEFA Euro 2024 Tournament Leaderboards
        </h3>
        <p className="subtitle">
          Aggregated performance leaders across cached Euro 2024 match event stream datasets.
        </p>
      </div>

      <div className="grid-2">
        {/* Top xG Leaders */}
        <div className="glass-card">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Target size={16} color="#38BDF8" /> Top Expected Goals ($xG$) Leaders
          </h4>
          <div style={{ overflowY: 'auto', maxHeight: '300px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {(data.top_xg || []).map((row, idx) => (
              <div key={idx} style={{
                background: 'rgba(8, 12, 20, 0.6)',
                padding: '10px 12px',
                borderRadius: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#FFF' }}>{idx + 1}. {row.player}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>{row.team}</div>
                </div>
                <div style={{ fontWeight: 800, color: '#38BDF8' }}>{row.total_xg?.toFixed(2)} xG</div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Goal Scorers */}
        <div className="glass-card card-emerald">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            ⚽ Top Goal Scorers
          </h4>
          <div style={{ overflowY: 'auto', maxHeight: '300px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {(data.top_goals || []).map((row, idx) => (
              <div key={idx} style={{
                background: 'rgba(8, 12, 20, 0.6)',
                padding: '10px 12px',
                borderRadius: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#FFF' }}>{idx + 1}. {row.player}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>{row.team}</div>
                </div>
                <div style={{ fontWeight: 800, color: '#10B981' }}>{row.goals} Goals</div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Pass Masters */}
        <div className="glass-card card-indigo">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Share2 size={16} color="#818CF8" /> Top Pass Masters (Completed Passes)
          </h4>
          <div style={{ overflowY: 'auto', maxHeight: '300px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {(data.top_passes || []).map((row, idx) => (
              <div key={idx} style={{
                background: 'rgba(8, 12, 20, 0.6)',
                padding: '10px 12px',
                borderRadius: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#FFF' }}>{idx + 1}. {row.player}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>{row.team}</div>
                </div>
                <div style={{ fontWeight: 800, color: '#818CF8' }}>{row.passes_completed} Passes ({row.pass_completion_pct?.toFixed(1)}%)</div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Defensive Pressers */}
        <div className="glass-card card-crimson">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Shield size={16} color="#F43F5E" /> Top Defensive Pressers
          </h4>
          <div style={{ overflowY: 'auto', maxHeight: '300px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {(data.top_pressures || []).map((row, idx) => (
              <div key={idx} style={{
                background: 'rgba(8, 12, 20, 0.6)',
                padding: '10px 12px',
                borderRadius: '8px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#FFF' }}>{idx + 1}. {row.player}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>{row.team}</div>
                </div>
                <div style={{ fontWeight: 800, color: '#F43F5E' }}>{row.pressures} Pressures</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
