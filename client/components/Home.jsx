import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import './Home.css';

function Home({ onLogout }) {
  const location = useLocation();

  return (
    <div className={`home-page ${location.pathname === '/home' ? 'show-background' : ''}`}>
      <header className='head'>
        <nav>
          <h1 className='logo'>
            <span className='site-name'>Event</span><span className='site-tagline'>Booking</span>
          </h1>
          <ul className="nav-links">
            <li><NavLink to="/home" activeClassName="active-link">Home</NavLink></li>
            <li><NavLink to="/pricing" activeClassName="active-link">Pricing</NavLink></li>
            <li><NavLink to="/events" activeClassName="active-link">Create Event</NavLink></li>
            <li><NavLink to="/explore" activeClassName="active-link">Explore Events</NavLink></li>
            <li><NavLink to="/admin" activeClassName="active-link">Admin</NavLink></li>
          </ul>
        </nav>
        <p className="event-ticketing">Your gateway to unforgettable moments. Secure your tickets effortlessly, and make every event memorable.</p>
      </header>
    </div>
  );
}

export default Home;
