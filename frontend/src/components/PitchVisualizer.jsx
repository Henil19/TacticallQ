import React, { useState } from 'react';
import { Target, Share2, Flame, ArrowUpRight, Shield, Activity } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export default function PitchVisualizer({ telemetry, eventsData }) {
  const [activeLayer, setActiveLayer] = useState('shots');
  const [shotTeamFilter, setShotTeamFilter] = useState('All');

  if (!telemetry || !eventsData) return null;

  const matchInfo = telemetry.match_info || {};
  const homeTeam = matchInfo.home_team || 'Home';
  const awayTeam = matchInfo.away_team || 'Away';

  const shots = eventsData.shots || [];
  const passLinks = eventsData.pass_links || [];
  const avgPositions = eventsData.average_positions || [];
  const disruptions = eventsData.disruptions || [];
  const keyPasses = telemetry.key_passes || [];
  const defLine = telemetry.defensive_line_height || {};
  const fieldPressure = telemetry.field_thirds_pressure || {};
  const momentum = telemetry.match_momentum || {};

  const filteredShots = shotTeamFilter === 'All'
    ? shots
    : shots.filter(s => s.team === shotTeamFilter);

  // Recharts data for momentum subtab
  const momentumIntervals = momentum.intervals || [];
  const momentumScores = momentum.momentum || {};
  const momentumChartData = momentumIntervals.map((intv, idx) => {
    const item = { interval: intv };
    Object.keys(momentumScores).forEach(t => {
      item[t] = momentumScores[t][idx] || 0;
    });
    return item;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Subtabs Selector */}
      <div className="tabs-nav">
        <button className={`tab-btn ${activeLayer === 'shots' ? 'active' : ''}`} onClick={() => setActiveLayer('shots')}>
          <Target size={15} /> Dual-Goal Shot Quality Map
        </button>
        <button className={`tab-btn ${activeLayer === 'passes' ? 'active' : ''}`} onClick={() => setActiveLayer('passes')}>
          <Share2 size={15} /> Pass Networks & Formations
        </button>
        <button className={`tab-btn ${activeLayer === 'pressure' ? 'active' : ''}`} onClick={() => setActiveLayer('pressure')}>
          <Flame size={15} /> Pressure Density & Field Thirds
        </button>
        <button className={`tab-btn ${activeLayer === 'keypasses' ? 'active' : ''}`} onClick={() => setActiveLayer('keypasses')}>
          <ArrowUpRight size={15} /> Key Pass & xA Creation Vectors
        </button>
        <button className={`tab-btn ${activeLayer === 'defline' ? 'active' : ''}`} onClick={() => setActiveLayer('defline')}>
          <Shield size={15} /> Defensive Line Height & Disruptions
        </button>
        <button className={`tab-btn ${activeLayer === 'momentum' ? 'active' : ''}`} onClick={() => setActiveLayer('momentum')}>
          <Activity size={15} /> Match Momentum Flow
        </button>
      </div>

      {/* Main Visualizer Area */}
      {activeLayer === 'momentum' ? (
        <div className="glass-card">
          <h3 style={{ fontSize: '1.1rem', marginBottom: '16px' }}>15-Minute Tactical Match Momentum Index</h3>
          <div style={{ width: '100%', height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={momentumChartData}>
                <XAxis dataKey="interval" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" />
                <Tooltip contentStyle={{ background: '#0F172A', borderColor: 'rgba(255,255,255,0.1)', color: '#FFF' }} />
                <Area type="monotone" dataKey={homeTeam} stroke="#38BDF8" fill="#38BDF8" fillOpacity={0.25} strokeWidth={2.5} />
                <Area type="monotone" dataKey={awayTeam} stroke="#F43F5E" fill="#F43F5E" fillOpacity={0.25} strokeWidth={2.5} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      ) : (
        <div className="grid-2" style={{ gridTemplateColumns: activeLayer === 'shots' ? '2.4fr 1fr' : '1fr' }}>
          {/* SVG Pitch Canvas */}
          <div className="glass-card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {activeLayer === 'shots' && (
              <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                <span style={{ fontSize: '0.8rem', color: '#94A3B8', fontWeight: 600 }}>Filter Team Shots:</span>
                {['All', homeTeam, awayTeam].map(tm => (
                  <button
                    key={tm}
                    onClick={() => setShotTeamFilter(tm)}
                    style={{
                      padding: '4px 12px',
                      borderRadius: '16px',
                      border: 'none',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                      background: shotTeamFilter === tm ? '#38BDF8' : 'rgba(30, 41, 59, 0.8)',
                      color: shotTeamFilter === tm ? '#000' : '#FFF'
                    }}
                  >
                    {tm}
                  </button>
                ))}
              </div>
            )}

            {/* Standard 120 x 80 Yard Pitch Graphic */}
            <svg viewBox="-5 -5 130 90" style={{ width: '100%', height: 'auto', background: '#0C1527', borderRadius: '12px', border: '1px solid #334155' }}>
              {/* Pitch Boundaries & Center Line */}
              <rect x="0" y="0" width="120" height="80" fill="none" stroke="#334155" strokeWidth="1.2" />
              <line x1="60" y1="0" x2="60" y2="80" stroke="#334155" strokeWidth="1.2" />
              <circle cx="60" cy="40" r="9.15" fill="none" stroke="#334155" strokeWidth="1.2" />
              <circle cx="60" cy="40" r="1" fill="#334155" />

              {/* Penalty Areas */}
              <rect x="0" y="18" width="18" height="44" fill="none" stroke="#334155" strokeWidth="1.2" />
              <rect x="0" y="30" width="6" height="20" fill="none" stroke="#334155" strokeWidth="1.0" />
              <rect x="102" y="18" width="18" height="44" fill="none" stroke="#334155" strokeWidth="1.2" />
              <rect x="114" y="30" width="6" height="20" fill="none" stroke="#334155" strokeWidth="1.0" />

              {/* Pitch Labels */}
              <text x="5" y="77" fill="#64748B" fontSize="3" fontWeight="bold">{homeTeam} Attacking Goal ➔</text>
              <text x="115" y="77" fill="#64748B" fontSize="3" fontWeight="bold" textAnchor="end">🧠 {awayTeam} Attacking Goal</text>

              {/* LAYER 1: Dual-Goal Shot Quality Map */}
              {activeLayer === 'shots' && filteredShots.map((shot, i) => {
                const isHome = shot.team === homeTeam;
                const plotX = isHome ? (shot.start_x || 100) : (120.0 - (shot.start_x || 100));
                const plotY = isHome ? (shot.start_y || 40) : (80.0 - (shot.start_y || 40));
                const r = Math.max(1.8, Math.min(5.5, (shot.xg || 0.1) * 12));

                let color = '#F59E0B'; // Saved
                if (shot.shot_outcome === 'Goal') color = '#10B981';
                else if (shot.shot_outcome === 'Off T') color = '#EF4444';
                else if (shot.shot_outcome === 'Blocked') color = '#6B7280';

                return (
                  <g key={i}>
                    <circle cx={plotX} cy={plotY} r={r} fill={color} fillOpacity={0.75} stroke="#FFF" strokeWidth="0.5">
                      <title>{`${shot.player || 'Player'} (${shot.team}) - xG: ${shot.xg?.toFixed(2)} - Outcome: ${shot.shot_outcome}`}</title>
                    </circle>
                  </g>
                );
              })}

              {/* LAYER 2: Pass Networks & Average Positions */}
              {activeLayer === 'passes' && (
                <>
                  {/* Pass Links */}
                  {passLinks.map((link, i) => {
                    const p1 = avgPositions.find(p => p.player === link.player);
                    const p2 = avgPositions.find(p => p.player === link.pass_recipient);
                    if (!p1 || !p2) return null;
                    return (
                      <line
                        key={i}
                        x1={p1.avg_x} y1={p1.avg_y}
                        x2={p2.avg_x} y2={p2.avg_y}
                        stroke={p1.team === homeTeam ? '#38BDF8' : '#F43F5E'}
                        strokeWidth={Math.min(2.5, link.pass_count * 0.4)}
                        strokeOpacity={0.6}
                      />
                    );
                  })}

                  {/* Player Nodes */}
                  {avgPositions.map((pos, i) => {
                    const isHome = pos.team === homeTeam;
                    return (
                      <g key={i}>
                        <circle cx={pos.avg_x} cy={pos.avg_y} r="3.2" fill={isHome ? '#38BDF8' : '#F43F5E'} stroke="#FFF" strokeWidth="0.6" />
                        <text x={pos.avg_x} y={pos.avg_y + 6} fill="#FFF" fontSize="2.2" textAnchor="middle" fontWeight="bold">
                          {pos.player?.split(' ').pop()}
                        </text>
                      </g>
                    );
                  })}
                </>
              )}

              {/* LAYER 3: Key Pass xA Vectors */}
              {activeLayer === 'keypasses' && keyPasses.map((kp, i) => {
                if (!kp.start_x || !kp.end_x) return null;
                const isHome = kp.team === homeTeam;
                const sx = isHome ? kp.start_x : (120.0 - kp.start_x);
                const sy = isHome ? kp.start_y : (80.0 - kp.start_y);
                const ex = isHome ? kp.end_x : (120.0 - kp.end_x);
                const ey = isHome ? kp.end_y : (80.0 - kp.end_y);

                return (
                  <g key={i}>
                    <line x1={sx} y1={sy} x2={ex} y2={ey} stroke="#10B981" strokeWidth="1.4" strokeDasharray="1.5,1.5" />
                    <circle cx={ex} cy={ey} r="1.8" fill="#10B981" />
                  </g>
                );
              })}

              {/* LAYER 4: Defensive Line Height & Disruptions */}
              {activeLayer === 'defline' && (
                <>
                  {Object.keys(defLine).map((tm, idx) => {
                    const info = defLine[tm];
                    const h = info.avg_line_height_yards || 45;
                    const lineX = idx === 0 ? h : (120.0 - h);
                    const color = idx === 0 ? '#38BDF8' : '#F43F5E';

                    return (
                      <g key={tm}>
                        <line x1={lineX} y1="0" x2={lineX} y2="80" stroke={color} strokeWidth="1.8" strokeDasharray="3,3" />
                        <rect x={idx === 0 ? lineX : lineX - 25} y={10 + idx * 25} width="25" height="12" fill="#0F172A" stroke={color} rx="2" strokeWidth="0.8" />
                        <text x={idx === 0 ? lineX + 12.5 : lineX - 12.5} y={17 + idx * 25} fill="#FFF" fontSize="2.3" textAnchor="middle" fontWeight="bold">
                          {tm}: {h}yds ({info.block_type})
                        </text>
                      </g>
                    );
                  })}

                  {disruptions.map((dis, i) => {
                    if (!dis.start_x) return null;
                    const isHome = dis.team === homeTeam;
                    const dx = isHome ? dis.start_x : (120.0 - dis.start_x);
                    const dy = isHome ? dis.start_y : (80.0 - dis.start_y);

                    return (
                      <circle key={i} cx={dx} cy={dy} r="1.5" fill={isHome ? '#38BDF8' : '#F43F5E'} fillOpacity={0.6} />
                    );
                  })}
                </>
              )}
            </svg>

            {/* Pitch Legend */}
            <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', fontSize: '0.78rem', color: '#94A3B8' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10B981', display: 'inline-block' }}></span> Goal
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#F59E0B', display: 'inline-block' }}></span> Saved
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#EF4444', display: 'inline-block' }}></span> Off Target
              </span>
              <span style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#6B7280', display: 'inline-block' }}></span> Blocked
              </span>
            </div>
          </div>

          {/* Shot Details Table Sidebar (when activeLayer is 'shots') */}
          {activeLayer === 'shots' && (
            <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h4 style={{ fontSize: '0.95rem' }}>📋 Shot Events Log</h4>
              <div style={{ overflowY: 'auto', maxHeight: '380px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {filteredShots.map((s, idx) => (
                  <div key={idx} style={{
                    background: 'rgba(8, 12, 20, 0.6)',
                    padding: '8px 10px',
                    borderRadius: '8px',
                    fontSize: '0.8rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    borderLeft: `3px solid ${s.shot_outcome === 'Goal' ? '#10B981' : '#F59E0B'}`
                  }}>
                    <div>
                      <div style={{ fontWeight: 700, color: '#F8FAFC' }}>{s.player || 'Player'} ({s.team})</div>
                      <div style={{ color: '#94A3B8', fontSize: '0.72rem' }}>Min {s.minute}' • {s.body_part || 'Foot'}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ color: '#38BDF8', fontWeight: 800 }}>xG {s.xg?.toFixed(2)}</div>
                      <div style={{ fontSize: '0.72rem', color: s.shot_outcome === 'Goal' ? '#10B981' : '#94A3B8' }}>{s.shot_outcome}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Field Thirds Pressure Card */}
      {fieldPressure && Object.keys(fieldPressure).length > 0 && (
        <div className="glass-card">
          <h3 style={{ fontSize: '1.05rem', marginBottom: '12px' }}>Field Thirds Defensive Pressure Intensity</h3>
          <div className="grid-2">
            {Object.keys(fieldPressure).map(tm => {
              const pdata = fieldPressure[tm];
              return (
                <div key={tm} style={{ background: 'rgba(8, 12, 20, 0.5)', padding: '14px', borderRadius: '10px' }}>
                  <h4 style={{ color: '#38BDF8', fontSize: '0.95rem', marginBottom: '8px' }}>{tm} ({pdata.total_pressures} Pressures)</h4>
                  <div style={{ fontSize: '0.82rem', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <div>
                      <span>Attacking Third: {pdata.attraction_third} ({pdata.att_pct}%)</span>
                      <div className="progress-bar-bg"><div className="progress-bar-fill" style={{ width: `${pdata.att_pct}%` }}></div></div>
                    </div>
                    <div>
                      <span>Midfield Third: {pdata.midfield_third} ({pdata.mid_pct}%)</span>
                      <div className="progress-bar-bg"><div className="progress-bar-fill" style={{ width: `${pdata.mid_pct}%` }}></div></div>
                    </div>
                    <div>
                      <span>Defensive Third: {pdata.defensive_third} ({pdata.def_pct}%)</span>
                      <div className="progress-bar-bg"><div className="progress-bar-fill" style={{ width: `${pdata.def_pct}%` }}></div></div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
