import React, { useState, useEffect } from 'react';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  // Mock data for notifications
  const mockNotifications = [
    {
      id: 1,
      title: 'Booking Confirmation',
      message: 'Your booking for Mount Cameroon Adventure has been confirmed.',
      type: 'booking_confirmation',
      isRead: false,
      createdAt: '2026-01-15T10:30:00Z'
    },
    {
      id: 2,
      title: 'Payment Successful',
      message: 'Your payment of FCFA 300,000 for Waza Wildlife Safari has been processed.',
      type: 'payment_confirmation',
      isRead: true,
      createdAt: '2026-01-20T14:15:00Z'
    },
    {
      id: 3,
      title: 'Tour Reminder',
      message: 'Your Kribi Coastal Getaway tour starts in 3 days. Please check the meeting point.',
      type: 'tour_reminder',
      isRead: false,
      createdAt: '2026-01-25T09:00:00Z'
    }
  ];

  useEffect(() => {
    // TODO: Fetch notifications from API
    setTimeout(() => {
      setNotifications(mockNotifications);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredNotifications = filter === 'all' 
    ? notifications 
    : notifications.filter(notification => notification.type === filter);

  const markAsRead = (id) => {
    // TODO: Implement API call to mark notification as read
    setNotifications(notifications.map(notification => 
      notification.id === id ? { ...notification, isRead: true } : notification
    ));
  };

  const markAllAsRead = () => {
    // TODO: Implement API call to mark all notifications as read
    setNotifications(notifications.map(notification => 
      ({ ...notification, isRead: true })
    ));
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'booking_confirmation': return '✅';
      case 'payment_confirmation': return '💰';
      case 'tour_reminder': return '⏰';
      case 'tour_update': return '📢';
      default: return '🔔';
    }
  };

  if (loading) {
    return <div className="loading">Loading notifications...</div>;
  }

  return (
    <div className="notifications-page">
      <div className="page-header">
        <h2>Notifications</h2>
        <div className="notification-actions">
          <button 
            className="mark-all-read-button"
            onClick={markAllAsRead}
            disabled={notifications.every(n => n.isRead)}
          >
            Mark All as Read
          </button>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            className="filter-select"
          >
            <option value="all">All Types</option>
            <option value="booking_confirmation">Booking Confirmations</option>
            <option value="payment_confirmation">Payment Confirmations</option>
            <option value="tour_reminder">Tour Reminders</option>
            <option value="tour_update">Tour Updates</option>
          </select>
        </div>
      </div>

      <div className="notifications-list">
        {filteredNotifications.length === 0 ? (
          <div className="no-notifications">
            <p>You have no notifications.</p>
          </div>
        ) : (
          filteredNotifications.map(notification => (
            <div 
              key={notification.id} 
              className={`notification-card ${notification.isRead ? 'read' : 'unread'}`}
            >
              <div className="notification-icon">
                {getNotificationIcon(notification.type)}
              </div>
              <div className="notification-content">
                <h3>{notification.title}</h3>
                <p>{notification.message}</p>
                <div className="notification-meta">
                  <span className="notification-date">
                    {new Date(notification.createdAt).toLocaleDateString()}
                  </span>
                  <span className="notification-type">{notification.type.replace('_', ' ')}</span>
                </div>
              </div>
              {!notification.isRead && (
                <button 
                  className="mark-read-button"
                  onClick={() => markAsRead(notification.id)}
                >
                  Mark as Read
                </button>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Notifications;