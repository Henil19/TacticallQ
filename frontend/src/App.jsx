import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import MatchOverview from './components/MatchOverview';
import PitchVisualizer from './components/PitchVisualizer';
import MLClustering from './components/MLClustering';
import AIScout from './components/AIScout';
import HeadToHead from './components/HeadToHead';
import Leaderboards from './components/Leaderboards';
import { apiClient } from './api/client';
import { BarChart3, Target, Cpu, Bot, Swords, Trophy } from 'lucide-react';

export default function App() {
  const [matches, setMatches] = useState([]);
  const [stages, setStages] = useState(['All']);
  const [selectedMatchId, setSelectedMatchId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedStage, setSelectedStage] = useState('All');
  const [apiKey, setApiKey] = useState('');

  const [activeTab, setActiveTab] = useState('overview');
  const [telemetry, setTelemetry] = useState(null);
  const [eventsData, setEventsData] = useState(null);
  const [playerStatsData, setPlayerStatsData] = useState(null);
  const [loading, setLoading] = useState(false);

  // Load matches index on mount & when filter changes
  useEffect(() => {
    fetchMatches();
  }, [searchQuery, selectedStage]);

  const fetchMatches = async () => {
    try {
      const data = await apiClient.getMatches(searchQuery, selectedStage);
      setMatches(data.matches || []);
      setStages(data.stages || ['All']);
      if (data.matches.length > 0 && !selectedMatchId) {
        setSelectedMatchId(data.matches[0].match_id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Load match telemetry & events when selectedMatchId changes
  useEffect(() => {
    if (selectedMatchId) {
      loadMatchDetails(selectedMatchId);
    }
  }, [selectedMatchId]);

  const loadMatchDetails = async (mId) => {
    setLoading(true);
    try {
      const [tData, eData, pData] = await Promise.all([
        apiClient.getMatchTelemetry(mId),
        apiClient.getMatchEvents(mId),
        apiClient.getPlayerStatsAndClustering(mId)
      ]);
      setTelemetry(tData);
      setEventsData(eData);
      setPlayerStatsData(pData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        matches={matches}
        stages={stages}
        selectedMatchId={selectedMatchId}
        setSelectedMatchId={setSelectedMatchId}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        selectedStage={selectedStage}
        setSelectedStage={setSelectedStage}
      />

      {/* Main App Workspace */}
      <div className="main-content">
        {/* Executive Header Banner */}
        <Header
          matchInfo={telemetry?.match_info}
          eventCount={telemetry?.total_events || 0}
          apiKey={apiKey}
          setApiKey={setApiKey}
        />

        {/* Executive Top Navigation Tabs */}
        <div style={{ marginTop: '20px' }}>
          <div className="tabs-nav">
            <button className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
              <BarChart3 size={16} /> 📊 Match Overview & AI Report
            </button>

            <button className={`tab-btn ${activeTab === 'spatial' ? 'active' : ''}`} onClick={() => setActiveTab('spatial')}>
              <Target size={16} /> 🎯 xG & Spatial Pitch Analytics
            </button>

            <button className={`tab-btn ${activeTab === 'ml' ? 'active' : ''}`} onClick={() => setActiveTab('ml')}>
              <Cpu size={16} /> 🤖 ML Player Role Clustering
            </button>

            <button className={`tab-btn ${activeTab === 'scout' ? 'active' : ''}`} onClick={() => setActiveTab('scout')}>
              <Bot size={16} /> 🔍 AI Scout & Live Web Search
            </button>

            <button className={`tab-btn ${activeTab === 'h2h' ? 'active' : ''}`} onClick={() => setActiveTab('h2h')}>
              <Swords size={16} /> ⚔️ Cross-Fixture Head-to-Head
            </button>

            <button className={`tab-btn ${activeTab === 'leaderboards' ? 'active' : ''}`} onClick={() => setActiveTab('leaderboards')}>
              <Trophy size={16} /> 🏆 Tournament Leaderboards
            </button>
          </div>
        </div>

        {/* Tab Body View */}
        <div className="content-body">
          {loading ? (
            <div style={{ textAlign: 'center', padding: '60px', color: '#38BDF8', fontWeight: 700 }}>
              Ingesting telemetry tokens and computing spatial analytics...
            </div>
          ) : (
            <>
              {activeTab === 'overview' && (
                <MatchOverview telemetry={telemetry} apiKey={apiKey} />
              )}

              {activeTab === 'spatial' && (
                <PitchVisualizer telemetry={telemetry} eventsData={eventsData} />
              )}

              {activeTab === 'ml' && (
                <MLClustering playerStatsData={playerStatsData} />
              )}

              {activeTab === 'scout' && (
                <AIScout matchInfo={telemetry?.match_info} apiKey={apiKey} />
              )}

              {activeTab === 'h2h' && (
                <HeadToHead matches={matches} />
              )}

              {activeTab === 'leaderboards' && (
                <Leaderboards />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
