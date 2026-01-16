import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { tourismAPI, bookingsAPI, authAPI } from '../../services/api';
import SiteForm from './SiteForm';
import './AdminDashboard.css';

const AdminDashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState({
    totalSites: 0,
    totalBookings: 0,
    totalUsers: 0,
    totalRevenue: 0,
    pendingBookings: 0,
    activeSites: 0,
  });
  const [sites, setSites] = useState([]);
  const [bookings, setBookings] = useState([]);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showSiteForm, setShowSiteForm] = useState(false);
  const [editingSite, setEditingSite] = useState(null);

  useEffect(() => {
    // Check if user is superuser
    if (!user?.is_superuser) {
      navigate('/dashboard');
      return;
    }
    
    fetchDashboardData();
  }, [user, navigate]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel
      const [sitesRes, bookingsRes, usersRes] = await Promise.all([
        tourismAPI.getSites({}),
        bookingsAPI.getBookings(),
        authAPI.getUsers(),
      ]);

      const sitesData = sitesRes.data;
      const bookingsData = bookingsRes.data;
      const usersData = usersRes.data;

      setSites(sitesData);
      setBookings(bookingsData);
      setUsers(usersData);

      // Calculate stats
      const totalRevenue = bookingsData.reduce((sum, booking) => 
        sum + parseFloat(booking.total_price || 0), 0
      );
      const pendingBookings = bookingsData.filter(b => b.status === 'pending').length;
      const activeSites = sitesData.filter(s => s.is_active).length;

      setStats({
        totalSites: sitesData.length,
        totalBookings: bookingsData.length,
        totalUsers: usersData.length,
        totalRevenue: totalRevenue.toFixed(2),
        pendingBookings,
        activeSites,
      });

    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error('Admin dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleSiteStatus = async (siteId, currentStatus) => {
    try {
      await tourismAPI.adminUpdateSite(siteId, { is_active: !currentStatus });
      
      // Update local state
      setSites(sites.map(s => 
        s.id === siteId ? { ...s, is_active: !currentStatus } : s
      ));
      
      // Update stats
      const newActiveSites = !currentStatus 
        ? stats.activeSites + 1 
        : stats.activeSites - 1;
      setStats({ ...stats, activeSites: newActiveSites });
      
      console.log(`Site ${siteId} status toggled to ${!currentStatus}`);
    } catch (err) {
      console.error('Error toggling site status:', err);
      alert('Failed to update site status. Please try again.');
    }
  };

  const handleUpdateBookingStatus = async (bookingId, newStatus) => {
    try {
      await bookingsAPI.updateBooking(bookingId, { status: newStatus });
      fetchDashboardData();
    } catch (err) {
      console.error('Error updating booking status:', err);
    }
  };

  const handleUpdateUserStatus = async (userId, field, value) => {
    try {
      const updateData = { [field]: value };
      await authAPI.adminUpdateUser(userId, updateData);
      
      // Update local state
      setUsers(users.map(u => 
        u.id === userId ? { ...u, [field]: value } : u
      ));
      
      // Show success message (optional)
      console.log(`User ${userId} ${field} updated to ${value}`);
    } catch (err) {
      console.error('Error updating user status:', err);
      alert('Failed to update user status. Please try again.');
    }
  };

  const handleAddSite = () => {
    setEditingSite(null);
    setShowSiteForm(true);
  };

  const handleEditSite = (site) => {
    setEditingSite(site);
    setShowSiteForm(true);
  };

  const handleCloseSiteForm = () => {
    setShowSiteForm(false);
    setEditingSite(null);
  };

  const handleSiteFormSuccess = () => {
    fetchDashboardData();
  };

  if (loading) {
    return <div className="loading">Loading admin dashboard...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>🛡️ Admin Dashboard</h1>
        <p className="admin-subtitle">Manage your tourism platform</p>
      </div>

      {/* Stats Overview */}
      <div className="admin-stats-grid">
        <div className="stat-card stat-primary">
          <div className="stat-icon">🏛️</div>
          <div className="stat-content">
            <h3>Tourist Sites</h3>
            <p className="stat-value">{stats.totalSites}</p>
            <span className="stat-label">{stats.activeSites} active</span>
          </div>
        </div>

        <div className="stat-card stat-success">
          <div className="stat-icon">📅</div>
          <div className="stat-content">
            <h3>Total Bookings</h3>
            <p className="stat-value">{stats.totalBookings}</p>
            <span className="stat-label">{stats.pendingBookings} pending</span>
          </div>
        </div>

        <div className="stat-card stat-info">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>Registered Users</h3>
            <p className="stat-value">{stats.totalUsers}</p>
            <span className="stat-label">Total accounts</span>
          </div>
        </div>

        <div className="stat-card stat-warning">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>Total Revenue</h3>
            <p className="stat-value">{stats.totalRevenue} FCFA</p>
            <span className="stat-label">From all bookings</span>
          </div>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="admin-tabs">
        <button
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`tab-button ${activeTab === 'sites' ? 'active' : ''}`}
          onClick={() => setActiveTab('sites')}
        >
          🏛️ Tourist Sites
        </button>
        <button
          className={`tab-button ${activeTab === 'bookings' ? 'active' : ''}`}
          onClick={() => setActiveTab('bookings')}
        >
          📅 Bookings
        </button>
        <button
          className={`tab-button ${activeTab === 'users' ? 'active' : ''}`}
          onClick={() => setActiveTab('users')}
        >
          👥 Users
        </button>
      </div>

      {/* Tab Content */}
      <div className="admin-content">
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="overview-grid">
              <div className="overview-section">
                <h2>Recent Bookings</h2>
                <div className="recent-list">
                  {bookings.slice(0, 5).map(booking => (
                    <div key={booking.id} className="recent-item">
                      <div className="recent-info">
                        <strong>{booking.tourist_site_name}</strong>
                        <span className="recent-date">
                          {new Date(booking.booking_date).toLocaleDateString()}
                        </span>
                      </div>
                      <span className={`status-badge status-${booking.status}`}>
                        {booking.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="overview-section">
                <h2>Popular Sites</h2>
                <div className="recent-list">
                  {sites.slice(0, 5).map(site => (
                    <div key={site.id} className="recent-item">
                      <div className="recent-info">
                        <strong>{site.name}</strong>
                        <span className="recent-date">{site.region?.name}</span>
                      </div>
                      <span className="site-fee">{site.entrance_fee || 0} FCFA</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sites' && (
          <div className="sites-tab">
            <div className="tab-header">
              <h2>Manage Tourist Sites</h2>
              <button 
                className="add-button"
                onClick={handleAddSite}
              >
                + Add New Site
              </button>
            </div>
            <div className="admin-table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Region</th>
                    <th>Entrance Fee</th>
                    <th>Status</th>
                    <th>Images</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {sites.map(site => (
                    <tr key={site.id}>
                      <td className="site-name-cell">
                        <strong>{site.name}</strong>
                      </td>
                      <td>{site.region?.name}</td>
                      <td>{site.entrance_fee || 0} FCFA</td>
                      <td>
                        <span className={`status-badge ${site.is_active ? 'status-active' : 'status-inactive'}`}>
                          {site.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                      <td>{site.images?.length || 0}</td>
                      <td>
                        <div className="action-buttons-group">
                          <button 
                            className="btn-edit" 
                            title="Edit"
                            onClick={() => handleEditSite(site)}
                          >
                            ✏️
                          </button>
                          <button className="btn-view" title="View" onClick={() => navigate(`/sites/${site.id}`)}>👁️</button>
                          <button 
                            className={`btn-toggle ${site.is_active ? 'btn-deactivate' : 'btn-activate'}`}
                            title={site.is_active ? 'Deactivate' : 'Activate'}
                            onClick={() => handleToggleSiteStatus(site.id, site.is_active)}
                          >
                            {site.is_active ? '🔴' : '🟢'}
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'bookings' && (
          <div className="bookings-tab">
            <div className="tab-header">
              <h2>Manage Bookings</h2>
              <div className="filter-buttons">
                <button className="filter-btn">All</button>
                <button className="filter-btn">Pending</button>
                <button className="filter-btn">Confirmed</button>
                <button className="filter-btn">Completed</button>
              </div>
            </div>
            <div className="admin-table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Site</th>
                    <th>Date</th>
                    <th>Visitors</th>
                    <th>Total Price</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings.map(booking => (
                    <tr key={booking.id}>
                      <td>#{booking.id}</td>
                      <td>{booking.tourist_site_name}</td>
                      <td>{new Date(booking.booking_date).toLocaleDateString()}</td>
                      <td>{booking.number_of_visitors}</td>
                      <td>{booking.total_price} FCFA</td>
                      <td>
                        <select
                          value={booking.status}
                          onChange={(e) => handleUpdateBookingStatus(booking.id, e.target.value)}
                          className={`status-select status-${booking.status}`}
                        >
                          <option value="pending">Pending</option>
                          <option value="confirmed">Confirmed</option>
                          <option value="completed">Completed</option>
                          <option value="cancelled">Cancelled</option>
                        </select>
                      </td>
                      <td>
                        <div className="action-buttons-group">
                          <button className="btn-view" title="View Details">👁️</button>
                          <button className="btn-delete" title="Delete">🗑️</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'users' && (
          <div className="users-tab">
            <div className="tab-header">
              <h2>Manage Users</h2>
              <div className="search-box">
                <input type="text" placeholder="🔍 Search users..." />
              </div>
            </div>
            <div className="admin-table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Username</th>
                    <th>Joined</th>
                    <th>Bookings</th>
                    <th>Active</th>
                    <th>Verified</th>
                    <th>Staff</th>
                    <th>Admin</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(userItem => (
                    <tr key={userItem.id}>
                      <td>#{userItem.id}</td>
                      <td>{userItem.first_name} {userItem.last_name}</td>
                      <td>{userItem.email}</td>
                      <td>@{userItem.username}</td>
                      <td>{new Date(userItem.created_at).toLocaleDateString()}</td>
                      <td>{bookings.filter(b => b.user === userItem.id).length}</td>
                      <td>
                        <label className="toggle-switch">
                          <input
                            type="checkbox"
                            checked={userItem.is_active}
                            onChange={(e) => handleUpdateUserStatus(userItem.id, 'is_active', e.target.checked)}
                            disabled={userItem.id === user?.id}
                          />
                          <span className="toggle-slider"></span>
                        </label>
                      </td>
                      <td>
                        <label className="toggle-switch">
                          <input
                            type="checkbox"
                            checked={userItem.is_verified}
                            onChange={(e) => handleUpdateUserStatus(userItem.id, 'is_verified', e.target.checked)}
                          />
                          <span className="toggle-slider"></span>
                        </label>
                      </td>
                      <td>
                        <label className="toggle-switch">
                          <input
                            type="checkbox"
                            checked={userItem.is_staff}
                            onChange={(e) => handleUpdateUserStatus(userItem.id, 'is_staff', e.target.checked)}
                            disabled={userItem.id === user?.id}
                          />
                          <span className="toggle-slider"></span>
                        </label>
                      </td>
                      <td>
                        <label className="toggle-switch">
                          <input
                            type="checkbox"
                            checked={userItem.is_superuser}
                            onChange={(e) => handleUpdateUserStatus(userItem.id, 'is_superuser', e.target.checked)}
                            disabled={userItem.id === user?.id}
                          />
                          <span className="toggle-slider"></span>
                        </label>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* Site Form Modal */}
      {showSiteForm && (
        <SiteForm
          site={editingSite}
          onClose={handleCloseSiteForm}
          onSuccess={handleSiteFormSuccess}
        />
      )}
    </div>
  );
};

export default AdminDashboard;
