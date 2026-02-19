import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUsers = async () => {
      const codespace = process.env.REACT_APP_CODESPACE_NAME;
      const apiUrl = `https://${codespace}-8000.app.github.dev/api/users/`;
      
      console.log('Fetching from Users API endpoint:', apiUrl);
      
      try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Users API Response:', data);
        
        // Handle both paginated (.results) and plain array responses
        const usersData = data.results || data;
        setUsers(Array.isArray(usersData) ? usersData : []);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
        <p className="mt-3">Loading users...</p>
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
      <h2><i className="bi bi-people me-2"></i>Users</h2>
      <p className="text-muted mb-4">Community members and their profiles</p>
      
      {users.length > 0 ? (
        <div className="table-responsive">
          <table className="table table-hover table-striped">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Name</th>
                <th scope="col">Email</th>
                <th scope="col">Team</th>
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user, index) => (
                <tr key={user._id || index}>
                  <th scope="row">{index + 1}</th>
                  <td>
                    <strong><i className="bi bi-person-circle me-2"></i>{user.name}</strong>
                  </td>
                  <td>{user.email}</td>
                  <td>
                    <span className="badge bg-info">{user.team || 'No Team'}</span>
                  </td>
                  <td>
                    <span className="badge bg-success">Active</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="alert alert-info" role="alert">
          <i className="bi bi-info-circle me-2"></i>
          No users found.
        </div>
      )}
    </div>
  );
};

export default Users;
