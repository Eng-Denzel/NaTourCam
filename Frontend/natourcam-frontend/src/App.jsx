import { Routes, Route, Link } from 'react-router-dom';
import './App.css';

// Import page components (to be created)
import Home from './pages/Home';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Profile from './pages/user/Profile';
import Attractions from './pages/attractions/Attractions';
import Tours from './pages/tours/Tours';
import Bookings from './pages/bookings/Bookings';
import Notifications from './pages/notifications/Notifications';
import Analytics from './pages/analytics/Analytics';
import NotFound from './pages/NotFound';

function App() {
  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">NaTourCam</Link>
        </div>
        <ul className="nav-links">
          <li><Link to="/">Home</Link></li>
          <li><Link to="/attractions">Attractions</Link></li>
          <li><Link to="/tours">Tours</Link></li>
          <li><Link to="/bookings">Bookings</Link></li>
          <li><Link to="/analytics">Analytics</Link></li>
          <li><Link to="/login">Login</Link></li>
          <li><Link to="/register">Register</Link></li>
        </ul>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/attractions" element={<Attractions />} />
          <Route path="/tours" element={<Tours />} />
          <Route path="/bookings" element={<Bookings />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>

      <footer className="footer">
        <p>© 2026 NaTourCam. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
