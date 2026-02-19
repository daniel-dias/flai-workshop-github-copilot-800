import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTeams = async () => {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = `https://${codespace}-8000.app.github.dev/api/teams/`;
      
      console.log('Fetching from Teams API endpoint:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Teams API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams data array:', teamsData);
        
        // Log each team's members for debugging
        if (Array.isArray(teamsData)) {
          teamsData.forEach(team => {
            console.log(`Team: ${team.name}, Members:`, team.members, 'Count:', team.members?.length);
          });
        }
        
        setTeams(Array.isArray(teamsData) ? teamsData : []);
      } catch (err) {
        console.error('Error fetching teams:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading teams...</p>
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
      <h2><i className="bi bi-people-fill me-2"></i>Teams</h2>
      <p className="text-muted mb-4">Join a team and compete together</p>
      
      {teams.length > 0 ? (
        <div className="table-responsive">
          <table className="table table-hover table-striped">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Team Name</th>
                <th scope="col">Members</th>
                <th scope="col">Total Points</th>
              </tr>
            </thead>
            <tbody>
              {teams.map((team, index) => (
                <tr key={team._id || index}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <strong><i className="bi bi-shield-check me-2"></i>{team.name}</strong>
                  </td>
                  <td>
                    <span className="badge bg-info">
                      {team.members?.length || 0} members
                    </span>
                  </td>
                  <td>
                    <span className="badge bg-success">{team.total_points || 0} pts</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="alert alert-info" role="alert">
          <i className="bi bi-info-circle me-2"></i>
          No teams found. Create the first team!
        </div>
      )}
    </div>
  );
};

export default Teams;
