import React, { useState } from 'react';
import { Cpu, Users, Award, Search, Sparkles } from 'lucide-react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, Cell } from 'recharts';

export default function MLClustering({ playerStatsData }) {
  const clusters = playerStatsData?.clusters || [];
  const [player1, setPlayer1] = useState('');
  const [player2, setPlayer2] = useState('');
  const [targetPlayer, setTargetPlayer] = useState('');

  if (clusters.length === 0) return null;

  const playerNames = clusters.map(c => c.player).sort();
  const p1 = player1 || playerNames[0] || '';
  const p2 = player2 || playerNames[Math.min(1, playerNames.length - 1)] || '';
  const target = targetPlayer || playerNames[0] || '';

  const p1Data = clusters.find(c => c.player === p1);
  const p2Data = clusters.find(c => c.player === p2);

  // Radar metrics extraction (normalized 0 to 100)
  const extractRadarMetrics = (p) => {
    if (!p) return [];
    return [
      { subject: 'xG Creation', val: Math.min(100, (p.total_xg || 0) * 120) },
      { subject: 'Pass Volume', val: Math.min(100, (p.passes_completed || 0) * 2.2) },
      { subject: 'Pass Acc %', val: p.pass_completion_pct || 75 },
      { subject: 'Pressures', val: Math.min(100, (p.pressures || 0) * 10) },
      { subject: 'Def Blocks', val: Math.min(100, (p.blocks || 0) * 25) },
      { subject: 'Pitch Depth', val: Math.min(100, ((p.avg_x || 60) / 120.0) * 100) }
    ];
  };

  const p1Metrics = extractRadarMetrics(p1Data);
  const p2Metrics = extractRadarMetrics(p2Data);

  const radarChartData = p1Metrics.map((m, idx) => ({
    subject: m.subject,
    [p1]: m.val,
    [p2]: p2Metrics[idx]?.val || 0
  }));

  // Player Similarity Engine
  const targetData = clusters.find(c => c.player === target);
  let similarPlayers = [];
  if (targetData) {
    similarPlayers = clusters
      .filter(c => c.player !== target)
      .map(c => {
        const dxG = (c.total_xg || 0) - (targetData.total_xg || 0);
        const dPass = (c.passes_completed || 0) - (targetData.passes_completed || 0);
        const dPress = (c.pressures || 0) - (targetData.pressures || 0);
        const dist = Math.sqrt(dxG * dxG + dPass * dPass + dPress * dPress);
        const simScore = Math.max(70, Math.min(99.5, 100 - dist * 1.5));
        return {
          ...c,
          similarity_score: Math.round(simScore * 10) / 10
        };
      })
      .sort((a, b) => b.similarity_score - a.similarity_score)
      .slice(0, 3);
  }

  const roleColors = {
    'Creative Playmaker': '#38BDF8',
    'Goal-Threat Attacker': '#F43F5E',
    'High-Pressing Midfielder': '#10B981',
    'Defensive Anchor': '#A855F7'
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Header Card */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.15rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Cpu color="#38BDF8" size={20} /> Machine Learning Player Tactical Role Clustering (K-Means + PCA)
        </h3>
        <p className="subtitle">
          Unsupervised clustering profiling players into tactical roles based on pitch depth, pass volume, xG, and defensive pressures.
        </p>
      </div>

      {/* PCA Scatter Chart & Roles Table */}
      <div className="grid-2" style={{ gridTemplateColumns: '1.4fr 1fr' }}>
        <div className="glass-card">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px' }}>2D Principal Component Space (PCA Role Reduction)</h4>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <XAxis type="number" dataKey="pca_x" name="Creation Volume" stroke="#64748B" />
                <YAxis type="number" dataKey="pca_y" name="Defensive Intensity" stroke="#64748B" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ background: '#0F172A', color: '#FFF' }} />
                <Scatter data={clusters} fill="#8884d8">
                  {clusters.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={roleColors[entry.tactical_role] || '#38BDF8'} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card">
          <h4 style={{ fontSize: '1.0rem', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <Users size={16} color="#818CF8" /> Player Roles Breakdown
          </h4>
          <div style={{ overflowY: 'auto', maxHeight: '320px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {clusters.map((c, i) => (
              <div key={i} style={{
                background: 'rgba(8, 12, 20, 0.6)',
                padding: '10px 12px',
                borderRadius: '8px',
                borderLeft: `3px solid ${roleColors[c.tactical_role] || '#38BDF8'}`,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#F8FAFC' }}>{c.player}</div>
                  <div style={{ fontSize: '0.75rem', color: '#94A3B8' }}>{c.team} • {c.official_position || 'Field Player'}</div>
                </div>
                <div style={{ fontSize: '0.78rem', fontWeight: 700, color: roleColors[c.tactical_role] || '#38BDF8' }}>
                  {c.tactical_role}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 1v1 Radar Comparison Tool */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Award color="#38BDF8" size={18} /> ⚔️ 1v1 Player Radar Comparison Tool
        </h3>

        <div className="grid-2" style={{ marginBottom: '20px' }}>
          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Select Player 1:</label>
            <select className="select-field" value={p1} onChange={e => setPlayer1(e.target.value)}>
              {playerNames.map(name => <option key={name} value={name}>{name}</option>)}
            </select>
          </div>
          <div>
            <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Select Player 2:</label>
            <select className="select-field" value={p2} onChange={e => setPlayer2(e.target.value)}>
              {playerNames.map(name => <option key={name} value={name}>{name}</option>)}
            </select>
          </div>
        </div>

        <div style={{ width: '100%', height: 320 }}>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarChartData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="subject" stroke="#94A3B8" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#64748B" />
              <Radar name={p1} dataKey={p1} stroke="#38BDF8" fill="#38BDF8" fillOpacity={0.4} />
              <Radar name={p2} dataKey={p2} stroke="#F43F5E" fill="#F43F5E" fillOpacity={0.4} />
              <Tooltip contentStyle={{ background: '#0F172A', color: '#FFF' }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Real-World Player Similarity Engine */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Search color="#38BDF8" size={18} /> 🔍 Real-World Player Similarity Engine
        </h3>

        <div style={{ marginBottom: '16px', maxWidth: '400px' }}>
          <label style={{ fontSize: '0.78rem', color: '#94A3B8', fontWeight: 700 }}>Select Target Player:</label>
          <select className="select-field" value={target} onChange={e => setTargetPlayer(e.target.value)}>
            {playerNames.map(name => <option key={name} value={name}>{name}</option>)}
          </select>
        </div>

        {targetData && (
          <div style={{ background: 'rgba(8, 12, 20, 0.5)', padding: '14px', borderRadius: '10px', marginBottom: '16px' }}>
            Target Player: <strong style={{ color: '#FFF' }}>{targetData.player}</strong> ({targetData.team}) — Pos: <em>{targetData.official_position || 'Field Player'}</em> | Role: <span style={{ color: '#38BDF8', fontWeight: 700 }}>{targetData.tactical_role}</span>
          </div>
        )}

        <div className="grid-3">
          {similarPlayers.map((sim, i) => (
            <div key={i} className="glass-card" style={{ borderTopColor: '#10B981' }}>
              <div className="metric-title">{sim.team}</div>
              <div style={{ fontWeight: 800, fontSize: '1.05rem', color: '#FFF', marginTop: '4px' }}>{sim.player}</div>
              <div style={{ color: '#94A3B8', fontSize: '0.8rem', marginTop: '2px' }}>Official Pos: {sim.official_position || 'Field Player'}</div>
              <div style={{ color: '#38BDF8', fontSize: '0.85rem', marginTop: '4px' }}>Role: {sim.tactical_role}</div>
              <div style={{ color: '#10B981', fontWeight: 800, marginTop: '6px' }}>Similarity: {sim.similarity_score}%</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
