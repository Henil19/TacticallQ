import React, { useState } from 'react';
import { Target, Trophy, Flame, Download, Bot, Sparkles, TrendingUp, CheckCircle2 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
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
        .replace(/^[⚽📋🛡️⚡🎯🚀🔥💡]\s*/, '')
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
                SECTION {secIdx + 1}
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

export default function MatchOverview({ telemetry, apiKey }) {
  const [aiReport, setAiReport] = useState('');
  const [loadingReport, setLoadingReport] = useState(false);

  if (!telemetry) return null;

  const matchInfo = telemetry.match_info || {};
  const xgSummary = telemetry.xg_summary || {};
  const homeTeam = matchInfo.home_team || 'Home';
  const awayTeam = matchInfo.away_team || 'Away';

  const hXg = xgSummary[homeTeam]?.total_xg || 0;
  const aXg = xgSummary[awayTeam]?.total_xg || 0;
  const hShots = xgSummary[homeTeam]?.total_shots || 0;
  const aShots = xgSummary[awayTeam]?.total_shots || 0;

  const totXg = Math.max(0.1, hXg + aXg);
  const totShots = Math.max(1, hShots + aShots);

  // Format Recharts data for cumulative xG timeline
  const cumXgData = telemetry.cumulative_xg_timeline || {};
  const chartData = [];
  const homeTimeline = cumXgData[homeTeam]?.minutes || [];
  const homeValues = cumXgData[homeTeam]?.cum_xg || [];
  const awayValues = cumXgData[awayTeam]?.cum_xg || [];

  for (let i = 0; i < homeTimeline.length; i++) {
    chartData.push({
      minute: `${homeTimeline[i]}'`,
      [homeTeam]: homeValues[i] || 0,
      [awayTeam]: awayValues[i] || 0
    });
  }

  const handleGenerateReport = async () => {
    setLoadingReport(true);
    try {
      const res = await apiClient.generateAIReport(matchInfo.match_id, apiKey);
      setAiReport(res.report);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingReport(false);
    }
  };

  const handleDownloadDossier = () => {
    const dossierText = `# TacticalIQ Match Scouting Dossier: ${homeTeam} vs ${awayTeam}
Date: ${matchInfo.match_date || '2024'} | Stage: ${matchInfo.stage || 'Euro 2024'}
Scoreline: ${homeTeam} ${matchInfo.home_score} - ${matchInfo.away_score} ${awayTeam}
Total xG: ${homeTeam} (${hXg.toFixed(2)}) | ${awayTeam} (${aXg.toFixed(2)})

${aiReport || 'Click "Generate AI Match Report" to synthesize full LLM analysis.'}
`;
    const element = document.createElement('a');
    const file = new Blob([dossierText], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `TacticalIQ_Scouting_Report_${homeTeam}_vs_${awayTeam}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Metric Cards */}
      <div className="grid-4">
        <div className="glass-card">
          <div className="metric-title"><Trophy size={14} color="#38BDF8" /> Fixture</div>
          <div className="metric-value" style={{ fontSize: '1.25rem' }}>{homeTeam} vs {awayTeam}</div>
          <div className="metric-sub">{matchInfo.stage || 'Euro 2024'}</div>
        </div>

        <div className="glass-card card-indigo">
          <div className="metric-title"><Trophy size={14} color="#818CF8" /> Scoreline</div>
          <div className="metric-value">{matchInfo.home_score ?? 0} - {matchInfo.away_score ?? 0}</div>
          <div className="metric-sub" style={{ color: '#818CF8' }}>Full Time Result</div>
        </div>

        <div className="glass-card card-emerald">
          <div className="metric-title"><Target size={14} color="#10B981" /> {homeTeam} xG</div>
          <div className="metric-value">{hXg.toFixed(2)}</div>
          <div className="metric-sub" style={{ color: '#10B981' }}>{hShots} Shots Attempts</div>
        </div>

        <div className="glass-card card-crimson">
          <div className="metric-title"><Target size={14} color="#F43F5E" /> {awayTeam} xG</div>
          <div className="metric-value">{aXg.toFixed(2)}</div>
          <div className="metric-sub" style={{ color: '#F43F5E' }}>{aShots} Shots Attempts</div>
        </div>
      </div>

      {/* Head to Head Progress Bars */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Flame color="#38BDF8" size={18} /> Team Head-to-Head Comparison ({homeTeam} vs {awayTeam})
        </h3>
        
        <div className="grid-2">
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', fontWeight: 600 }}>
              <span>Expected Goals ($xG$) Share</span>
              <span style={{ color: '#38BDF8' }}>{homeTeam} ({hXg.toFixed(2)}) vs {awayTeam} ({aXg.toFixed(2)})</span>
            </div>
            <div className="progress-bar-bg">
              <div className="progress-bar-fill" style={{ width: `${(hXg / totXg) * 100}%` }}></div>
            </div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.88rem', fontWeight: 600 }}>
              <span>Total Shot Attempts Share</span>
              <span style={{ color: '#818CF8' }}>{homeTeam} ({hShots}) vs {awayTeam} ({aShots})</span>
            </div>
            <div className="progress-bar-bg">
              <div className="progress-bar-fill" style={{ width: `${(hShots / totShots) * 100}%`, background: 'linear-gradient(90deg, #818CF8 0%, #F43F5E 100%)' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Recharts Cumulative xG Timeline */}
      <div className="glass-card">
        <h3 style={{ fontSize: '1.1rem', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <TrendingUp color="#38BDF8" size={18} /> Match Momentum: Cumulative Expected Goals (xG) Timeline
        </h3>
        <p className="subtitle" style={{ marginBottom: '16px' }}>
          Tracks minute-by-minute cumulative team xG trajectory over 90 minutes.
        </p>

        <div style={{ width: '100%', height: 260 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="gradHome" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#38BDF8" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#38BDF8" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="gradAway" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#F43F5E" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#F43F5E" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="minute" stroke="#64748B" />
              <YAxis stroke="#64748B" />
              <Tooltip contentStyle={{ background: '#0F172A', borderColor: 'rgba(255,255,255,0.1)', color: '#FFF' }} />
              <Area type="monotone" dataKey={homeTeam} stroke="#38BDF8" fillOpacity={1} fill="url(#gradHome)" strokeWidth={2.5} />
              <Area type="monotone" dataKey={awayTeam} stroke="#F43F5E" fillOpacity={1} fill="url(#gradAway)" strokeWidth={2.5} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Executive AI Match Report Section */}
      <div className="glass-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px', marginBottom: '16px' }}>
          <div>
            <h3 style={{ fontSize: '1.1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Bot color="#38BDF8" size={20} /> AI Executive Tactical Match Report
            </h3>
            <p className="subtitle">Real-time LLM synthesis of spatial telemetry and news context.</p>
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <button onClick={handleDownloadDossier} className="btn-secondary">
              <Download size={15} /> Export Dossier (.md)
            </button>
            <button onClick={handleGenerateReport} className="btn-primary" disabled={loadingReport}>
              <Sparkles size={15} /> {loadingReport ? 'Synthesizing...' : 'Generate AI Match Report'}
            </button>
          </div>
        </div>

        {aiReport ? (
          <PointWiseCardList text={aiReport} accentColor="#38BDF8" />
        ) : (
          <div style={{ textAlign: 'center', padding: '30px', color: '#64748B', background: 'rgba(8, 12, 20, 0.4)', borderRadius: '12px' }}>
            Click <strong>Generate AI Match Report</strong> to produce a real-time tactical synthesis for this fixture.
          </div>
        )}
      </div>
    </div>
  );
}

