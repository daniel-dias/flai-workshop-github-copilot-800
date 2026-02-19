import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = `https://${codespace}-8000.app.github.dev/api/leaderboard/`;
      
      console.log('Fetching from Leaderboard API endpoint:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Leaderboard API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
      } catch (err) {
        console.error('Error fetching leaderboard:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  const getRankClass = (rank) => {
    if (rank === 1) return 'table-warning';
    if (rank === 2) return 'table-secondary';
    if (rank === 3) return 'table-info';
    return '';
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading leaderboard...</p>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2><i className="bi bi-trophy me-2"></i>Leaderboard</h2>
      <p className="text-muted mb-4">Top performers and competitive rankings</p>
      
      {leaderboard.length > 0 ? (
        <div className="table-responsive">
          <table className="table table-hover table-striped">
            <thead>
              <tr>
                <th scope="col">Rank</th>
                <th scope="col">User</th>
                <th scope="col">Team</th>
                <th scope="col">Total Calories</th>
                <th scope="col">Activities Completed</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((entry, index) => {
                const rank = index + 1;
                return (
                  <tr key={entry._id || index} className={getRankClass(rank)}>
                    <th scope="row">
                      <strong>{getRankBadge(rank)}</strong>
                    </th>
                    <td>
                      <strong><i className="bi bi-person-badge me-2"></i>{entry.user_name || 'Unknown User'}</strong>
                    </td>
                    <td>
                      <span className="badge bg-info">{entry.team || 'No Team'}</span>
                    </td>
                    <td>
                      <span className="badge bg-primary">{entry.total_calories || 0} cal</span>
                    </td>
                    <td>
                      <span className="badge bg-success">{entry.total_activities || 0}</span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="alert alert-info" role="alert">
          <i className="bi bi-info-circle me-2"></i>
          No leaderboard data available. Start competing today!
        </div>
      )}
    </div>
  );
};

export default Leaderboard;
