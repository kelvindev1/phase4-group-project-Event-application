import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import RegisterForm from './components/RegisterForm';
import Home from './components/Home'; // Import Home component
import './App.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  const handleRegister = () => {
    // Handle registration success or any other actions as needed
    // For simplicity, just update authentication state
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Routes>
            <Route path="/" element={<Navigate to={isAuthenticated ? '/home' : '/login'} />} />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/register" element={<RegisterForm onRegister={handleRegister} />} />
            {/* Conditionally render Home or Login based on isAuthenticated */}
            {isAuthenticated ? (
              <Route path="/home" element={<Home onLogout={handleLogout} />} />
            ) : (
              <Route path="/home" element={<Navigate to="/login" />} />
            )}
          </Routes>
        </header>
      </div>
    </Router>
  );
}

export default App;
