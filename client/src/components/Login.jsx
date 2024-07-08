import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import './Login.css';

const Login = ({ onLogin }) => {
  const [usernameOrEmail, setUsernameOrEmail] = useState('');
  const [password, setPassword] = useState('');

  const [passwordVisible, setPasswordVisible] = useState(false);
  const [message, setMessage] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      username_or_email: usernameOrEmail,
      password,
    };

    try {
      const response = await axios.post('http://localhost:5000/login', userData);
      console.log(response.data);
      setMessage('Login successful');
      onLogin();
      navigate('/home', { replace: true });
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setMessage('Invalid username or password');
      } else {
        setMessage('Login failed. Please try again later.');
      }
      console.error('Login Error:', error);
    }
  };

  return (
    <div className="Login">
      <h2>Login</h2>
      {message && <p style={{ color: message.includes('successful') ? 'blue' : 'red' }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Username or Email:
          <input
            type="text"
            value={usernameOrEmail}
            onChange={(e) => setUsernameOrEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password:
          <input
            type={passwordVisible ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <span onClick={() => setPasswordVisible(!passwordVisible)}>
            {passwordVisible ? '👁️' : '🙈'}
          </span>
        </label>
        <div className="login-link">
          Don't have an account? <Link to="/register">Register here</Link>
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
