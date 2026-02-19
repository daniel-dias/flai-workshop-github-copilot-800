import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWorkouts = async () => {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = `https://${codespace}-8000.app.github.dev/api/workouts/`;
      
      console.log('Fetching from Workouts API endpoint:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Workouts API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
      } catch (err) {
        console.error('Error fetching workouts:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  const getDifficultyBadge = (difficulty) => {
    const badges = {
      'beginner': 'bg-success',
      'intermediate': 'bg-warning',
      'advanced': 'bg-danger',
      'easy': 'bg-success',
      'medium': 'bg-warning',
      'hard': 'bg-danger'
    };
    return badges[difficulty?.toLowerCase()] || 'bg-secondary';
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading workouts...</p>
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
      <h2><i className="bi bi-heart-pulse me-2"></i>Workouts</h2>
      <p className="text-muted mb-4">Personalized workout suggestions for your fitness goals</p>
      
      {workouts.length > 0 ? (
        <div className="table-responsive">
          <table className="table table-hover table-striped">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Workout Name</th>
                <th scope="col">Description</th>
                <th scope="col">Duration (min)</th>
                <th scope="col">Difficulty</th>
                <th scope="col">Category</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map((workout, index) => (
                <tr key={workout._id || index}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <strong><i className="bi bi-lightning-charge me-2"></i>{workout.name}</strong>
                  </td>
                  <td>{workout.description}</td>
                  <td>
                    <span className="badge bg-primary">{workout.duration}</span>
                  </td>
                  <td>
                    <span className={`badge ${getDifficultyBadge(workout.difficulty)}`}>
                      {workout.difficulty}
                    </span>
                  </td>
                  <td>{workout.category}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="alert alert-info" role="alert">
          <i className="bi bi-info-circle me-2"></i>
          No workouts found. Check back soon for new workout suggestions!
        </div>
      )}
    </div>
  );
};

export default Workouts;
