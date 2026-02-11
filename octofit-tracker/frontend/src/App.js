import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Workouts from './components/Workouts';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">OctoFit Tracker</Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-5">
              <div className="jumbotron">
                <h1 className="display-4">Welcome to OctoFit Tracker</h1>
                <p className="lead">Track your fitness activities, compete with teams, and achieve your goals!</p>
                <hr className="my-4" style={{borderColor: 'rgba(255,255,255,0.3)'}} />
                <p>Use the navigation menu above to explore different sections of the app.</p>
                <div className="row mt-4">
                  <div className="col-md-6 mb-3">
                    <Link to="/users" className="text-decoration-none">
                      <div className="card bg-light" style={{cursor: 'pointer'}}>
                        <div className="card-body">
                          <h5 className="card-title text-dark">👥 Users</h5>
                          <p className="card-text text-dark">Browse all registered users and their fitness profiles.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-6 mb-3">
                    <Link to="/activities" className="text-decoration-none">
                      <div className="card bg-light" style={{cursor: 'pointer'}}>
                        <div className="card-body">
                          <h5 className="card-title text-dark">📊 Activities</h5>
                          <p className="card-text text-dark">Log your workouts and monitor your progress over time.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-6 mb-3">
                    <Link to="/leaderboard" className="text-decoration-none">
                      <div className="card bg-light" style={{cursor: 'pointer'}}>
                        <div className="card-body">
                          <h5 className="card-title text-dark">🏆 Leaderboard</h5>
                          <p className="card-text text-dark">Challenge friends and climb the leaderboard rankings.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-6 mb-3">
                    <Link to="/teams" className="text-decoration-none">
                      <div className="card bg-light" style={{cursor: 'pointer'}}>
                        <div className="card-body">
                          <h5 className="card-title text-dark">👥 Teams</h5>
                          <p className="card-text text-dark">Collaborate with others and reach fitness goals together.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-6 mb-3">
                    <Link to="/workouts" className="text-decoration-none">
                      <div className="card bg-light" style={{cursor: 'pointer'}}>
                        <div className="card-body">
                          <h5 className="card-title text-dark">💪 Workouts</h5>
                          <p className="card-text text-dark">Receive personalized workout recommendations.</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
