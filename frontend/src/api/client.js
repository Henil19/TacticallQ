import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = {
  // Matches
  getMatches: async (query = '', stage = '') => {
    const params = {};
    if (query) params.query = query;
    if (stage && stage !== 'All') params.stage = stage;
    const response = await axios.get(`${API_BASE_URL}/matches`, { params });
    return response.data;
  },

  // Match Telemetry
  getMatchTelemetry: async (matchId) => {
    const response = await axios.get(`${API_BASE_URL}/matches/${matchId}/telemetry`);
    return response.data;
  },

  // Match Events & Spatial Data
  getMatchEvents: async (matchId) => {
    const response = await axios.get(`${API_BASE_URL}/matches/${matchId}/events`);
    return response.data;
  },

  // Player Stats & ML Role Clustering
  getPlayerStatsAndClustering: async (matchId) => {
    const response = await axios.get(`${API_BASE_URL}/matches/${matchId}/player-stats`);
    return response.data;
  },

  // AI Tactical Report
  generateAIReport: async (matchId, apiKey = null) => {
    const response = await axios.post(`${API_BASE_URL}/ai/report`, {
      match_id: matchId,
      api_key: apiKey
    });
    return response.data;
  },

  // AI Scout Q&A
  runAIScoutQuery: async (matchId, query, apiKey = null) => {
    const response = await axios.post(`${API_BASE_URL}/ai/scout`, {
      match_id: matchId,
      query,
      api_key: apiKey
    });
    return response.data;
  },

  // AI Counter-Strategy Simulator
  simulateCounterStrategy: async (opponentTeam, formation, playstyle, keyPlayer, apiKey = null) => {
    const response = await axios.post(`${API_BASE_URL}/ai/counter-strategy`, {
      opponent_team: opponentTeam,
      formation,
      playstyle,
      key_player: keyPlayer,
      api_key: apiKey
    });
    return response.data;
  },

  // Tournament Leaderboards
  getLeaderboards: async () => {
    const response = await axios.get(`${API_BASE_URL}/leaderboards`);
    return response.data;
  },

  // Head-to-Head Cross-Fixture Comparison
  getHeadToHead: async (matchAId, matchBId) => {
    const response = await axios.get(`${API_BASE_URL}/head-to-head`, {
      params: { match_a_id: matchAId, match_b_id: matchBId }
    });
    return response.data;
  }
};
