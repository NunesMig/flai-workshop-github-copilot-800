import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const apiUrl = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;
    console.log('Fetching from Workouts API endpoint:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Fetched Workouts data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger error-message" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  const getDifficultyColor = (level) => {
    switch(level?.toLowerCase()) {
      case 'beginner': return 'success';
      case 'intermediate': return 'warning';
      case 'advanced': return 'danger';
      default: return 'secondary';
    }
  };

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>Workout Recommendations</h2>
        <p className="mb-0">Personalized workouts tailored to your fitness level</p>
      </div>
      <div className="row">
        {workouts.map((workout) => {
          const difficultyLevel = workout.difficulty_level || workout.fitness_level;
          const workoutType = workout.workout_type || workout.activity_type;
          const duration = workout.duration || workout.duration_minutes;
          
          return (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{workout.name}</h5>
                  <p className="card-text">{workout.description}</p>
                  <hr />
                  <div className="mb-2">
                    <strong>Type:</strong>{' '}
                    <span className="badge bg-info">{workoutType}</span>
                  </div>
                  <div className="mb-2">
                    <strong>Duration:</strong> {duration} minutes
                  </div>
                  <div className="mb-2">
                    <strong>Difficulty:</strong>{' '}
                    <span className={`badge bg-${getDifficultyColor(difficultyLevel)}`}>
                      {difficultyLevel}
                    </span>
                  </div>
                  {workout.equipment_needed && (
                    <div className="mb-2">
                      <strong>Equipment:</strong> {workout.equipment_needed}
                    </div>
                  )}
                  {workout.instructions && (
                    <div className="mb-2">
                      <strong>Instructions:</strong>
                      <p className="small text-muted">{workout.instructions.substring(0, 100)}...</p>
                    </div>
                  )}
                </div>
                <div className="card-footer bg-transparent">
                  <button className="btn btn-sm btn-primary w-100">
                    Start Workout
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Workouts;
